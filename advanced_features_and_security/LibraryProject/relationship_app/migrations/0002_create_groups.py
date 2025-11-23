from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # permission codenames defined on Book model
    codenames = ['can_view', 'can_create', 'can_edit', 'can_delete']
    perms = Permission.objects.filter(content_type__app_label='relationship_app', codename__in=codenames)

    editors, _ = Group.objects.get_or_create(name='Editors')
    viewers, _ = Group.objects.get_or_create(name='Viewers')
    admins, _ = Group.objects.get_or_create(name='Admins')

    # assign permissions
    editors.permissions.set(perms.filter(codename__in=['can_create', 'can_edit', 'can_view']))
    viewers.permissions.set(perms.filter(codename__in=['can_view']))
    admins.permissions.set(perms)


def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['Editors', 'Viewers', 'Admins']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('relationship_app', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
