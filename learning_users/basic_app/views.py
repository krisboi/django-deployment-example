from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

# Tambahan import
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    dataContext={'title':'Home'}
    return render(request, 'basic_app/index.html', dataContext)

@login_required
def special(request):
    return HttpResponse("You are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):

    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']
            
            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    dataContext={'title':'Registration', 'user_form':user_form,'profile_form':profile_form, 'registered':registered}

    return render(request, 'basic_app/register.html',dataContext)

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username, password = password)

        # jika user lolos otentifikasi       
        if user:
            # jika user aktif
            if user.is_active:
                # user berhasil login dan arahkan ke halaman index
                login(request,user)
                return HttpResponseRedirect(reverse('special'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and the password: {}".format(username,password)) 
            return HttpResponse ("Invalid login detailed supplied!!")
    else:
        return render(request, 'basic_app/login.html')       

