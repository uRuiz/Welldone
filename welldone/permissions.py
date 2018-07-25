from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication


class JSONWebTokenAuthenticationQS(BaseJSONWebTokenAuthentication):

    @staticmethod
    def get_jwt_value(request):
        return request.META.get('HTTP_AUTHORIZATION', None)

    def is_valid_jwt(self, request):
        if self.get_jwt_value(request) is None:
            return False
        else:
            authenticate_response = self.authenticate(request)
            request.user = authenticate_response[0]
            return request.user.is_authenticated()


class IsAuthenticatedPermission(JSONWebTokenAuthenticationQS):

    def has_permission(self, request, view):
        return self.is_valid_jwt(request)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated()

