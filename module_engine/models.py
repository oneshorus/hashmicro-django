from django.db import models


class ModuleRegistry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    version = models.CharField(max_length=20)
    is_installed = models.BooleanField(default=False)
    installed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} (v{self.version}) - ({'Installed' if self.is_installed else 'Not Installed'})"
    
class ModuleSchemaVersion(models.Model):
    module = models.ForeignKey(ModuleRegistry, on_delete=models.CASCADE)
    version = models.CharField(max_length=50)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.module.name} - {self.version}"