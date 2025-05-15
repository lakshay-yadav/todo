from django.shortcuts import render,redirect
from .models import todo,PasswordResetOTP
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import random

# Create your views here.
@login_required(login_url="/login")
def home(request):
    if request.method == "POST":
        data = request.POST

        title = data.get('title').strip()
        description = data.get('description').strip()
        user = request.user

        if len(description) == 0:
            description = "Default description(Please add description)"

        print(title)
        print(len(description))

        if not title:
            messages.error(request,"Please Enter Title")
            return redirect("/todo")
        
        item = todo.objects.create(
            title = title,
            description = description,
            status = "In Progress",
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
    context = {
        "user" : request.user,
    }
    return render(request,"profile.html",context)


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

        user = User.objects.filter(username = username)

        if not user:
            messages.info(request,"User does not exists")
            return redirect("/forget-password")
        
        else:
            try:
                user = user[0]
                email = user.email
                first_name = user.first_name

                otp = str(random.randint(100000, 999999))
                print("OTP ->",otp)

                PasswordResetOTP.objects.create(user=user, otp=otp)

                send_mail(
                    subject='OTP for Password Reset',
                    message=f'Hi {first_name},\nYour OTP to reset the password on To-Do app : {otp}\nThanks for choosing us',
                    from_email='lakshaybalwan@gmail.com',
                    recipient_list=[email],
                )

                return redirect(f"/forget-password/{username}")
            
            except Exception as e:
                print(e)
                messages.info(request,"Some error occured! Please try again")
                return render(request,"forget_password.html")       

    return render(request,"forget_password.html")


def forget_password_authenticate(request,username):
    if request.method == "POST":
        data = request.POST
        otp = data.get('otp')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        if password != confirm_password:
            messages.error(request,"Password and confirm password does not match")
            return render(request,"forget_password_authenticate.html")
        
        user = User.objects.filter(username = username)
        user = user[0]

        if not PasswordResetOTP.objects.filter(user = user).exists():
            messages.info(request,"Did not able to get the OTP. Kindly start from the beginning.")
            return redirect("/forget-password")
        
        original_otp = PasswordResetOTP.objects.filter(user = user)

        original_otp = original_otp[0]

        otp_from_db = int(original_otp.otp)
        otp = int(otp)

        if otp_from_db != otp:
            messages.info(request,"Wrong OTP. Please try again")
            return render(request,"forget_password_authenticate.html")

        user.set_password(password)
        user.save()

        original_otp.delete()

        messages.info(request,"Password reset done. Please login")
        return redirect("/login")

    return render(request,"forget_password_authenticate.html")


@login_required(login_url="/login")
def policy(request):
    return render(request,"policy.html")


@login_required(login_url="/login")
def delete_account(request,username):
    user = request.user
    user.delete()

    messages.info(request,"Successfully deleted account")
    return redirect("/login")


@login_required(login_url="/login")
def update_account(request,username):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        user = request.user

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        messages.info(request,"Profile updated successfully.")
        return redirect("/profile")

    return render(request,"update_account.html")
