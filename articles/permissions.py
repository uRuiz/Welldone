from welldone.permissions import JSONWebTokenAuthenticationQS


class UserPermissionOnArticles(JSONWebTokenAuthenticationQS):

    def has_permission(self, request, view):
        if view.action in ['retrieve', 'list']:
            return True
        else:
            return self.is_valid_jwt(request)

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and (obj == request.user or request.user.is_staff)
        else:
            return False
