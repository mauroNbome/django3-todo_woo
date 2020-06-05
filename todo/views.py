from django.shortcuts import render, redirect, get_object_or_404 #useful to redirect users to other page, get_object_or_404 is to grab certain objects
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm # The first is to registrer, the second login.
from django.contrib.auth.models import User # By importing this we have access to the user models.
from django.db import IntegrityError # import to display the error properly.
from django.contrib.auth import login, logout, authenticate # Authenticate is used to assign data to a User (username, password).
from .forms import TodoForm # Importing the form to create Todo.
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required



#-------------------------------------------------------AUTH-------------------------------------------------------------------------
def signupuser(request):
    if request.method == 'GET': #every time you click on the url the web use GET to display info, displays an empty form.
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            # Create a new user (by clicking submit).
            try:
                user = User.objects.create_user(request.POST['username'],password = request.POST['password1'])
                user.save() # This save the user in the DB.
                login(request, user) # Auto-loggin the new user in the page.
                # we have to redirec the user somewhere:
                return redirect('currenttodos')
            except IntegrityError: # This error shows up because the user is already taken, you can see it in the "Exception type".
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken. Please choose a new one'})

        else:# Tell the user the password didn't match
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Password did not match'})


def loginuser(request):
    if request.method == 'GET': #every time you click on the url the web use GET to display info, displays an empty form.
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None: # If the user isn't correct, user becomes None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            login(request, user) # Auto-loggin the new user in the page.
            return redirect('currenttodos')
       

@login_required # DECORATOR
def logoutuser(request):
    if request.method == 'POST': # We only allow someone logout IF it's a post request. Otherwise chrome's gonna kick us all the time.
        logout(request)
        return redirect('home')


#------------------------------------------------------------TODOS-------------------------------------------------------------------------

def home(request):
    return render(request, 'todo/home.html')


@login_required # DECORATOR
def createtodo(request):
        if request.method == 'GET': #every time you click on the url the web use GET to display info, displays an empty form.
            return render(request, 'todo/createtodo.html', {'form':TodoForm()})
        else: # request.POST method...
            try:
                form = TodoForm(request.POST)
                newtodo = form.save(commit=False) # This save the form's data without commit to the DB.
                newtodo.user = request.user # Adding the current user field to the object.
                newtodo.save() # The saving it.
                return redirect('currenttodos')
            except ValueError:
                return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'The maxlenght is 100 chars!'})


@login_required # DECORATOR
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True) # Displaying objects that only belongs to the user, only if datecompleted is null.
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required # DECORATOR
def completedtodos(request):
        todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted') # The list is ordered by the completed date!
        return render(request, 'todo/completedtodos.html', {'todos': todos})



@login_required # DECORATOR
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user) # Last parameter is a restriction, if you're not the user who created it returns a 404.
    if request.method == 'GET':
        form = TodoForm(instance=todo) # Here we're instanciating the form we've created with the specific object.
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form}) # Adding the object and the form to the context.
    else:
        try:
            # Here it's necesary to instanciate the current object too. It'll help us now that this is an existing object tha we're trying to do an update.
            form = TodoForm(request.POST, instance=todo) 
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad info'})


@login_required # DECORATOR
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required # DECORATOR
def deletetodo(request, todo_pk): # This function doesn't require a template, it's a functionality of the site.
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
