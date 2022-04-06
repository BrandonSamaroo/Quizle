from pyexpat import model
import re
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

@login_required
def profile(request, user_id):
    user = User.objects.get(id=user_id)
    scores = Score.objects.filter(user=user_id)
    quizes_id = scores.values('quiz_id').distinct()
    quizes = []
    for quiz in quizes_id:
        quizes.append(Quiz.objects.get(id=quiz['quiz_id']))
    createdquizes = Quiz.objects.filter(creator=user_id)
    return render(request, 'main_app/profile_view.html', {'thisuser': user, 'quizes': quizes, 'createdquizes': createdquizes}) 
    

class Topics(LoginRequiredMixin, ListView):
    model = Topic

class TopicCreate(LoginRequiredMixin, CreateView):
    model = Topic
    fields = '__all__'
    success_url = '/topics/'

class Profile(DetailView):
    model = User

@login_required
def home(request):
    my_following = UserExtras.objects.get(user=request.user.id).followedTopics.all()
    quiz = Quiz.objects.all()
    # quizes = Topic.objects.get.
    return render(request, 'landingpages/home.html', {'my_following': my_following, 'quiz': quiz}) 

@login_required
def unassoc_topic(request, topic_id):
    UserExtras.objects.get(user=request.user).followedTopics.remove(topic_id)
    return redirect('home')


@login_required
def search(request):
    return render(request, "main_app/search.html")

def create_quiz(request):
    topics = Topic.objects.all()
    return render(request, "main_app/create_quiz.html", {'topics': topics})

@login_required
def create_quiz_questions(request):
    num_questions = request.POST['num_questions']
    topic_id = request.POST['topic_id']
    return render(request, "main_app/create_quiz_questions.html", {'range_num_questions': range(int(num_questions)), 'topic_id': topic_id, 'num_questions': num_questions})


@login_required
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


@login_required
def play_quiz(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    questions = Question.objects.filter(quiz=quiz_id)
    print(questions)
    return render(request, "main_app/play_quiz.html", {'quiz': quiz, 'questions': questions})


@login_required
def play_quiz_post(request, quiz_id):
    score = 0 
    qanda = []
    
    for count, answer in enumerate(request.POST.getlist('answers')):
        question = Question.objects.get(quiz=quiz_id, answer=answer)
        isCorrect = False
        if request.POST[f'guess{count}'] == answer:
            score+=1
            isCorrect = True
        qanda.append({'question': question.question, 'correctanswer': answer, 'givenanswer': request.POST[f'guess{count}'], 'isCorrect': isCorrect})
    print(qanda)
    quiz = Quiz.objects.get(id=quiz_id)
    score = Score.objects.create(score=score, user=request.user, quiz=quiz)
    total = len(request.POST.getlist('answers'))
    return render(request, "main_app/post_quiz.html", {'qanda': qanda, 'score': score, 'total': total})


@login_required
def view_score(request, quiz_id, user_id):
    scores = Score.objects.filter(quiz=quiz_id, user=user_id)
    return render(request, "main_app/quiz_score.html", {'scores': scores})

@login_required
def profile_edit(request):
    return render(request, "main_app/profile_edit.html")


@login_required
def profile_edit_post(request):
    userextras = UserExtras.objects.get(user=request.user.id)
    if request.FILES:
        userextras.profilePic = request.FILES['img']
        userextras.save()
    if request.POST['first_name'] != '' or request.user.first_name:
        request.user.first_name =  request.POST['first_name']
        request.user.save()
    if request.POST['last_name'] != '' or request.user.first_name:
        request.user.last_name =  request.POST['last_name']
        request.user.save()
    return redirect(f"/accounts/profile/{request.user.id}")
