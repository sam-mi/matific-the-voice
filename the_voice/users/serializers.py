from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User, UserProfile


__author__ = 'pure'
__created__ = '21/09/2014'
__copyright__ = 'Copyright (C) 2014 PureCreative'



class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PasswordSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)


class UserProfileSerializer(serializers.HyperlinkedModelSerializer):

    user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    user = serializers.ReadOnlyField(source='user.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email')
    salutation = serializers.CharField(source='user.salutation')
    name = serializers.CharField(source='user.name')

    class Meta:
        model = UserProfile
        depth=1
        fields = (
            'url', 'id', 'username', 'email', 'salutation', 'name',
            'user', 'user_url', 'terms', 'privacy', 'fairplay', 'welcome',
        )
        read_only_fields = ('user',)

    def update(self, instance, validated_data):

        # retrieve the User
        user_data = validated_data.pop('user', None)
        for attr, val in user_data.items():
            setattr(instance.user, attr, val)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance



class UserSerializer(serializers.HyperlinkedModelSerializer):
    #votes = serializers.HyperlinkedRelatedField(many=True, view_name="users-list", lookup_field="username")
    #permissions = serializers.HyperlinkedRelatedField(many=True, view_name='permission-detail')

    profile = UserProfileSerializer(read_only=True)
    permissions = serializers.ReadOnlyField(source='get_all_permissions')

    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'groups', 'url',
            'salutation', 'name', 'permissions',
            'date_joined', 'profile'
        )
        read_only_fields = ('date_joined',)
        write_only_fields = ('password', 'confirm_password')
