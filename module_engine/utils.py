import importlib
from django.conf import settings
from django.urls import path, include
from .models import ModuleRegistry
# from django.utils.timezone import now

def discover_modules():
    all = []
    for app in settings.INSTALLED_APPS:
        try:
            mod_meta = importlib.import_module(f"{app}.module_meta")
            info = getattr(mod_meta, "MODULE_INFO", None)
            if info:
                obj, created = ModuleRegistry.objects.get_or_create(name=info["name"], defaults={
                    "description": info.get("description", ""),
                    "version": info.get("version", "0.0.1"),
                    "is_installed": False
                })
                if not created and obj.version != info["version"]:
                    obj.description = info["description"]
                    obj.save()
                obj.new_version = info["version"]
                all.append(obj)
        except ModuleNotFoundError:
            continue
        
    return all

def get_dynamic_urlpatterns():
    dynamic_patterns = []

    for module in ModuleRegistry.objects.filter(is_installed=True):
        try:
            module_url = importlib.import_module(f"{module.name}.urls")
            dynamic_patterns.append(
                path(f"{module.name}/", include((module_url.urlpatterns, module.name)))
            )
        except ModuleNotFoundError:
            continue

    return dynamic_patterns