from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import NewUser, Question, Answer, TrendingQuestion, TrendingAnswer
import jwt, json
import hashlib
from datetime import datetime

@csrf_exempt
def new_user(request):
	if request.method == 'POST':
		name = request.POST.get('name')
		user_name = request.POST.get('user_name')
		password = request.POST.get('password')
		email_check = NewUser.objects.filter(user_name=user_name).all()
		response = {}
		if not email_check:
			try:
				password = password_hash(password)
				create_user = NewUser(name=name, user_name=user_name, password=password)
				create_user.save()
				response['status_code'] = 200
				response['status_message'] =  "New user created"
				return HttpResponse(json.dumps(response), content_type="application/json")
			except Exception as e:
				return HttpResponse(e)
		else:
			response['status_code'] = 400
			response['status_message'] =  "User name already existing"
			return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def user_login(request):
	if request.method == 'POST':
		user_name = request.POST.get('user_name')
		password = request.POST.get('password')
		email_check = NewUser.objects.filter(user_name=user_name).all()
		if email_check:
			password = password_hash(password=password)
			email_check = NewUser.objects.filter(user_name=user_name, password=password).all()
			if email_check:
				response = {}
				token = ''
				for user_id in email_check:
					encoded = {
						'user_id' : user_id.id,
						'name' : user_id.name,
						'user_name' : user_id.user_name,
 					}
					token = jwt_encode(payload=encoded)
				response['status_code'] = 200
				response['token'] = token
				response['status_message'] =  "Login successfully"
				return HttpResponse(json.dumps(response), content_type="application/json")
			else:
				response = {}
				response['status_code'] = 401
				response['status_message'] =  "Incorrect password"
				return HttpResponse(json.dumps(response), content_type="application/json")
		else:
			response = {}
			response['status_code'] = 400
			response['status_message'] =  "username is not exists"
			return HttpResponse(json.dumps(response), content_type="application/json")

def password_hash(password):
	return hashlib.sha512(password).hexdigest()

def jwt_encode(payload):
	return jwt.encode(payload, 'Stack', algorithm='HS256')

def jwt_decode(payload):
	return jwt.decode(payload, 'Stack', algorithm='HS256')

def date_conversion(date, result_format):
	return date.strftime(result_format)

@csrf_exempt
def question_creation(request):
	title = request.POST.get('title')
	description = request.POST.get('description')
	category = request.POST.get('category')
	user_id = jwt_decode(payload=request.POST.get('token'))
	user_id = NewUser.objects.filter(id=user_id.get('user_id')).all()
	for ids in user_id:
		user_id = ids
	category = map(str, (category.split(',')))
	response = {}
	try:
		create_question = Question(title=title, description=description, category=category, user_id=user_id)
		create_question.save()
		response['status_code'] = 200
		response['status_message'] =  "Questions created"
		return HttpResponse(json.dumps(response), content_type="application/json")
	except Exception as e:
		return HttpResponse(e)

@csrf_exempt
def answer_creation(request):
	description = request.POST.get('description')
	user_id = jwt_decode(payload=request.POST.get('token'))
	user_id = NewUser.objects.filter(id=user_id.get('user_id')).all()
	for ids in user_id:
		user_id = ids
	
	ques_id = Question.objects.filter(id=request.POST.get('ques_id')).all()
	for ids in ques_id:
		ques_id = ids

	response = {}
	answer_check = Answer.objects.filter(user_id=user_id, ques_id=ques_id).all()
	if not answer_check:
		try:
			create_answer = Answer(description=description, user_id=user_id, ques_id=ques_id)
			create_answer.save()
			response['status_code'] = 200
			response['status_message'] =  "Answer created"
			return HttpResponse(json.dumps(response), content_type="application/json")
		except Exception as e:
			return HttpResponse(e)
	else:
		Answer.objects.filter(user_id=user_id, ques_id=ques_id).update(description=description)
		response['status_code'] = 201
		response['status_message'] =  "Answer Updated"
		return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def star_added(request):
	star = request.POST.get('star')
	
	user_id = jwt_decode(payload=request.POST.get('token'))
	user_id = NewUser.objects.filter(id=user_id.get('user_id')).all()
	for ids in user_id:
		user_id = ids
	
	ques_id = Question.objects.filter(id=request.POST.get('ques_id')).all()
	for ids in ques_id:
		ques_id = ids

	star_check = TrendingQuestion.objects.filter(user_id=user_id, ques_id=ques_id).all()
	if not star_check:
		try:
			create_star = TrendingQuestion(star=True, user_id=user_id, ques_id=ques_id)
			create_star.save()
			response = {}
			response['status_code'] = 200
			response['status_message'] =  "Star Added"
			return HttpResponse(json.dumps(response), content_type="application/json")
		
		except Exception as e:
			return HttpResponse(e)
	else:
		try:
			star = False
			for stars in star_check:
				star = not stars.star
			star_check = TrendingQuestion.objects.filter(user_id=user_id, ques_id=ques_id).update(star=star)
			response = {}
			response['status_code'] = 204
			response['status_message'] =  "Star Updated"
			return HttpResponse(json.dumps(response), content_type="application/json")

		except Exception as e:
			return HttpResponse(e)

