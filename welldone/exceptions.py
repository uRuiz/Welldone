# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from rest_framework.exceptions import APIException


class RelationDelete(APIException):
    status_code = 204
    default_detail = _('Deleted relation.')
    default_code = _('relation_delete')
