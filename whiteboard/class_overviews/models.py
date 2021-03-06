from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from wbMessageBoard.models import DiscussionBoard
import sys


class Semester(models.Model):
    season = models.CharField(max_length=10, default="Fall")
    year = models.IntegerField(default=2015)
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.season + " " + str(self.year)


class Course(models.Model):
    department = models.CharField(max_length=4)
    course_number = models.IntegerField(default=999)
    course_name = models.CharField(max_length=200)
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.department + str(self.course_number) + ": " + self.course_name




class Section(models.Model):
    location = models.CharField(max_length=50)
    start_time = models.TimeField(auto_now=False, blank=True)
    end_time = models.TimeField(auto_now=False, blank=True)
    days_of_week = models.CharField(max_length=7)
    section_number = models.IntegerField(default=0)
    course = models.ForeignKey(Course)
    semester = models.ForeignKey(Semester)

    def __str__(self):
        return str(self.course) + " (" + str(self.section_number) + ") " + self.semester.season + str(self.semester.year)


class Document(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, blank=True)
    file = models.FileField(upload_to='documents')
    course_section = models.ForeignKey(Section)

    def __str__(self):
        return self.name

@receiver(post_save, sender=Section)
def create_board(sender, instance, created, **kwargs):
    if created and 'test' not in sys.argv and 'migrate' not in sys.argv and 'loaddata' not in sys.argv:
        board, created = DiscussionBoard.objects.get_or_create(course=instance,
                                                               name= instance.course.course_name + ' ' + str(instance.section_number),
                                                               description='Blah')