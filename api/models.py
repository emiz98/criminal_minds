from django.db import models


class Investigation(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    network = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class InvestigationData(models.Model):
    investigation = models.ForeignKey(
        Investigation, null=True, on_delete=models.SET_NULL)
    caller = models.CharField(max_length=200, null=False, blank=False)
    receiver = models.CharField(max_length=200, null=False, blank=False)
    call_type = models.IntegerField()
    duration = models.IntegerField()
    imei = models.BigIntegerField()
    imsi = models.BigIntegerField()
    created_at = models.DateTimeField()
