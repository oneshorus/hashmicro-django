from django.db import migrations
from django.contrib.auth.hashers import make_password


def create_default_users(apps, schema_editor):
    User = apps.get_model('hashmicro', 'User')

    users = [
        {"username": "manager1", "password": "manager123", "role": "manager"},
        {"username": "user1", "password": "user123", "role": "user"},
    ]

    for data in users:
        if not User.objects.filter(username=data["username"]).exists():
            User.objects.create(
                username=data["username"],
                password=make_password(data["password"]),
                role=data["role"],
                is_staff=True
            )

class Migration(migrations.Migration):

    dependencies = [
        ('hashmicro', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_users),
    ]