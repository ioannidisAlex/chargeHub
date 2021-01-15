from django.shortcuts import render, redirect

def home(request):
    return render(request, 'ev_charging_api/api.html')
