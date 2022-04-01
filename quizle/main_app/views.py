from pyexpat import model
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Topic,Quiz,Score,Question, UserExtras
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
def home(request):
    return render(request, 'landingpages/home.html')

class Profile(DetailView):
    model = User

class Topics(ListView):
    model = Topic

def search(request):
    return render(request, "main_app/search.html")

def create_quiz(request):
    return render(request, "main_app/create_quiz.html")
