from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_shared_permission(apps, schema_editor):
    ModuleRegistry = apps.get_model('module_engine', 'ModuleRegistry')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Permission = apps.get_model('auth', 'Permission')
    Group = apps.get_model('auth', 'Group')

    content_type = ContentType.objects.get_for_model(ModuleRegistry)

    permission_specs = [
        ('can_add_product', 'Can add products', ['Manager', 'User']),
        ('can_change_product', 'Can change products', ['Manager', 'User']),
        ('can_delete_product', 'Can delete products', ['Manager']),
        ('can_view_product', 'Can view products', ['Manager', 'User']),
    ]

    for codename, name, groups in permission_specs:
        perm, _ = Permission.objects.get_or_create(
            codename=codename,
            name=name,
            content_type=content_type
        )

        perm.group_set.clear()
        
        for group_name in groups:
            group, _ = Group.objects.get_or_create(name=group_name)
            group.permissions.add(perm)

def remove_shared_permission(apps, schema_editor):
    Permission = apps.get_model('auth', 'Permission')
    Permission.objects.filter(codename__in=[
        'can_add_product',
        'can_change_product',
        'can_delete_product',
        'can_view_product'
    ]).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('module_engine', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_shared_permission, reverse_code=remove_shared_permission),
    ]