# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import Follower


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

class RelatedObjectDoesNotExist(object):
    pass

class UserCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

class SignupSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        pass

    @staticmethod
    def encrypt_password(validated_data):
        password = validated_data.get('password')
        if password:
            validated_data['password'] = make_password(password)
        validated_data['is_active'] = True

    @staticmethod
    def validate_fields(validated_data):
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')

        error_list = []
        if not (email and email.strip()):
            error_list.append(ValidationError(_('Email is empty'), code='100'))
        if not (first_name and first_name.strip()):
            error_list.append(ValidationError(_('First name is empty'), code='101'))
        if not (last_name and last_name.strip()):
            error_list.append(ValidationError(_('Last name is empty'), code='102'))

        if len(error_list) == 0:
            validated_data['is_active'] = True
        else:
            raise ValidationError(error_list)

    def create(self, validated_data):
        """
        Encrypts the password and creates the user
        """
        self.encrypt_password(validated_data)
        self.validate_fields(validated_data)
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        """
        Encrypts the password and updates the user
        """
        self.encrypt_password(validated_data)
        self.validate_fields(validated_data)
        return super(UserSerializer, self).update(instance, validated_data)


class FollowUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follower
        fields = ('followed',)
