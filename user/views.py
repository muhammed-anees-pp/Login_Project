from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.db.models import Q
import re


# Create your views here.
@never_cache
@login_required(login_url='login')
def home_page(request):
    
    return render (request,'home.html')


@never_cache
def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home') 

    error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        
        if password1 != password2:
            response_html = '<html><body><p style="color:red;">Your passwords do not match!</p></body></html>'
            return HttpResponse(response_html)

        
        if User.objects.filter(username=username).exists():
            response_html = '<html><body><p style="color:red;">Username already exists!</p></body></html>'
            return HttpResponse(response_html)

        if User.objects.filter(email=email).exists():
            response_html = '<html><body><p style="color:red;">Email already exists!</p></body></html>'
            return HttpResponse(response_html)
        
        if not re.match(r'^(?=.*\d)[^\s]{6,}$', username):
            
            error = "Need 6 characters including numbers, no spaces!"
        
        if not error:

            my_user = User.objects.create_user(username, email, password1)
            my_user.save()
            return redirect('login')


    return render(request, 'signup.html', {'message': error})

@never_cache
def login_page(request):
    if request.user.is_authenticated:
        # Redirect based on user type
        if request.user.is_superuser:
            return redirect('admin_panel')
        else:
            return redirect('home')

    error = ""
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=password1)

        if user is not None:
            login(request, user)
            # Redirect admin to admin panel and other users to home page
            if user.is_superuser:
                return redirect('admin_panel')
            else:
                return redirect('home')
        else:
            error = "Incorrect username or password"

    return render(request, 'login.html', {'message': error})

@never_cache
def logout_page(request):
    if request.user.is_authenticated:
        if request.POST:
            logout(request)
            return redirect('login')
        return redirect('home')
    return redirect('login')

# Admin panal to list users, add, edit, and delete
@never_cache
@login_required(login_url='login')
def admin_panel(request):
    if request.user.is_superuser:
        # Get the search query from the request
        search_query = request.GET.get('search', '')

        # Filter users based on the search query (username or email)
        if search_query:
            users = User.objects.filter(
                Q(username__icontains=search_query) | Q(email__icontains=search_query)
            )  # Case-insensitive search
        else:
            users = User.objects.exclude(is_superuser=True)

        return render(request, 'admin_panel.html', {'users': users, 'search_query': search_query})
    else:
        return HttpResponse("<h3>You are not authorized to view this page.</h3>")

# add new user
@never_cache
@login_required(login_url='login')
def add_user(request):
    if request.user.is_superuser:
        error = ""
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            if User.objects.filter(username=username).exists():
                error = "Username already exists!"

            elif not re.match(r'^(?=.*\d)[^\s]{6,}$', username):
                error = "Need 6 characters including numbers, no spaces!"
        

            elif User.objects.filter(email=email).exists():
                error = "Email already exists!"

            elif len(password) < 5:
                error = "Password should be 5 characters"

            else:
                User.objects.create_user(username=username, email=email, password=password)
                return redirect('admin_panel')

        return render(request, 'add_user.html', {'message': error})
    else:
        return HttpResponse("<h3>You are not authorized to view this page.</h3>")
    

@never_cache
@login_required(login_url='login')
def edit_user(request, user_id):
    if request.user.is_superuser:
        user = get_object_or_404(User, id=user_id)
        error = ""

        if request.method == 'POST':
            new_username = request.POST.get('username')
            new_email = request.POST.get('email')
            password = request.POST.get('password')

            # Check if the username already exists (excluding current user)
            if User.objects.filter(username=new_username).exclude(id=user_id).exists():
                error = "Username already taken."
                
            # Check if the email already exists (excluding current user)
            elif User.objects.filter(email=new_email).exclude(id=user_id).exists():
                error = "Email already taken."

            elif not re.match(r'^(?=.*\d)[^\s]{6,}$', new_username):
                error = "Need 6 characters including numbers, no spaces!"

            elif len(password) < 5:
                error = "Password should be 5 int/characters"

            # Only save if there are no errors
            if not error:
                user.username = new_username
                user.email = new_email

                if password:
                    user.set_password(password)

                user.save()
                return redirect('admin_panel')

        # Render the template with the error message if it exists
        return render(request, 'edit_user.html', {
            'user': user,
            'message': error,
        })
    else:
        return HttpResponse("<h3>You are not authorized to view this page.</h3>")



# deleting the user
@never_cache
@login_required(login_url='login')
def delete_user(request):
    if request.user.is_superuser:
        user_id = request.POST.get('id')
        print(user_id)
        user = get_object_or_404(User, id=user_id)
        print(user)
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('admin_panel')
    else:
        return HttpResponse("<h3>You are not authorized to view this page.</h3>")