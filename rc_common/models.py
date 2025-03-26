from django.db import models
from jsonfield import JSONField

# Create your models here.

class CommonConfigurations(models.Model):
    name = models.CharField(max_length=100,default='')
    data = JSONField(default={})

    class Meta:
        permissions = [
            ('system_reset_permissions', 'System Reset Permissions'),
            ('developer_permissions', 'Developer Permissions'),
            ('dashboard_permissions', 'Dashboard Permissions')
        ]
