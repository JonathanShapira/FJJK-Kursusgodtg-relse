from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile, Kursus
from .serializers import UserProfileSerializer, UserProfileUpdateSerializer, UserSerializer, KursusSerializer, KursusCreateSerializer


class UserProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Retrieve and update user profile
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    Get current user information
    """
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update user profile information
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    serializer = UserProfileUpdateSerializer(profile, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Profile updated successfully',
            'profile': UserProfileSerializer(profile).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_page_data(request):
    """
    Get all data needed for the profile page
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    user_data = UserSerializer(request.user).data
    profile_data = UserProfileSerializer(profile).data
    
    return Response({
        'user': user_data,
        'profile': profile_data
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_user_info(request):
    """
    Update user information (email, first_name, last_name)
    """
    try:
        user = request.user
        data = request.data
        
        if 'email' in data:
            user.email = data['email']
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        
        user.save()
        
        return Response({
            'success': True,
            'message': 'User information updated successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@login_required
def profile_page(request):
    """
    Serve the profile page HTML
    """
    return render(request, 'profiles/profile.html')


# Kursus API Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_kursus_list(request):
    """
    Get all kursus records for the current user
    """
    kursus_records = Kursus.objects.filter(user=request.user)
    serializer = KursusSerializer(kursus_records, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_kursus(request):
    """
    Create a new kursus record
    """
    # Check if user has completed their profile
    try:
        profile = request.user.profile
        if not profile.trainer_for or not profile.reg_number or not profile.account_number:
            return Response({
                'error': 'Du skal udfylde alle påkrævede felter (Træner for, Reg nr, Konto nr) før du kan tilføje kurser.'
            }, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response({
            'error': 'Profil ikke fundet. Kontakt administrator.'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = KursusCreateSerializer(data=request.data)
    if serializer.is_valid():
        kursus = serializer.save(user=request.user)
        return Response(KursusSerializer(kursus).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_kursus_detail(request, kursus_id):
    """
    Get a specific kursus record
    """
    kursus = get_object_or_404(Kursus, id=kursus_id, user=request.user)
    serializer = KursusSerializer(kursus)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_kursus(request, kursus_id):
    """
    Update a kursus record
    """
    kursus = get_object_or_404(Kursus, id=kursus_id, user=request.user)
    
    if request.method == 'PUT':
        serializer = KursusCreateSerializer(kursus, data=request.data)
    else:  # PATCH
        serializer = KursusCreateSerializer(kursus, data=request.data, partial=True)
    
    if serializer.is_valid():
        serializer.save()
        return Response(KursusSerializer(kursus).data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_kursus(request, kursus_id):
    """
    Delete a kursus record
    """
    kursus = get_object_or_404(Kursus, id=kursus_id, user=request.user)
    kursus.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
