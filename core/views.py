from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login, logout, authenticate
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

def register_account(request):
    if request.user.is_authenticated:
        return redirect('/admin/')

    errors = {}
    values = {}
    registered = False

    if request.method == 'POST':
        # Read the raw data from the HTML form
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # Keep what the user typed so the form can be refilled on error
        # (passwords are never sent back to the template)
        values = {'username': username, 'email': email}

        # ----- Username -----
        if not username:
            errors['username'] = 'Username is required.'
        elif len(username) > 50:
            errors['username'] = 'Username cannot be more than 50 characters.'
        else:
            try:
                User.username_validator(username)  # allowed characters only
            except ValidationError:
                errors['username'] = 'Use only letters, numbers and @/./+/-/_ characters.'
            else:
                if User.objects.filter(username__iexact=username).exists():
                    errors['username'] = 'This username is already in use.'

        # ----- Email -----
        if not email:
            errors['email'] = 'Email is required.'
        else:
            try:
                validate_email(email)
            except ValidationError:
                errors['email'] = 'Enter a valid email address.'
            else:
                if User.objects.filter(email__iexact=email).exists():
                    errors['email'] = 'This email is already in use.'

        # ----- Password -----
        if not password:
            errors['password'] = ['Password is required.']
        else:
            try:
                # Runs the validators in AUTH_PASSWORD_VALIDATORS (settings.py)
                validate_password(password, user=User(username=username, email=email))
            except ValidationError as e:
                errors['password'] = list(e.messages)

        if not confirm_password:
            errors['confirm_password'] = 'Please confirm your password.'
        elif password and password != confirm_password:
            errors['confirm_password'] = 'Passwords do not match.'

        # ----- Group -----
        group = Group.objects.filter(name='Booking staff').first()
        if group is None:
            errors['general'] = 'Registration is unavailable right now. Please contact an admin.'

        # ----- Create the user -----
        if not errors:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_active=False,  # an admin must activate the account
            )
            user.groups.add(group)
            registered = True

    context = {
        'errors': errors,
        'values': values,
        'registered': registered,
    }
    return render(request, 'register.html', context)

def home(request):
    return render(request, 'index.html')

def login_account(request):
    # Where to send the user after a successful login
    next_url = request.POST.get('next') or request.GET.get('next') or '/admin/'
    if not url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = '/admin/'
 
    if request.user.is_authenticated:
        return redirect(next_url)
 
    error = None
    warning = False
    username = ''
    remember = False
 
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember = request.POST.get('remember') == 'on'
 
        if not username or not password:
            error = 'Please enter your username and password.'
        else:
            user = authenticate(request, username=username, password=password)
 
            if user is not None:
                if not user.is_staff:
                    error = 'This account does not have access to the admin area.'
                else:
                    login(request, user)
                    if not remember:
                        # session ends when the browser is closed
                        request.session.set_expiry(0)
                    return redirect(next_url)
            else:
                # authenticate() returns None for inactive users too, so check
                # whether this is a correct login on a not-yet-approved account.
                pending = User.objects.filter(username__iexact=username, is_active=False).first()
                if pending and pending.check_password(password):
                    error = 'Your account is still waiting for approval by a NACOS admin.'
                    warning = True
                else:
                    error = 'Invalid username or password.'
 
    context = {
        'error': error,
        'warning': warning,
        'username': username,
        'remember': remember,
        'next': next_url,
    }
    return render(request, 'login.html', context)
 