@csrf_exempt
def view_added(request):
	star = request.POST.get('view')
	
	user_id = jwt_decode(payload=request.POST.get('token'))
	user_id = NewUser.objects.filter(id=user_id.get('user_id')).all()
	for ids in user_id:
		user_id = ids
	
	ques_id = Question.objects.filter(id=request.POST.get('ques_id')).all()
	for ids in ques_id:
		ques_id = ids

	view_check = TrendingQuestion.objects.filter(user_id=user_id, ques_id=ques_id).all()
	if not view_check:
		try:
			create_view = TrendingQuestion(views=True, user_id=user_id, ques_id=ques_id)
			create_view.save()
			response = {}
			response['status_code'] = 200
			response['status_message'] =  "View Added"
			return HttpResponse(json.dumps(response), content_type="application/json")
		
		except Exception as e:
			return HttpResponse(e)
	else:
		for view in view_check:
			if not view.views:
				try:
					view = not view.views
					create_view = TrendingQuestion.objects.filter(user_id=user_id, ques_id=ques_id).update(views=view)
					response = {}
					response['status_code'] = 200
					response['status_message'] =  "View Updated"
					return HttpResponse(json.dumps(response), content_type="application/json")
				
				except Exception as e:
					return HttpResponse(e)

			else:
				response = {}
				response['status_code'] = 201
				response['status_message'] =  "View Already Added"
				return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def votes_added(request):
	up_vote = request.POST.get('up_vote')
	down_vote = request.POST.get('down_vote')
	
	user_id = jwt_decode(payload=request.POST.get('token'))
	user_id = NewUser.objects.filter(id=user_id.get('user_id')).all()
	for ids in user_id:
		user_id = ids
	
	ques_id = Question.objects.filter(id=request.POST.get('ques_id')).all()
	for ids in ques_id:
		ques_id = ids

	vote_check = TrendingQuestion.objects.filter(user_id=user_id, ques_id=ques_id).all()
	if not vote_check:
		try:
			create_vote = TrendingQuestion(up_vote=True, down_vote=False, user_id=user_id, ques_id=ques_id)
			create_vote.save()
			response = {}
			response['status_code'] = 200
			response['status_message'] =  "Vote Added"
			return HttpResponse(json.dumps(response), content_type="application/json")
		
		except Exception as e:
			return HttpResponse(e)
	else:
		for vote in vote_check:
			if vote.up_vote != up_vote and vote.down_vote != down_vote and up_vote != down_vote:
				try:
					create_view = TrendingQuestion.objects.filter(user_id=user_id, ques_id=ques_id).update(up_vote=up_vote, down_vote=down_vote)
					response = {}
					response['status_code'] = 200
					response['status_message'] =  "Vote Added"
					return HttpResponse(json.dumps(response), content_type="application/json")
				
				except Exception as e:
					return HttpResponse(e)

			else:
				response = {}
				response['status_code'] = 201
				response['status_message'] =  "Vote Already Added"
				return HttpResponse(json.dumps(response), content_type="application/json")

