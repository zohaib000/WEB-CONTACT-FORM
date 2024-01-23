from django.http.response import HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from django.http import JsonResponse
from .models import *
from django.http import JsonResponse
import time
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import requests
import base64
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def signup(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        password = request.POST["password"]

        # Create a new user with additional information
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        return redirect("login")
    else:
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "home/signup.html")

    return render(request, "home/signup.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  # Replace 'dashboard' with your desired URL
    else:
        if request.user.is_authenticated:
            return redirect("home")
        return render(request, "home/login.html")

    return render(request, "home/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def profile(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            user_profile = User.objects.get(username=request.user)

            context = {
                "first_name": user_profile.first_name,
                "last_name": user_profile.last_name,
            }

            return render(request, "home/profile.html", context)
        else:
            return redirect("login")


class home(View):
    def post(self, request):
        date = request.POST.get("date")
        ID = request.POST.get("ID")
        customer = request.POST.get("customer")
        job = request.POST.get("job")
        contractor = request.POST.get("contractor")
        timeIn = request.POST.get("timeIn")
        timeOut = request.POST.get("timeOut")
        totalTime = request.POST.get("totalTime")
        jobDescription = request.POST.get("jobDescription")
        whatWasCompleted = request.POST.get("whatWasCompleted")
        stillNeedsCompleted = request.POST.get("stillNeedsCompleted")
        notes = request.POST.get("notes")
        uploaded_images = request.FILES.getlist("uploaded_images")
        signature = request.POST.get("signature_data")

        # getting signature image from base64 encoded data
        _, data = signature.split(";base64,")
        binary_data = base64.b64decode(data)
        filename = f"Signatures/signature_{customer}.png"
        with open(f"media/{filename}", "wb") as f:
            f.write(binary_data)

        # creating object and saving data
        form_data = FormData.objects.create(
            date=date,
            WO_ID=ID,
            customer=customer,
            job=job,
            contractor=contractor,
            inTime=timeIn,
            outTime=timeOut,
            totalTime=totalTime,
            job_description=jobDescription,
            waht_was_completed=whatWasCompleted,
            still_needs_completed=stillNeedsCompleted,
            issues=notes,
            signature=filename,
        )

        # Add uploaded images to FormData
        for image in uploaded_images:
            form_data.add_uploaded_image(image)

        return render(
            request,
            "home/index.html",
            {"message": "Your Data is submitted successfully!"},
        )

    def get(self, request):
        return render(request, "home/index.html")
