from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .models import UserProfile


def home(request):
    return render(
        request,
        "home.html",
        {
            "user": request.user
        }
    )


def register_view(request):

    if request.method == "POST":

        full_name = request.POST.get("full_name")
        age = request.POST.get("age")
        gender = request.POST.get("gender")

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Validation

        if not full_name:
            messages.error(request, "Full Name is required")
            return redirect("register")

        if not age:
            messages.error(request, "Age is required")
            return redirect("register")

        if not gender:
            messages.error(request, "Gender is required")
            return redirect("register")

        if not username:
            messages.error(request, "Username is required")
            return redirect("register")

        if not email:
            messages.error(request, "Email is required")
            return redirect("register")

        if not password:
            messages.error(request, "Password is required")
            return redirect("register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        # Create Django User

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        # Create User Profile

        UserProfile.objects.create(
            user=user,
            full_name=full_name,
            age=age,
            gender=gender
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            messages.error(
                request,
                "Invalid Username or Password"
            )
            return redirect("login")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                "Login Successful"
            )

            return redirect("/")

        messages.error(
            request,
            "Invalid Username or Password"
        )

        return redirect("login")

    return render(
        request,
        "login.html"
    )


def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out"
    )

    return redirect("/")
def about(request):
    return render(request, "about.html")