@csrf_exempt
def answer_votes_added(request):
	up_vote = request.POST.get('up_vote')
	down_vote = request.POST.get('down_vote')

	user_id = jwt_decode(payload=request.POST.get('token'))
	user_id = NewUser.objects.filter(id=user_id.get('user_id')).all()
	for ids in user_id:
		user_id = ids
	
	ans_id = Answer.objects.filter(id=request.POST.get('ans_id')).all()
	for ids in ans_id:
		ans_id = ids

	vote_check = TrendingAnswer.objects.filter(user_id=user_id, ans_id=ans_id).all()

	if not vote_check:
		try:
			create_vote = TrendingAnswer(up_vote=True, down_vote=False, user_id=user_id, ans_id=ans_id)
			create_vote.save()
			response = {}
			response['status_code'] = 200
			response['status_message'] =  "Vote Added"
			return HttpResponse(json.dumps(response), content_type="application/json")
		
		except Exception as e:
			return HttpResponse(e)
	else:
		for vote in vote_check:
			if vote.up_vote != up_vote and vote.down_vote != down_vote and up_vote != down_vote:
				try:
					create_view = TrendingAnswer.objects.filter(user_id=user_id, ans_id=ans_id).update(up_vote=up_vote, down_vote=down_vote)
					response = {}
					response['status_code'] = 200
					response['status_message'] =  "Vote Added"
					return HttpResponse(json.dumps(response), content_type="application/json")
				
				except Exception as e:
					return HttpResponse(e)

			else:
				response = {}
				response['status_code'] = 201
				response['status_message'] =  "Vote Already Added"
				return HttpResponse(json.dumps(response), content_type="application/json")

def question_list(request):
	question_list = Question.objects.all()
	question = []
	for row in question_list:
		created_on = date_conversion(row.pub_date, '%Y-%m-%d')
		username = NewUser.objects.filter(id=row.user_id.id).values_list('name')
		for user in username:
			name = user[0] if user else None
		single_ques = {
			'name'			: name,
			'ques_id'		: row.id,
			'ques_title'	: row.title,
			'category'		: row.category,
			'created_on'	: created_on,
			'answer_count' 	: Answer.objects.filter(ques_id=row.id).count(),
			'view_count' 	: TrendingQuestion.objects.filter(ques_id=row.id, views=True).count(),
			'vote_count' 	: TrendingQuestion.objects.filter(ques_id=row.id, up_vote=True, down_vote=False).count(),
		}
		question.append(single_ques)

	return HttpResponse(json.dumps(question), content_type="application/json")

def category_question_list(request):
	category = []
	category.append( request.GET.get('category') )
	question_list = Question.objects.filter(category__contains=list(category)).all()
	print question_list
	question = []
	for row in question_list:
		created_on = date_conversion(row.pub_date, '%Y-%m-%d')
		username = NewUser.objects.filter(id=row.user_id.id).values_list('name')
		for user in username:
			name = user[0] if user else None
		single_ques = {
			'name'			: name,
			'ques_id'		: row.id,
			'ques_title'	: row.title,
			'category'		: row.category,
			'created_on'	: created_on,
			'answer_count' 	: Answer.objects.filter(ques_id=row.id).count(),
			'view_count' 	: TrendingQuestion.objects.filter(ques_id=row.id, views=True).count(),
			'vote_count' 	: TrendingQuestion.objects.filter(ques_id=row.id, up_vote=True, down_vote=False).count(),
		}
		question.append(single_ques)

	return HttpResponse(json.dumps(question), content_type="application/json")

@csrf_exempt
def single_question(request):
	user_id = jwt_decode(payload=request.GET.get('token'))
	user_id = NewUser.objects.filter(id=user_id.get('user_id')).all()
	for ids in user_id:
		user_id = ids

	single_ques = {}
	ques_id = Question.objects.filter(id=request.GET.get('id')).all()
	for row in ques_id:
		vote_count = TrendingQuestion.objects.filter(ques_id=ques_id, up_vote=True, down_vote=False).count() - TrendingQuestion.objects.filter(ques_id=ques_id, up_vote=False, down_vote=True).count()
		star_result = TrendingQuestion.objects.filter(user_id=user_id, ques_id=ques_id, star=True).all()
		for star in star_result:
			star_result = star.star
		
		single_ques["question"] = {
			'ques_id' 		: row.id,
			'ques_title'	: row.title,
			'vote_count'	: vote_count,
			'star'			: star_result
		}

	ans_id = Answer.objects.filter(ques_id=ques_id).all()
	answers_list = []
	for row in ans_id:
		username = NewUser.objects.filter(id=row.user_id.id).values_list('name')
		for user in username:
			username = user[0] if user else None

		vote_count = TrendingAnswer.objects.filter(ans_id=row.id, up_vote=True, down_vote=False).count() - TrendingAnswer.objects.filter(ans_id=row.id, up_vote=False, down_vote=True).count()
		answer = {
			'description'	: row.description,
			'created_on'	: date_conversion(row.pub_date, '%Y-%m-%d'),
			'accepted'		: row.accepted,
			'name'			: username,
			'vote_count'	: vote_count
		}
		answers_list.append(answer)
	single_ques['answer'] = answers_list
	return HttpResponse(json.dumps(single_ques), content_type="application/json")