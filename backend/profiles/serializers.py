from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Kursus


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'username', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'trainer_for', 'reg_number', 'account_number', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['trainer_for', 'reg_number', 'account_number']
    
    def validate(self, data):
        # Check if all required fields are provided
        required_fields = ['trainer_for', 'reg_number', 'account_number']
        for field in required_fields:
            if not data.get(field):
                raise serializers.ValidationError(f"{field} er påkrævet for at tilføje kurser.")
        return data


class KursusSerializer(serializers.ModelSerializer):
    filename = serializers.ReadOnlyField()
    
    class Meta:
        model = Kursus
        fields = ['id', 'kursus', 'sted', 'arrangor', 'pris', 'date', 'file', 'filename', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class KursusCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kursus
        fields = ['kursus', 'sted', 'arrangor', 'pris', 'date', 'file']
    
    def validate_file(self, value):
        # File is now optional for testing purposes
        return value


class KursusAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin export - includes bilagsnr"""
    filename = serializers.ReadOnlyField()
    user_full_name = serializers.SerializerMethodField()
    user_trainer_for = serializers.SerializerMethodField()
    
    class Meta:
        model = Kursus
        fields = ['id', 'kursus', 'sted', 'arrangor', 'pris', 'date', 'bilagsnr', 'file', 'filename', 'user_full_name', 'user_trainer_for', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_full_name(self, obj):
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full_name if full_name else obj.user.username
    
    def get_user_trainer_for(self, obj):
        if hasattr(obj.user, 'profile'):
            return obj.user.profile.trainer_for
        return ''
