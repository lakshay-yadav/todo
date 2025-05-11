from django.shortcuts import render,redirect
from .models import todo
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login")
def home(request):
    allTODO = todo.objects.all()
    context = {
        "items" : allTODO
    }

    if request.method == "POST":
        data = request.POST

        title = data.get('title')
        description = data.get('description')

        print(title)
        print(description)
        item = todo.objects.create(
            title = title,
            description = description,
            status = "In progress"
        )

        print(item)

        return redirect("/todo")

    return render(request,"home.html",context)

def delete_item(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.delete()

    return redirect('/todo/all_todos')

def update_status_to_finish(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.status = "Finished"
    item.save()

    return redirect('/todo/all_todos')

def update_status_to_progress(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.status = "In Progress"
    item.save()

    return redirect('/todo/all_todos')


def login_page(request):
    if request.method == "POST":
        # Getting data from the request
        user_data = request.POST

        # Assigning data to each variable
        username = user_data.get('username')
        password = user_data.get('password')

        user = authenticate(username = username,password = password)

        if not user:
            messages.error(request,"Invalid username or password")
            return redirect("/login")
        
        else:
            login(request,user)
            return redirect("/todo")
        
    return render(request,"login.html")


def logout_page(request):
    logout(request)
    return redirect("/login")


def register(request):
    if request.method == "POST":
        # Getting data from the request
        user_data = request.POST

        # Assigning data to each variable
        first_name = user_data.get('first_name')
        last_name = user_data.get('last_name')
        username = user_data.get('username')
        password = user_data.get('password')

        # Checking if username exists
        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(  request,"Username already exists")
            return redirect("/register")

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
        )

        user.set_password(password)

        user.save()

        messages.info(request,"Account Created successfully")

        return redirect("/register")


    return render(request,"register.html")


@login_required(login_url="/login")
def show_all_todos(request):
    allTODO = todo.objects.all()
    context = {
        "items" : allTODO
    }
    return render(request,"all_todos.html",context)

@login_required(login_url="/login")
def profile(request):
    return render(request,"profile.html")