from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import redirect, render

from .forms import PredictionForm
from .models import Prediction
from .ml_model.predictor import predict_performance


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created! You can now log in.")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect("home")
        else:
            messages.error(
                request, "Invalid username or password. Please try again.")
            return redirect("login")
    return render(request, "login.html")


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login")


@login_required
def home(request):
    result = None
    if request.method == "POST":
        form = PredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            grade, level = predict_performance(
                gender=data["gender"],
                ethnicity=data["ethnicity"],
                parental_education=data["parental_education"],
                lunch=data["lunch"],
                test_prep_course=data["test_prep_course"],
                math_score=data["math_score"],
                reading_score=data["reading_score"],
                writing_score=data["writing_score"],
            )
            Prediction.objects.create(
                user=request.user,
                gender=data["gender"],
                ethnicity=data["ethnicity"],
                parental_education=data["parental_education"],
                lunch=data["lunch"],
                test_prep_course=data["test_prep_course"],
                math_score=data["math_score"],
                reading_score=data["reading_score"],
                writing_score=data["writing_score"],
                predicted_grade=grade,
                predicted_level=level,
            )
            result = {
                "grade": grade,
                "level": level,
                "math": data["math_score"],
                "reading": data["reading_score"],
                "writing": data["writing_score"],
            }
    else:
        form = PredictionForm()
    return render(request, "home.html", {"form": form, "result": result})


@login_required
def users_list(request):
    """Admin-only page listing every registered user + their prediction count."""
    if not request.user.is_superuser:
        messages.error(request, "Only admins can view the users list.")
        return redirect("home")
    users = (
        User.objects.annotate(num_predictions=models.Count("predictions"))
        .order_by("-date_joined")
    )
    return render(request, "users.html", {"users": users})


@login_required
def history(request):
    is_admin = request.user.is_superuser
    if is_admin:
        # Admin sees ALL predictions from every user
        predictions = (
            Prediction.objects.select_related("user")
            .order_by("-created_at")
        )
    else:
        # Regular users only see their OWN predictions
        predictions = (
            Prediction.objects.filter(user=request.user)
            .select_related("user")
            .order_by("-created_at")
        )
    return render(request, "history.html", {
        "predictions": predictions,
        "is_admin": is_admin,
    })
