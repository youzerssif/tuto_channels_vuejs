from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from django.utils.safestring import mark_safe
# Create your views here.




def home(request):

    data={}
    return render(request, 'home.html',data)

def chat(request):

    data={}
    return render(request, 'chats.html',data)

def loginpage(request):
    
    data={}
    return render(request, 'login.html',data)

@login_required
def room(request, room_name):
    
    data={
        'room_name': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.user.username)),
    }
    return render(request, 'chat.html',data)




def connexion(request):
    
    postdata = json.loads(request.body.decode('utf-8'))

    username = postdata['username']
    password = postdata['password']
    isSuccess=False

    user = authenticate(username=username, password=password)
    print(user)
    if user is not None and user.is_active :
        print("user is login")
        isSuccess = True
        login(request, user)
        datas = {
        'success':True,
        'username':username,
        'message':'Votre connection a reussi avec succes',
    }
        return JsonResponse(datas,safe=False) # page si connect
        
    else:
        data = {
        'success':False,
        'message':'Vos identifiants ne sont pas correcte',
        }
        return JsonResponse(data,safe=False)
    
    
    
    return JsonResponse(datas, safe=False)
    
    
    
    return JsonResponse(datas, safe=False)


def deconnexion(request):
    logout(request)
    return redirect('channel_app:home')
    