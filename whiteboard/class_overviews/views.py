from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext, loader
from .models import Course, Section, Document
from wbMessageBoard.models import DiscussionBoard, Thread
from wb_calendar.models import Calendar, Event
from Profiles.models import StudentUser, Professor, Department
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
from django.utils import timezone
import sys


@login_required
def courseDetail(request, depart, course_num, sea="", yr=2015, section_num=0):

    template = 'class_overviews/course.html'
    c = Course.objects.filter(department = depart, course_number=course_num)
    if len(c) == 0:
        template = 'class_overviews/classnotfoundpage.html'
        context = RequestContext(request,)
        return render_to_response(template, locals(), context)
    else:
        c = c[0]

    if section_num == 0 and sea == "":
        s = Section.objects.filter(course = c)
    elif section_num != 0:
        s = Section.objects.filter(course = c, section_number = section_num)
    elif sea != "":
        s = Section.objects.filter(course = c, season = sea, year = yr)
    else:
        s = Section.objects.filter(course = c, season = sea, year = yr, section_number = section_num)

    if len(s) == 0:
        template = 'class_overviews/classnotfoundpage.html'
        context = RequestContext(request,)
        return render_to_response(template, locals(), context)
    else:
        s = s[0]

    sections = Section.objects.filter(course = c)

    documents = Document.objects.filter(course_section = s)

    b = DiscussionBoard.objects.filter(course = s)
    if len(b):
        threads = Thread.objects.filter(board = b)
    else:
        threads =   []

    students = s.studentuser_student.all()
    tas = s.studentuser_ta.all()

    user = StudentUser.objects.filter(user=request.user)[0]
    curr_classes = StudentUser.getCurrentClasses(user)

    professor = s.professor_set.all()[0]
    department = Department.objects.filter(department_code = depart)[0]

    context = RequestContext(request, {
        'course': c,
        'section' : s,
        'sections' : sections,
        'documents' : documents,
        'threads' : threads,
        'board_id': b[0].id,
        'students' : students,
        'teaching_assistants' : tas,
        'curr_user' : user,
        'curr_user_classes' : curr_classes,
        'professor' : professor,
        'department': department,
    })

    if(request.GET.get('mybtn')):
        addClass(s, user)

    return render_to_response(template, locals(), context)

def addClass(section, user):
    user.student_classes.add(section)

    calendar = Calendar.objects.filter(owner = user)[0]
    title = section.course.department + str(section.course.course_number)
    event = Event(title=title, description=section.course.course_name, calendar=calendar, start=section.start_time, end=section.end_time, recurring=False, dow=section.days_of_week)
    event.save()


@login_required
def getThreads(s):
    b = DiscussionBoard.objects.filter(course = s)

    threads = Thread.objects.filter(board = b)
    return threads


@login_required
def upload_document(request, depart, course_num, section_num):

    c = Course.objects.filter(department = depart, course_number=course_num)
    if len(c) == 0:
        template = 'class_overviews/classnotfoundpage.html'
        context = RequestContext(request,)
        return render_to_response(template, locals(), context)
    else:
        c = c[0]

    s = Section.objects.filter(course = c, section_number = section_num)
    if len(s) == 0:
        template = 'class_overviews/classnotfoundpage.html'
        context = RequestContext(request,)
        return render_to_response(template, locals(), context)
    else:
        s = s[0]
    print(request.method)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            new_document = Document( name = form.cleaned_data['name'],
                                description = form.cleaned_data['description'],
                                file = request.FILES['file'],
                                course_section = s,)
            new_document.save()
            return HttpResponseRedirect('/course/' + c.department
                                        + str(c.course_number) + '/'
                                        + s.semester.season + str(s.semester.year) + '/'
                                        + str(s.section_number))
        else:
            for field in form:
                sys.stderr.write(field.errors)
    else:
        form = UploadFileForm()

    context = {
        'course': c,
        'section' : s,
    }

    return render(request, 'class_overviews/upload_document.html', context)




