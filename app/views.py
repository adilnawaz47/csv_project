from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.modules.compare_csv import *
from app.modules.compare_json import *

def home(request):
    return render(request, 'dashboard.html')
