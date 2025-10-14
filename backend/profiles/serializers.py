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
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Kursus
        fields = ['id', 'kursus', 'sted', 'arrangor', 'pris', 'date', 'file_name', 'file_size', 'file_type', 'filename', 'file_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_file_url(self, obj):
        """Generate URL for file download"""
        if obj.has_file:
            return f"/api/kursus/{obj.id}/file/"
        return None


class KursusCreateSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=True)
    
    class Meta:
        model = Kursus
        fields = ['kursus', 'sted', 'arrangor', 'pris', 'date', 'file']
    
    def create(self, validated_data):
        """Handle file upload and store as blob"""
        file_obj = validated_data.pop('file')
        
        # Create kursus instance
        kursus = Kursus.objects.create(**validated_data)
        
        # Store file as blob
        if file_obj:
            kursus.file_data = file_obj.read()
            kursus.file_name = file_obj.name
            kursus.file_size = file_obj.size
            kursus.file_type = file_obj.content_type
            kursus.save()
        
        return kursus
    
    def update(self, instance, validated_data):
        """Handle file update and store as blob"""
        file_obj = validated_data.pop('file', None)
        
        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Update file if provided
        if file_obj:
            instance.file_data = file_obj.read()
            instance.file_name = file_obj.name
            instance.file_size = file_obj.size
            instance.file_type = file_obj.content_type
        
        instance.save()
        return instance


class KursusAdminSerializer(serializers.ModelSerializer):
    """Serializer for admin export - includes bilagsnr"""
    filename = serializers.ReadOnlyField()
    user_full_name = serializers.SerializerMethodField()
    user_trainer_for = serializers.SerializerMethodField()
    
    class Meta:
        model = Kursus
        fields = ['id', 'kursus', 'sted', 'arrangor', 'pris', 'date', 'bilagsnr', 'file_name', 'file_size', 'file_type', 'filename', 'user_full_name', 'user_trainer_for', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_full_name(self, obj):
        full_name = f"{obj.user.first_name} {obj.user.last_name}".strip()
        return full_name if full_name else obj.user.username
    
    def get_user_trainer_for(self, obj):
        if hasattr(obj.user, 'profile'):
            return obj.user.profile.trainer_for
        return ''
