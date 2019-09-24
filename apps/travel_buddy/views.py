from django.shortcuts import render, redirect, HttpResponse
from apps.login_app.models import *
from django.contrib import messages
from datetime import datetime


def dashboard_page(request):
    if request.session['user_first_name'] != '':
        loggedin_users_list = User.objects.filter(
            email=request.session['user_email'])
        loggedin_user = loggedin_users_list[0]
        all_trips = Trip.objects.all()

        context = {
            "loggedin_user": loggedin_user,
            "all_trips": all_trips,
        }

        return render(request, "travel_buddy/dashboard.html", context)
    else:
        return redirect('/')


def new_trip_page(request):
    date_rn = datetime.today()
    date_rn = date_rn.strftime('%Y-%m-%d')

    context = {
        "date_rn": date_rn,
    }

    return render(request, "travel_buddy/new_trip_page.html", context)


def view_trip_page(request, id):
    trip_id = int(id)
    specific_trips_list = Trip.objects.filter(id=trip_id)
    specific_trip = specific_trips_list[0]
    start_date = specific_trip.start_date.strftime('%m/%d/%Y')
    end_date = specific_trip.end_date.strftime('%m/%d/%Y')
    created_at = specific_trip.created_at.strftime('%m/%d/%Y')
    updated_at = specific_trip.updated_at.strftime('%m/%d/%Y')
    list_of_joined_users = []

    if len(specific_trip.user_trip.all()) > 0:
        for user in specific_trip.user_trip.all():
            list_of_joined_users.append(user.first_name)
    else:
        list_of_joined_users.append('None')

    context = {
        "specific_trip": specific_trip,
        "start_date": start_date,
        "end_date": end_date,
        "created_at": created_at,
        "updated_at": updated_at,
        "list_of_joined_users": list_of_joined_users,
    }

    return render(request, "travel_buddy/view_trip_page.html", context)


def action_new_trip(request):
    errors = Trip.objects.basic_validator_trip(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        return redirect('/trips/new')
    else:
        loggedin_users_list = User.objects.filter(
            email=request.session['user_email'])
        this_trip = Trip.objects.create(destination=request.POST["input_destination"],
                                        start_date=request.POST["input_start_date"], end_date=request.POST["input_end_date"],
                                        plan=request.POST["input_plan"], created_by=loggedin_users_list[0].first_name)
        loggedin_users_list[0].trip.add(this_trip)
        # this_trip.user_trip.add(loggedin_users_list[0])

        return redirect('/dashboard')


def action_remove_trip(request, id):
    loggedin_users_list = User.objects.filter(
        email=request.session['user_email'])
    trip_id = int(id)
    specific_trip = Trip.objects.get(id=trip_id)
    loggedin_users_list[0].trip.remove(specific_trip)
    specific_trip.delete()
    return redirect('/dashboard')


def edit_trip_page(request, id):
    trip_id = int(id)
    specific_trip = Trip.objects.get(id=trip_id)
    start_date = specific_trip.start_date.strftime('%Y-%m-%d')
    end_date = specific_trip.end_date.strftime('%Y-%m-%d')

    date_rn = datetime.today()
    date_rn = date_rn.strftime('%Y-%m-%d')

    context = {
        "specific_trip": specific_trip,
        "start_date": start_date,
        "end_date": end_date,
        "date_rn": date_rn,
    }

    return render(request, "travel_buddy/edit_trip_page.html", context)


def action_edit_trip(request, id):
    errors = Trip.objects.basic_validator_trip(request.POST)
    loggedin_users_list = User.objects.filter(
        email=request.session['user_email'])
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/edit/' + str(id))
    else:
        date_rn = datetime.today()
        trip_id = int(id)
        trip = Trip.objects.get(id=trip_id)
        loggedin_users_list[0].trip.remove(trip)
        trip.destination = request.POST["input_destination"]
        trip.start_date = request.POST["input_start_date"]
        trip.end_date = request.POST["input_end_date"]
        trip.plan = request.POST["input_plan"]
        trip.updated_at = date_rn
        trip.save()
        loggedin_users_list[0].trip.add(trip)

        return redirect('/dashboard')


def action_join_trip(request, id):
    loggedin_users_list = User.objects.filter(
        email=request.session['user_email'])
    trip_id = int(id)
    this_trip_list = Trip.objects.filter(id=trip_id)
    this_trip = this_trip_list[0]
    loggedin_users_list[0].trip.add(this_trip)
    this_trip.user_trip.add(loggedin_users_list[0])

    return redirect("/dashboard")


def action_cancel(request, id):
    loggedin_users_list = User.objects.filter(
        email=request.session['user_email'])
    trip_id = int(id)
    this_trip = Trip.objects.get(id=trip_id)
    loggedin_users_list[0].trip.remove(this_trip)
    this_trip.user_trip.remove(loggedin_users_list[0])

    return redirect("/dashboard")
