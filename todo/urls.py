from django.conf.urls import url
from . import views as user_view
from django.contrib.auth import views as auth_views

app_name="todo"

urlpatterns = [

    url(r'^$', user_view.registration, name="taskmanager"),
    url(r'registered/',user_view.registered, name='registered'),
    url(r'login/', user_view.login_view, name='login'),
    url(r'logout/', auth_views.LogoutView.as_view(template_name="todo/logout.html"), name='logout'),
    url(r'home/',user_view.home_view, name='home'),

    url(r'^profile/(?P<user_id>\d+)/$', user_view.user_profile, name='profile'),
    url(r'pending/', user_view.get_pending_request, name='pending_requests'),
    url(r'^approve/(?P<user_id>\d+)/$', user_view.approve_user, name='approve'),
    url(r'assign/',user_view.add_task, name='add_task'),
    url(r'^taskboard/$',user_view.taskboard, name='taskboard'),
    url(r'^completed/(?P<task_id>\d+)/$', user_view.task_completed, name='taskcompleted'),
    url(r'^edit/(?P<task_id>\d+)/$', user_view.edit_task, name='edittask'),
    url(r'^delete/(?P<task_id>\d+)/$', user_view.delete_task, name='deletetask'),

    url(r'group/', user_view.create_user_group, name='group'),

]