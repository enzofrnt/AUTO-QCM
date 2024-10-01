import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import migrations

logger = logging.getLogger(__name__)


# Function to create the default superuser
def create_default_admin(apps, schema_editor):
    User = get_user_model()
    Setting = apps.get_model("app", "AdminCreationFlag")

    # Check if the admin user has already been created
    if not Setting.objects.filter(flag="admin_created").exists():
        # Create the admin user
        user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="changeme",
            must_change_password=True,
        )

        # Mark the admin creation to avoid future executions
        Setting.objects.create(flag="admin_created")

        enseignant_goup = Group.objects.create(name="Enseignant")
        user.groups.add(enseignant_goup)
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0001_initial"),
    ]

    operations = [
        # Execute the logic to create the admin user only once
        migrations.RunPython(create_default_admin),
    ]
