from .decorators import login_required
import bcrypt
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Trip, User

@login_required
def index(request):
    return redirect("/travels")

@login_required
def travels(request):
    context = {
        "all_the_travels": Trip.objects.all(),
    }
    return render(request, "travels.html", context)

@login_required
def add_travel(request):
    context = {
        "all_the_travels": Trip.objects.all()
    }
    return render(request, "add_travel.html", context)

@login_required
def create_travel(request):
    errors = Trip.objects.trip_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/travels/new")
    try:
        create = Trip.objects.create(
            destination = request.POST["destination"], 
            start_date = request.POST["start_date"], 
            end_date = request.POST["end_date"], 
            plan = request.POST["plan"])
        trip_id = create.id
    except IntegrityError:
           messages.error(request, "Este viaje ya existe")
           return redirect("/travels/new")
    messages.success(request, "El viaje ha sido creado exitosamente")
    return redirect(f"/travels/{trip_id}")

@login_required
def view_travel(request, trip_id):
    this_travel = Trip.objects.get(id=trip_id)
    context = {
        "a_travel": this_travel
    }
    return render(request, "view_travel.html", context)

@login_required
def delete_travel(request, trip_id):
    if request.method != "POST":
        return redirect("/")
    if request.method == "POST":
        a_travel = Trip.objects.get(id=trip_id)
        a_travel.delete()
    return redirect("/travels")