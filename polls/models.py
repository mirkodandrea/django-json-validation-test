from django.db import models


class JSONSchema(models.Model):
    name = models.CharField(max_length=255)
    schema = models.JSONField()

    def __str__(self):
        return self.name


class JSONData(models.Model):
    schema = models.ForeignKey(
        JSONSchema, on_delete=models.CASCADE, blank=True, null=True)
    data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.schema.name} Data"
