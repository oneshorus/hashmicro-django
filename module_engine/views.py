import subprocess
import importlib
import sys
from django.contrib.auth.decorators import user_passes_test
from django.urls import Resolver404
from django.urls.resolvers import URLResolver, RegexPattern
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.http import Http404
from .models import ModuleRegistry, ModuleSchemaVersion
from .utils import discover_modules


def module_dispatcher(request, module_name, remaining_path=""):
    try:
        module = ModuleRegistry.objects.get(name=module_name, is_installed=True)
    except ModuleRegistry.DoesNotExist:
        raise Http404("Module not installed")

    try:
        module_urls = importlib.import_module(f"{module_name}.urls")
        urlpatterns = getattr(module_urls, 'urlpatterns', None)
        if urlpatterns is None:
            raise Http404("No urlpatterns in module")
    except ModuleNotFoundError:
        raise Http404("Module URL config not found")

    resolver = URLResolver(RegexPattern(r''), urlpatterns)

    try:
        print(f"Trying to resolve path: '{remaining_path}' in {module_name}")
        normalized_path = remaining_path
        if normalized_path and not normalized_path.endswith('/'):
            normalized_path += '/'

        callback, callback_args, callback_kwargs = resolver.resolve(normalized_path)

        callback_kwargs['module_name'] = module_name
        print(f"Dispatching to: {callback.__name__} with args: {callback_args}, kwargs: {callback_kwargs}")
        return callback(request, *callback_args, **callback_kwargs)
    except Resolver404:
        raise Http404("No matching route in module")


def dashboard(request):
    modules = ModuleRegistry.objects.filter(is_installed=True)
    title = "HASHMICRO | Dashboard"
    return render(request, 'dashboard.html', {
        'modules': modules,
        'title': title
    })


@user_passes_test(lambda u: u.is_superuser)
def module_list(request):
    module_lists = discover_modules()
    # module_lists = ModuleRegistry.objects.all()
    module_name = "Modules"
    title = 'HASHMICRO | Modules'
    
    return render(request, 'module_engine/module_list.html', {
        'title': title,
        'current_module': module_name,
        'modules': module_lists,
    })


@user_passes_test(lambda u: u.is_superuser)
def install_module(request, module_name):
    try:
        module = ModuleRegistry.objects.get(name=module_name)
        module.is_installed = True
        module.installed_at = now()
        module.save()
        
        # Run migrations
        subprocess.call([sys.executable, 'manage.py', 'makemigrations', module_name])
        subprocess.call([sys.executable, 'manage.py', 'migrate', module_name])
    except ModuleRegistry.DoesNotExist:
        pass
    return redirect('module-list')


@user_passes_test(lambda u: u.is_superuser)
def uninstall_module(request, module_name):
    try:
        module = ModuleRegistry.objects.get(name=module_name)
        module.is_installed = False
        module.installed_at = None
        module.save()

        # Optional: delete all tables (DANGEROUS for prod use)
        # subprocess.call([sys.executable, 'manage.py', 'flush'])

    except ModuleRegistry.DoesNotExist:
        pass
    return redirect('module-list')


@user_passes_test(lambda u: u.is_superuser)
def upgrade_module(request, module_name):
    try:
        module = ModuleRegistry.objects.get(name=module_name)

        mod_meta = importlib.import_module(f"{module_name}.module_meta")
        new_version = mod_meta.MODULE_INFO.get("version", module.version)

        ModuleSchemaVersion.objects.create(module=module, version=new_version)

        if new_version != module.version:
            module.version = new_version
            module.installed_at = now()
            module.save()

            subprocess.call([sys.executable, 'manage.py', 'makemigrations', module_name])
            subprocess.call([sys.executable, 'manage.py', 'migrate', module_name])
    except Exception as e:
        print(f"Upgrade failed: {e}")
    return redirect('module-list')