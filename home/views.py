from django.shortcuts import render,redirect
from .models import todo
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login")
def home(request):
    if request.method == "POST":
        data = request.POST

        title = data.get('title')
        description = data.get('description')
        user = request.user

        print(title)
        print(description)

        if not title:
            messages.error(request,"Please Enter Title")
            return redirect("/todo")
        
        item = todo.objects.create(
            title = title,
            description = description,
            status = "In progress",
            user = user
        )

        print(item)
        messages.success(request,"Item successfully added.")

        return redirect("/todo")

    return render(request,"home.html")


@login_required(login_url="/login")
def delete_item(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.delete()

    return redirect('/todo/all_todos')


@login_required(login_url="/login")
def update_status_to_finish(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.status = "Finished"
    item.save()

    return redirect('/todo/all_todos')


@login_required(login_url="/login")
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
        email = user_data.get('email')

        # Checking if username exists
        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(  request,"Username already exists")
            return redirect("/register")

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username,
            email = email,
        )

        user.set_password(password)

        user.save()

        messages.info(request,"Account Created successfully")

        return redirect("/register")


    return render(request,"register.html")


@login_required(login_url="/login")
def show_all_todos(request):
    allTODO = todo.objects.filter(user = request.user)
    context = {
        "items" : allTODO
    }
    return render(request,"all_todos.html",context)


@login_required(login_url="/login")
def profile(request):
    return render(request,"profile.html")


@login_required(login_url="/login")
def update_todo(request,id):
    item = todo.objects.get(id= id)
    context = {
        "item" : item
    }

    if request.method == "POST":
        data = request.POST
        title = data.get('title')
        description = data.get('description')

        item.description = description
        item.title = title

        item.save()

        messages.info(request,"Update successfully")

        return render(request,"update_todo.html",context)

    return render(request,"update_todo.html",context)


def forget_password(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username = username)

        if not user:
            messages.info(request,"User does not exists")
            return redirect("/forget-password")
        
        else:
            user = user[0]
            user.set_password(password)
        
            user.save()

            messages.success(request,"Password successfully reset.")
            # return redirect("/login")


    return render(request,"forget_password.html")