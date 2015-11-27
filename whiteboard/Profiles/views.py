from django.shortcuts import render_to_response, HttpResponseRedirect, render, HttpResponse
from django.template import RequestContext
from .models import StudentUser, Minor, Major, Professor, Department
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from .forms import EditProfileForm


@login_required
def profile(request, first, last, student_id):
    template = 'Profiles/userprofile.html'
    student_list = StudentUser.objects.filter(pk=student_id)

    if len(student_list) != 1:
        template = 'Profiles/usernotfound.html'
        context = RequestContext(request,)
    else:
        student = student_list[0]
        classes = student.student_classes.all()

        user = StudentUser.objects.filter(user=request.user)[0]
        curr_user_classes = StudentUser.getCurrentClasses(student)
        majors = student.majors.all()
        minors = student.minors.all()

        context = RequestContext(request, {
            'student': student,
            'classes': classes,
            'curr_user': user,
            'curr_user_classes': curr_user_classes,
            'majors': majors,
            'minors': minors,
        })
    return render_to_response(template, locals(), context)

@login_required
def professorProfile(request, first, last):
    template = 'Profiles/professorprofile.html'
    prof=Professor.objects.filter(first_name=first, last_name=last)

    if len(prof) != 1:
        template = 'Profiles/usernotfound.html'
        context = RequestContext(request,)
    else:
        professor = prof[0]
        user = StudentUser.objects.filter(user=request.user)[0]
        curr_user_classes = StudentUser.getCurrentClasses(user)
        prof_curr_classes = Professor.getCurrentClasses(professor)
        prof_past_classes = Professor.getCurrentClasses(professor)


        context = RequestContext(request, {
                                 'professor': professor,
                                 'curr_user': user,
                                 'curr_user_classes': curr_user_classes,
                                 'prof_curr_classes': prof_curr_classes,
                                 'prof_past_classes': prof_past_classes,
                                  })
    return render_to_response(template, locals(), context)

@login_required
def departmentProfile(request, code):
    template = 'Profiles/departmentprofile.html'
    depart=Department.objects.filter(department_code=code)
    
    if len(depart) != 1:
        template = 'Profiles/usernotfound.html'
        context = RequestContext(request,)
    else:
        department = depart[0]
        user = StudentUser.objects.filter(user=request.user)[0]
        curr_user_classes = StudentUser.getCurrentClasses(user)
        #dept_curr_classes = Department.getCurrentClasses(department)
        #dept_past_classes = Department.getCurrentClasses(department)

        context = RequestContext(request, {
                                 'department': department,
                                 'curr_user': user,
                                 'curr_user_classes': curr_user_classes,
                                 'dept_curr_classes': "",
                                 'dept_past_classes': "",
                                 })
    return render_to_response(template, locals(), context)




@login_required
def edit_profile(request, first, last, student_id):
    curr_user = StudentUser.objects.filter(user=request.user)[0]
    threads = curr_user.thread_set.all()
    curr_user_classes = StudentUser.getCurrentClasses(curr_user)
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            form.edit_user(request,)
            redirect = '/Profiles/' + curr_user.first_name + curr_user.last_name + '/' + str(curr_user.pk) + '/'
            return HttpResponseRedirect(redirect)
        else:
            return HttpResponse("Invalid Form")
    else:
        form = EditProfileForm(initial={'first_name': curr_user.first_name,
                                                              'last_name': curr_user.last_name,
                                                              'email_id': curr_user.email_id,
                                                              'bio': curr_user.bio,
                                                              'grad_year': curr_user.grad_year,
                                                              'majors': curr_user.majors.values_list('id', flat=True),
                                                              'minors': curr_user.minors.values_list('id', flat=True),
                                                              })
    return render(request, 'Profiles/editprofile.html', RequestContext(request, {'curr_user': curr_user,
                                                                                 'threads': threads,
                                                                                 'edit_profile_form': form,
                                                                                 'curr_user_classes': curr_user_classes,
                                                                                 }))
