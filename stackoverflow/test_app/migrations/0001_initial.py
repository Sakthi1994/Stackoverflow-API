# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-03 04:40
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('user_name', models.EmailField(max_length=70, unique=True)),
                ('password', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=5)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.NewUser')),
            ],
        ),
        migrations.CreateModel(
            name='TrendingAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('up_vote', models.BooleanField(default=False)),
                ('down_vote', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ans_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.Question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.NewUser')),
            ],
        ),
        migrations.CreateModel(
            name='TrendingQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False)),
                ('up_vote', models.BooleanField(default=False)),
                ('down_vote', models.BooleanField(default=False)),
                ('views', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ques_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.Question')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.NewUser')),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='ques_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='test_app.NewUser'),
        ),
    ]
