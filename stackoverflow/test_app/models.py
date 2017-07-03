from django.db import models
from django.contrib.postgres.fields import ArrayField

class NewUser(models.Model):
	name = models.CharField(max_length=100, blank=False)
	user_name = models.EmailField(max_length=70, unique=True)
	password = models.TextField(blank=False, null=False)
	created_on = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
	title = models.CharField(max_length=100, blank=False, null=False)
	description = models.TextField(blank=False, null=False)
	category = ArrayField(models.TextField(blank=False), size=5)
	user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
	pub_date = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
	description = models.TextField(blank=False, null=False)
	ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
	user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
	accepted = models.BooleanField(default=False)
	pub_date = models.DateTimeField(auto_now_add=True)

class TrendingQuestion(models.Model):
	ques_id = models.ForeignKey(Question, on_delete=models.CASCADE)
	user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
	star = models.BooleanField(default=False)
	up_vote = models.BooleanField(default=False)
	down_vote = models.BooleanField(default=False)
	views = models.BooleanField(default=False)
	created_on = models.DateTimeField(auto_now_add=True)

class TrendingAnswer(models.Model):
	ans_id = models.ForeignKey(Question, on_delete=models.CASCADE)
	user_id = models.ForeignKey(NewUser, on_delete=models.CASCADE)
	up_vote = models.BooleanField(default=False)
	down_vote = models.BooleanField(default=False)
	created_on = models.DateTimeField(auto_now_add=True)