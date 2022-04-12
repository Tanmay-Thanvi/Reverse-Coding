from datetime import datetime, timedelta
import json
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import auth, User
from quiz.models import userlist, question
import random
from .models import Profile
from quiz.views import listtotext
import re
import requests
from quiz.views import instructions


# Create your views here.
def login(request):
    # if request.user.is_authenticated:
    #     redirect(instructions)        
    # else:
    #     messages.error(request,'Not going to instructions page')    
    #   it is a debugging code to understand that back button cannot be handle through backend
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        # Check User API
        # payload = {
        #     "username": username,
        #     "password": password,
        #     "event": "Reverse Coding"
        # }
        # headers = {'Content-type' : 'application/json'}
        # print(payload)
        # payload_json_data = json.dumps(payload)
        # user = requests.post("http://backend.credenz.in/api/check_user/", headers = headers, data=payload_json_data)
        # print(user)
        # if user.status_code == 200:
        #     response = user.json()
        #     print(response)
        #     # User.objects.create(username=username, password=password)
        # else:
        #     print("User Does not Exist")
        #     return

        if User.objects.filter(username=username).exists():
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # print(0)
                auth.login(request, user)
                # print(1)
                # print(user.is_staff)
                if user.is_staff == False:
                    # print(2)
                    if not (Profile.objects.filter(user=user).exists()):
                        profile = Profile.objects.create(user=user)
                        profile.save()
                    P = Profile.objects.get(user=user)
                    if P.has_started == False:
                        # print(3)
                        # Add Userlist elements here
                        c = question.objects.all()
                        # print(c)
                        li = list(range(1, len(c) + 1))
                        random.shuffle(li)
                        l = listtotext(li)
                        ul = userlist.objects.create(user=user, unattemptedlist=l)
                        ul.save()
                    # print(4)
                return redirect(instructions)
            else:
                messages.error(request, "Invalid Credentials")
                return render(request, 'login.html', {'title': 'Login'})
        else:
            messages.error(request, "User does not exist")
            return render(request, 'login.html', {'title': 'Login'})
    else:
        return render(request, 'login.html', {'title': 'Login'})


def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        regexusername = "^[[A-Z]|[a-z]][[A-Z]|[a-z]|\\d|[_]]{7,29}$"
        regexemail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        regexpassword = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        if not re.search(regexusername, username):
            messages.warning(request, 'Invalid username.')
            return render(request, 'register.html', {'title': 'Register'})
        if not re.search(regexemail, email):
            messages.warning(request, 'Invalid E-mail address.')
            return render(request, 'register.html', {'title': 'Register'})
        if not re.search(regexpassword, password):
            messages.error(request,
                           "The password must contain at least 8 characters,1 uppercase character,1 speacial character and a number.")
            return render(request, 'register.html', {'title': 'register'})
        if not str(fname).isalpha():
            messages.warning(request, 'First name is not valid')
            return render(request, 'register.html', {'title': 'Register'})
        if not str(lname).isalpha():
            messages.warning(request, 'Lastname is not valid.')
            return render(request, 'register.html', {'title': 'Register'})
        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already taken')
                return render(request, 'register.html', {'title': 'Register'})
            else:
                user = User.objects.create_user(username=username, password=password, email=email, first_name=fname,
                                                last_name=lname)
                user.save()
                messages.success(request, 'Sign-up successful. You can login now')
                return redirect(login)
        else:
            messages.warning(request, 'Password do not Match')
            return render(request, 'register.html', {'title': 'Register'})
    else:
        return render(request, 'register.html', {'title': 'Register'})


def check(request):
    name = request.POST['username']
    user = User.objects.filter(username=name)
    if user.exists():
        m = "Username ' " + name + " ' already exist. You cannot use it. Status : ❌"
    else:
        m = "Username ' " + name + " ' do not exist. You can use it. Status : ✅"
    messages.info(request, m)
    return redirect(register)


def logout(request):
    auth.logout(request)
    return redirect('/')


def leaderboard(request):
    users = User.objects.all()
    profile = Profile.objects.all().order_by('-score', 'Timetaken')
    # print(profile)
    return render(request, 'leaderboard.html', {'users': users, 'profile': profile})
