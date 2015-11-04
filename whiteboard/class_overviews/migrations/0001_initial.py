# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('department', models.CharField(max_length=4)),
                ('course_number', models.IntegerField(default=999)),
                ('course_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('path', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('season', models.CharField(default='Fall', max_length=10)),
                ('year', models.IntegerField(default=2015)),
                ('location', models.CharField(max_length=50)),
                ('time_of_day', models.CharField(max_length=20)),
                ('days_of_week', models.CharField(max_length=7)),
                ('section_number', models.IntegerField(default=0)),
                ('course', models.ForeignKey(to='class_overviews.Course')),
            ],
            options={
                'ordering': ['-year', 'season'],
            },
        ),
        migrations.AddField(
            model_name='document',
            name='course_section',
            field=models.ForeignKey(to='class_overviews.Section'),
        ),
    ]
