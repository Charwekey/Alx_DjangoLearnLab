# Managing Permissions and Groups in Django

This project demonstrates how to manage permissions and groups in Django for fine-grained access control.

## Custom Permissions
The Post model defines four custom permissions:

- `can_view`
- `can_create`
- `can_edit`
- `can_delete`

These permissions are created inside the model's Meta class.

## Groups Setup
Three groups were created in Django Admin:

### Viewers
- can_view

### Editors
- can_view
- can_create
- can_edit

### Admins
- can_view
- can_create
- can_edit
- can_delete

## View-Level Permission Enforcement
Views use `@permission_required()` to restrict access:

- Viewing posts → `can_view`
- Creating posts → `can_create`
- Editing posts → `can_edit`
- Deleting posts → `can_delete`

## Testing
1. Create several test users.
2. Assign each user to one of the groups.
3. Log in as each user and attempt different actions.
4. Verify that permissions correctly allow or block access.

This completes the permissions and groups setup.
