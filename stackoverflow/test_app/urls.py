from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^new/user', views.new_user, name='create_user'),
    url(r'^login', views.user_login, name='login'),
    url(r'^create_question', views.question_creation, name='create_question'),
    url(r'^answer', views.answer_creation, name='create_answer'),
    url(r'^star', views.star_added, name='star_added'),
    url(r'^view', views.view_added, name='view_added'),
    url(r'^votes', views.votes_added, name='votes_added'),
    url(r'^answer_votes', views.answer_votes_added, name='answer_votes_added'),
    url(r'^questions', views.question_list, name='question_list'),
    url(r'^category_search', views.category_question_list, name='category_question_list'),
    url(r'^question', views.single_question, name='single_question'),
]