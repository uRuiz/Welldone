# -*- coding: utf-8 -*-
import jwt
from django.utils.translation import ugettext as _
from rest_framework.exceptions import PermissionDenied

from welldone.permissions import JSONWebTokenAuthenticationQS


class UserPermission(JSONWebTokenAuthenticationQS):

    def has_permission(self, request, view):
        if view.action in ['create']:
            return True
        elif view.action in ['list'] or not request.user.is_superuser:
            raise PermissionDenied(_('Action not allowed'))
        else:
            return self.is_valid_jwt(request)

    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve', 'list']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated() and (obj == request.user or request.user.is_staff)
        else:
            return False
