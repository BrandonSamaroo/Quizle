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
            UserExtras.objects.create(user = request.user)
            return redirect('/')
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

class TopicCreate(CreateView):
    model = Topic
    fields = '__all__'
    success_url = '/topics/'

def home(request):
    my_following = UserExtras.objects.get(user=request.user.id).followedTopics.all()
    quiz = Quiz.objects.all()
    # quizes = Topic.objects.get.
    return render(request, 'landingpages/home.html', {'my_following': my_following, 'quiz': quiz}) 

def unassoc_topic(request, topic_id, quiz_id):
    Quiz.objects.get(id=quiz_id).topic.remove(topic_id)
    return redirect('', quiz_id=quiz_id)

def search(request):
    return render(request, "main_app/search.html")

def create_quiz(request):
    topics = Topic.objects.all()
    return render(request, "main_app/create_quiz.html", {'topics': topics})

def create_quiz_questions(request):
    num_questions = request.POST['num_questions']
    topic_id = request.POST['topic_id']
    return render(request, "main_app/create_quiz_questions.html", {'range_num_questions': range(int(num_questions)), 'topic_id': topic_id, 'num_questions': num_questions})


def create_quiz_post(request):
    if request.method == 'POST':
        quiz = Quiz.objects.create(name=request.POST['name'], creator=request.user)
        Quiz.objects.get(id=quiz.id).topic.add(request.POST['topic_id'])
        print(request.POST)
        print(request.POST.getlist('question'))
        for i in range(len(request.POST.getlist('question'))):
            answer_number =  request.POST[f'answer{i}']
            Question.objects.create(
                quiz=quiz,
                question=request.POST.getlist('question')[i],
                option1=request.POST.getlist('option1')[i],
                option2=request.POST.getlist('option2')[i],
                option3=request.POST.getlist('option3')[i],
                option4=request.POST.getlist('option4')[i],
                answer=request.POST.getlist(f'option{answer_number}')[i]
            )
    return redirect('/')


