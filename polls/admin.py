from django.contrib import admin
from django import forms
from .models import JSONSchema, JSONData
from django_jsonform.widgets import JSONFormWidget
from django_jsonform.validators import JSONSchemaValidator, JSONSchemaValidationError


class JSONDataAdminForm(forms.ModelForm):
    reset_data = forms.BooleanField(label='Reset Data', required=False,
                                    initial=False, help_text='Check this box to reset the data to default.')

    class Meta:
        model = JSONData
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(JSONDataAdminForm, self).__init__(*args, **kwargs)
        if self.instance.schema_id:
            schema = self.instance.schema.schema
            data = self.instance.data
            validator = JSONSchemaValidator(schema)
            try:
                if data is not None:
                    validator(data)
                self.fields['data'].widget = JSONFormWidget(schema=schema)

            except JSONSchemaValidationError as e:
                # create a textarea widget and a reset button
                self.fields['data'].widget = forms.Textarea()
                self.fields['data'].initial = data
                self.fields['data'].help_text = str(e)
                self.fields['data'].required = False
                self.fields['data'].label = 'Invalid Data'
                self.fields['data'].widget.attrs['readonly'] = True

    def clean_data(self):
        if self.data.get('reset_data', 'off') == 'on':
            self.instance.data = None
            self.instance.save()
            self.cleaned_data['data'] = None

        return self.cleaned_data['data']


class JSONDataAdmin(admin.ModelAdmin):
    form = JSONDataAdminForm


admin.site.register(JSONSchema)
admin.site.register(JSONData, JSONDataAdmin)
