from django.contrib.auth import login, logout,authenticate
from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView
from .form import PhotographerSignUpForm, ViewerSignUpForm
from django.contrib.auth.forms import AuthenticationForm
from .models import User

def index(request):
    return render(request, '../templates/index.html')

def register(request):
    return render(request, '../templates/register.html')

class photographer_register(CreateView):
    model = User
    form_class = PhotographerSignUpForm
    template_name = '../templates/photographer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')

class viewer_register(CreateView):
    model = User
    form_class = ViewerSignUpForm
    template_name = '../templates/viewer_register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/')


def login_request(request):
    if request.method=='POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None :
                login(request,user)
                return redirect('/')
            else:
                messages.error(request,"Invalid username or password")
        else:
                messages.error(request,"Invalid username or password")
    return render(request, '../templates/login.html',context={'form':AuthenticationForm()})

def logout_view(request):
    logout(request)
    return redirect('/')

