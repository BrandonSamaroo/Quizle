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

# Use @login_required for functions 
# Pass LoginRequiredMixin as a parameter for classes

# Create your views here.

# def form_valid(self, form):
#     form.instance.user = self.request.user
#     return super().form_valid(form)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = "Invalid Signup - Try Again"
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

def home(request):
    return render(request, 'landingpages/home.html')

class Profile(DetailView):
    model = User

class Topics(ListView):
    model = Topic

def search(request):
    return render(request, "main_app/search.html")

def create_quiz(request):
    topics = Topic.objects.all()
    return render(request, "main_app/create_quiz.html", {'topics': topics})
