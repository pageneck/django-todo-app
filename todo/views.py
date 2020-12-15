from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def signuppage(request):
  if request.method == 'GET':
    return render(request, 'todo/signuppage.html', {'form' : UserCreationForm()})
  else:
    try:
      if request.POST['password1'] == request.POST['password2']:
        user = User.objects.create_user(request.POST['username'], password = request.POST['password1'])
        user.save()
        login(request, user)
        return redirect('currenttodos')
    except IntegrityError:
      return render(request, 'todo/signuppage.html', {'form' : UserCreationForm(), 'error': 'Username already exist, find another username that is not taken'})
   
    else:
      # tell the user the passwords do not match
      return render(request, 'todo/signuppage.html', {'form' : UserCreationForm(), 'error': 'Passwords does not match'})

@login_required
def currenttodos(request):
  todos = Todo.objects.filter(user = request.user, datecompleted__isnull=True)
  return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def logout_request(request):
  if request.method == 'POST':
    logout(request)
    return redirect('home')

def home(request):
  return render(request, 'todo/home.html')


def loginuser(request):
  if request.method == 'GET':
    return render(request, 'todo/loginuser.html', {'form' : AuthenticationForm()})
  else:
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('currenttodos')
    else:
      return render(request, 'todo/loginuser.html', {'form' : AuthenticationForm(), 'error': 'Username and password do not match'})

@login_required
def createtodo(request):
  if request.method == 'GET':
    return render(request, 'todo/createtodo.html', {'form' : TodoForm()})
  else:
    try:
      form = TodoForm(request.POST)
      newtodo = form.save(commit=False)
      newtodo.user = request.user
      newtodo.save()
      return redirect('createtodo')
    except ValueError:
      return render(request, 'todo/createtodo.html', {'form' : TodoForm(), 'error':'Bad data entered. Try again'})

@login_required
def viewstodo(request, todo_pk):

  todo  = get_object_or_404(Todo, pk=todo_pk, user=request.user)
  if request.method == 'GET':
    form = TodoForm(instance=todo)
    return render(request, 'todo/viewtodos.html', {'todo':todo, 'form':form})
  else:
    form = TodoForm(request.POST,instance=todo)
    form.save()
    return redirect('currenttodos')

@login_required
def completedtodo(request, todo_pk):
    todo  = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
      todo.datecompleted = timezone.now()
      todo.save()
      return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo  = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
      todo.delete()
      return redirect('currenttodos')

@login_required
def completed(request):
  todos = Todo.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
  return render(request, 'todo/completed.html', {'todos':todos})

