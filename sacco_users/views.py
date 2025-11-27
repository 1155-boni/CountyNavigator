from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from .models import SaccoUser
from .serializers import SaccoUserSerializer, SaccoUserCreateSerializer

class UserListCreateView(generics.ListCreateAPIView):
    queryset = SaccoUser.objects.all()
    serializer_class = SaccoUserSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SaccoUserCreateSerializer
        return SaccoUserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaccoUser.objects.all()
    serializer_class = SaccoUserSerializer
    permission_classes = [IsAdminUser]

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.is_superuser:
        users = SaccoUser.objects.exclude(is_superuser=True).exclude(id=request.user.id)
    else:
        users = SaccoUser.objects.all()
    return render(request, 'dashboard.html', {'users': users})

def profile_view(request, pk):
    if not request.user.is_authenticated:
        return redirect('login')
    user = get_object_or_404(SaccoUser, pk=pk)
    return render(request, 'profile.html', {'user': user})

def add_user_view(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        id_number = request.POST.get('id_number')
        membership_number = request.POST.get('membership_number')
        county = request.POST.get('county')
        sub_county = request.POST.get('sub_county')
        ward = request.POST.get('ward')
        stage = request.POST.get('stage')
        next_of_kin_first_name = request.POST.get('next_of_kin_first_name')
        next_of_kin_last_name = request.POST.get('next_of_kin_last_name')
        next_of_kin_id_number = request.POST.get('next_of_kin_id_number')
        next_of_kin_phone = request.POST.get('next_of_kin_phone')
        stage_chairman_first_name = request.POST.get('stage_chairman_first_name')
        stage_chairman_last_name = request.POST.get('stage_chairman_last_name')
        stage_chairman_phone = request.POST.get('stage_chairman_phone')
        ward_chairman_first_name = request.POST.get('ward_chairman_first_name')
        ward_chairman_last_name = request.POST.get('ward_chairman_last_name')
        ward_chairman_phone = request.POST.get('ward_chairman_phone')
        sub_county_chairman_first_name = request.POST.get('sub_county_chairman_first_name')
        sub_county_chairman_last_name = request.POST.get('sub_county_chairman_last_name')
        sub_county_chairman_phone = request.POST.get('sub_county_chairman_phone')
        motor_bike_model = request.POST.get('motor_bike_model')
        motor_bike_registration_number = request.POST.get('motor_bike_registration_number')
        motor_bike_color = request.POST.get('motor_bike_color')
        password = request.POST.get('password', 'defaultpassword')
        try:
            user = SaccoUser.objects.create_user(
                username=username,
                first_name=first_name,
                middle_name=middle_name,
                last_name=last_name,
                email=email,
                phone=phone,
                id_number=id_number,
                membership_number=membership_number,
                county=county,
                sub_county=sub_county,
                ward=ward,
                stage=stage,
                next_of_kin_first_name=next_of_kin_first_name,
                next_of_kin_last_name=next_of_kin_last_name,
                next_of_kin_id_number=next_of_kin_id_number,
                next_of_kin_phone=next_of_kin_phone,
                stage_chairman_first_name=stage_chairman_first_name,
                stage_chairman_last_name=stage_chairman_last_name,
                stage_chairman_phone=stage_chairman_phone,
                ward_chairman_first_name=ward_chairman_first_name,
                ward_chairman_last_name=ward_chairman_last_name,
                ward_chairman_phone=ward_chairman_phone,
                sub_county_chairman_first_name=sub_county_chairman_first_name,
                sub_county_chairman_last_name=sub_county_chairman_last_name,
                sub_county_chairman_phone=sub_county_chairman_phone,
                motor_bike_model=motor_bike_model,
                motor_bike_registration_number=motor_bike_registration_number,
                motor_bike_color=motor_bike_color,
                password=password
            )
            user.generate_qr_code()
            user.save()
            messages.success(request, 'User added successfully.')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error adding user: {str(e)}')
    return render(request, 'add_user.html')

def edit_user_view(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    user = get_object_or_404(SaccoUser, pk=pk)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.id_number = request.POST.get('id_number')
        try:
            user.save()
            messages.success(request, 'User updated successfully.')
            return redirect('dashboard')
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    return render(request, 'edit_user.html', {'user': user})

def delete_user_view(request, pk):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('login')
    user = get_object_or_404(SaccoUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('dashboard')
    return render(request, 'delete_user.html', {'user': user})

def scan_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        qr_data = data.get('qr_data')
        if qr_data and qr_data.startswith('/users/'):
            try:
                user_id = int(qr_data.split('/')[2])
                user = get_object_or_404(SaccoUser, pk=user_id)
                return JsonResponse({'success': True, 'redirect_url': f'/sacco_users/profile/{user_id}/'})
            except (ValueError, IndexError):
                return JsonResponse({'success': False, 'error': 'Invalid QR code data.'})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid QR code format.'})
    return render(request, 'scan.html')
