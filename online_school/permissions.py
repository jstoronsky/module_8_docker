from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    message = 'У пользователя нет прав доступа'

    def has_permission(self, request, view):
        groups_names = [group.name for group in request.user.groups.all()]
        if request.user.groups.all().count() != 0 and 'Moderators' in groups_names:
            return True
        return False


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.added_by:
            return True
        return False
