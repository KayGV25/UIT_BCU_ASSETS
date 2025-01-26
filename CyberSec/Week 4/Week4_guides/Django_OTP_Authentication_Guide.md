
# Django OTP Authentication with Username, Password, and OTP on Apache Server

This guide provides instructions to set up a Django application with an authentication system using a username, password, and one-time password (OTP), served by Apache.

### Prerequisites

- Ensure OpenSSL is installed on your system.
- Install the required Python packages: `django`, `django-otp`, and `djangorestframework`.

```bash
python -m pip install django django-otp djangorestframework
```

---

## Step 1: Django Setup

1. **Create a Django project** and an app for authentication:

   ```bash
   django-admin startproject myauthproject
   cd myauthproject
   python manage.py startapp auth_app
   ```

2. **Run initial migrations**:

   ```bash
   python manage.py migrate
   ```

3. **Create a superuser** (optional but useful for testing and management):

   ```bash
   python manage.py createsuperuser
   ```

4. **Start the Django development server** (optional, for local testing):

   ```bash
   python manage.py runserver
   ```

---

## Step 2: Configure Django OTP and Authentication Settings

Edit `settings.py` to configure Django OTP and add the necessary middleware and apps:

```python
# settings.py

INSTALLED_APPS = [
   'django.contrib.sites',
   'django_otp',
   'django_otp.plugins.otp_totp',  # Time-based OTP
   'rest_framework',
   'auth_app',  # Your custom authentication app
]

MIDDLEWARE = [
   'django_otp.middleware.OTPMiddleware',  # Middleware for OTP
]

SITE_ID = 1  # Required for OTP functionality
```

Configure Django REST Framework (if using APIs):

```python
REST_FRAMEWORK = {
   'DEFAULT_AUTHENTICATION_CLASSES': [
       'rest_framework.authentication.SessionAuthentication',
   ],
}
```

---

## Step 3: Model for Shared Secret

Create a `UserProfile` model in `auth_app/models.py` to store a shared secret for OTP generation:

```python
# auth_app/models.py
from django.contrib.auth.models import User
from django.db import models
from django_otp.plugins.otp_totp.models import TOTPDevice

class UserProfile(models.Model):
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   shared_secret = models.CharField(max_length=50)  # Store shared secret here
   otp_device = models.OneToOneField(TOTPDevice, on_delete=models.SET_NULL, null=True, blank=True)

   def __str__(self):
       return self.user.username
```

Run migrations to apply the new model:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Step 4: Generate OTP and Authenticate with Username, Password, and OTP

1. **Create views to register a shared secret and authenticate using Username, Password, and OTP** in `auth_app/views.py`.

   ```python
   # auth_app/views.py
   import pyotp
   from django_otp.plugins.otp_totp.models import TOTPDevice
   from rest_framework import status
   from rest_framework.decorators import api_view
   from rest_framework.response import Response
   from django.contrib.auth import authenticate
   from .models import UserProfile

   @api_view(['POST'])
   def register_secret(request):
       user = request.user
       secret = pyotp.random_base32()  # Generate a random shared secret
       user_profile, created = UserProfile.objects.get_or_create(user=user)
       user_profile.shared_secret = secret
       user_profile.save()
       return Response({"shared_secret": secret}, status=status.HTTP_200_OK)

   @api_view(['POST'])
   def authenticate_with_otp(request):
       username = request.data.get('username')
       password = request.data.get('password')
       otp = request.data.get('otp')
       
       # First, authenticate the username and password
       user = authenticate(username=username, password=password)
       if user:
           user_profile, created = UserProfile.objects.get_or_create(user=user)
           if not user_profile.otp_device:
               device = TOTPDevice.objects.create(user=user, key=user_profile.shared_secret)
               user_profile.otp_device = device
               user_profile.save()

           # Verify the OTP
           if user_profile.otp_device.verify_token(otp):
               return Response({"message": "Authentication successful"}, status=status.HTTP_200_OK)
           else:
               return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
       else:
           return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
   ```

2. **Define URLs** in `auth_app/urls.py` for registration and OTP authentication:

   ```python
   # auth_app/urls.py
   from django.urls import path
   from .views import register_secret, authenticate_with_otp

   urlpatterns = [
       path('register-secret/', register_secret, name='register_secret'),
       path('authenticate/', authenticate_with_otp, name='authenticate_with_otp'),
   ]
   ```

3. **Include these URLs** in the main `urls.py` file of the Django project:

   ```python
   # myauthproject/urls.py
   from django.urls import include, path

   urlpatterns = [
       path('auth/', include('auth_app.urls')),
   ]
   ```

---

## Step 5: Configure Apache for Django

1. **Install `mod_wsgi`**:

   ```bash
   sudo apt-get install libapache2-mod-wsgi-py3
   ```

2. **Set Up Virtual Host** for Django in Apache configuration (e.g., `/etc/apache2/sites-available/myauthproject.conf`):

   ```apache
   <VirtualHost *:80>
       ServerAdmin admin@example.com
       ServerName myauthproject.com

       Alias /static /path/to/myauthproject/static
       <Directory /path/to/myauthproject/static>
           Require all granted
       </Directory>

       <Directory /path/to/myauthproject/myauthproject>
           <Files wsgi.py>
               Require all granted
           </Files>
       </Directory>

       WSGIDaemonProcess myauthproject python-path=/path/to/myauthproject
       WSGIProcessGroup myauthproject
       WSGIScriptAlias / /path/to/myauthproject/myauthproject/wsgi.py
   </VirtualHost>
   ```

3. **Restart Apache**:

   ```bash
   sudo service apache2 restart
   ```

---

## Usage

1. **Register Shared Secret**:  
   After logging in, a user sends a request to `auth/register-secret/` to generate a shared secret for OTP.

2. **Authenticate with Username, Password, and OTP**:  
   The user submits their `username`, `password`, and `OTP` to `auth/authenticate/`. If all three factors are valid, the server authenticates the user successfully.

---

This setup provides a secure authentication system using a username, password, and OTP with Django, served by Apache. This method offers a layered security approach to ensure safe user access.
