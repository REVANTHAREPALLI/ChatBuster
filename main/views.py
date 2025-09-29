from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic, Message
from .forms import FormRoom
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


# dicto = [
#     {'id':1, 'name':'python'},
#     {'id':2, 'name':'java'},
#     {'id':3, 'name':'C'},
# ]

# Create your views here.

'''def home(request):
    return render(request,'main/home.html',{'room':dicto})

def room(request, n):
    room = []
    for i in dicto:
        if i['id'] == int(n):
            room.append(i['id'])
            room.append(i['name'])
            break
    return render(request,'main/room.html',{'room':room})'''

def home(request):
    q = request.GET.get('q') if request.GET.get('q')!= None else ''
    # room = Room.objects.filter(topic__name__icontains=q) for filtering search by topic only
    room = Room.objects.filter(        #this can serach by topic/name/description
                            Q(topic__name__icontains=q) |
                            Q(name__icontains=q) |
                            Q(description__icontains=q)
                            )
    room2 = Room.objects.all()
    room_count = room.count()
    topics = Topic.objects.all()
    count = []
    for i in topics:
        count.append(i.room_set.all().count())
    context = {'rooms':room, 'room_count':room_count, 'query':q,'topics_count':zip(topics,count),'total':sum(count)}
    return render( request, 'main/home.html', context)

def room(request, n):
    room = Room.objects.get(id=n)
    room_message = room.message_set.all().order_by('-created')  #one-many relationship
    participants = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
        user = request.user,
        room = room,
        body = request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', n=room.id)
    print(participants)
    context = {'room':room, 'room_message':room_message, 'participants':participants}
    return render(request,'main/room.html', context)

@login_required(login_url="login")
def createRoom(request):
    form = FormRoom()
    if request.method == 'POST':
        form = FormRoom(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'main/room_form.html',context)

@login_required(login_url="login")
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = FormRoom(instance=room)

    if request.user != room.host:
        return HttpResponse("Sorry!<br>" \
        "<h1>You are not allowed to edit, as you are not host of this room" \
        ":(</h1>")
    if request.method == 'POST':
        form = FormRoom(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'main/room_form.html',context)

@login_required(login_url="login")
def deleteRoom(request,pk):
    q="room"
    form = Room.objects.get(id=pk)
    if request.method == 'POST':
        form.delete()
        return redirect('home')
    context = {'nm': form,'q':q}
    return render(request,'main/delete_room.html', context)

def loginPage(request):
    q = "login"
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('un').lower()
        password = request.POST.get('pw')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "User credentials are incorrect")
    context = {"task":q}
    return render(request,'main/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request,"An error occured while registering") 
    context = {'form':form}
    return render(request,'main/login_register.html',context)

@login_required(login_url="login")
def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    context = {'obj': message}
    return render(request,'main/delete_room.html', context)