from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, LoginForm, ImageUploadForm
from .models import CustomUser, UserImage
from .utils import extract_exif, calculate_hash, encrypt_image, verify_image
import rsa
from django.shortcuts import render
from .backends import TelephoneBackend  # Add this import
from django.contrib.auth.hashers import make_password
from cryptography.fernet import Fernet  # For AES


#register
#This is Third code
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Keys will be auto-generated via save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'authsystem/register.html', {'form': form})


#user login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data['telephone']
            password = form.cleaned_data['password']
            
            # Authenticate using telephone
            user = authenticate(request, telephone=telephone, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid telephone or password. Please try again.')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = LoginForm()
    return render(request, 'authsystem/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    images = UserImage.objects.filter(user=user).order_by('-uploaded_at')
    return render(request, 'authsystem/dashboard.html', {
        'user': user,
        'images': images
    })

#new code to try handle image size
@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                image_file = request.FILES['image']
                exif_data = extract_exif(image_file)
                
                # ... (your existing EXIF validation code) ...
                # Camera verification logic
                if not request.user.camera_make or not request.user.camera_model:
                    if exif_data and 'Make' in exif_data and 'Model' in exif_data:
                        request.user.camera_make = exif_data['Make']
                        request.user.camera_model = exif_data['Model']
                        request.user.save()
                    else:
                        messages.error(request, 'No EXIF data found. Please upload an image with metadata.')
                        return render(request, 'authsystem/upload.html', {'form': form})
                
                # Verify camera matches
                if exif_data and ('Make' not in exif_data or 'Model' not in exif_data or 
                                 exif_data['Make'] != request.user.camera_make or 
                                 exif_data['Model'] != request.user.camera_model):
                    messages.error(request, 'This image was not captured by you')
                    return render(request, 'authsystem/upload.html', {'form': form})
                

                # Process image
                image_file.seek(0)
                image_hash = calculate_hash(image_file)
                
                  # Check if any user has uploaded this image before
                if UserImage.objects.filter(image_hash=image_hash).exists():
                    messages.error(request, 'Blocked by duplicate hash check')
                    return redirect('upload')
                
                image_file.seek(0)
                encrypted_data = encrypt_image(image_file, request.user.get_public_key())
                
                # Save to model
                user_image = form.save(commit=False)
                user_image.user = request.user
                user_image.encrypted_image = encrypted_data
                user_image.image_hash = image_hash
                user_image.camera_make = exif_data.get('Make')
                user_image.camera_model = exif_data.get('Model')
                user_image.save()
                
                messages.success(request, 'Image uploaded and verified successfully!')
                return redirect('dashboard')
                
            except Exception as e:
                messages.error(request, f'Error processing image: {str(e)}')
                return render(request, 'authsystem/upload.html', {'form': form})
    
    else:
        form = ImageUploadForm()
    return render(request, 'authsystem/upload.html', {'form': form})


# authsystem/views.py
def index(request):
    return render(request, 'authsystem/index.html')

