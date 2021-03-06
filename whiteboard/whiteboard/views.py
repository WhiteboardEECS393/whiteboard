from django.shortcuts import render_to_response, render
from django.template import RequestContext
from Profiles.models import StudentUser, Professor
from wb_calendar.models import Calendar
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout
from .forms import LoginForm, CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


def main_redirect(request,):
    return HttpResponseRedirect('/login/')


def login_view(request,):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user is not None:
            if user.is_active:
                login(request, user)
                student = StudentUser.objects.filter(user=user)[0]
                redirect = '/Profiles/' + student.first_name + student.last_name + '/' + str(student.pk) + '/'
                return HttpResponseRedirect(redirect)
            else:
                return HttpResponse('Your User is not active.')
    return render(request, 'Profiles/userloginpage.html', {'login_form': form})


def create_new_user(request,):
    form = CreateUserForm(request.POST or None)
    if request.POST and form.is_valid():
            user = form.create_new_user(request)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    student = StudentUser.objects.filter(user=user)[0]
                    c= Calendar(owner=student, name=student.full_name)
                    c.save();
                    redirect = '/Profiles/' + student.first_name + student.last_name + '/' + str(student.pk) + '/'
                    return HttpResponseRedirect(redirect)
                else:
                    return HttpResponse('Your User is not active.')
    return render(request, 'Profiles/createuser.html', {'create_user_form': form})


def logout_view(request,):
    logout(request)
    return HttpResponseRedirect('../')
