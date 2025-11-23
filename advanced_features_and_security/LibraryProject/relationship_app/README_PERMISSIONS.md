Permissions & Groups Setup (relationship_app)

Overview

- This app defines custom permissions for the `Book` model with codenames:
  - `can_view` — view book listings and details
  - `can_create` — create new books
  - `can_edit` — edit existing books
  - `can_delete` — delete books

What I changed

- `models.py` (Book.Meta.permissions) now declares the above codenames.
- `views.py` decorators/mixins enforce those permissions:
  - `@permission_required('relationship_app.can_view', raise_exception=True)` on `list_books`
  - `LibraryDetailView` uses `PermissionRequiredMixin` with `permission_required = 'relationship_app.can_view'`
  - `@permission_required('relationship_app.can_create', raise_exception=True)` on `add_book`
  - `@permission_required('relationship_app.can_edit', raise_exception=True)` on `edit_book`
  - `@permission_required('relationship_app.can_delete', raise_exception=True)` on `delete_book`
- Added a data migration `0002_create_groups.py` that creates 3 groups and assigns permissions:
  - `Editors` => `can_create`, `can_edit`, `can_view`
  - `Viewers` => `can_view`
  - `Admins` => all book permissions

How to apply and test

1. Apply migrations (this will also create the groups):

   ```
   cd C:\Users\Rabiatu\Desktop\django-models\advanced_features_and_security\LibraryProject
   python manage.py migrate
   ```

2. Create users and assign groups (via admin or shell):

   - Using admin UI: log in as a superuser, go to Groups, verify `Editors`, `Viewers`, `Admins` exist and have appropriate permissions.
   - Or using shell:
     ```
     python manage.py shell
     from django.contrib.auth.models import Group
     Group.objects.all()
     ```

3. Test permissions manually:
   - Create users and add them to `Editors`/`Viewers`/`Admins` groups.
   - Log in as each user and verify access:
     - Viewers should access book listings/details but not create/edit/delete.
     - Editors should create and edit books but not delete (unless you grant delete).
     - Admins have all permissions.

Notes

- The groups are created by the migration `0002_create_groups.py`. If you prefer to manage groups via the admin UI, you may remove or skip that migration.
- If you add more models with custom permissions, extend the migration or add a new RunPython migration to assign permissions to groups.
