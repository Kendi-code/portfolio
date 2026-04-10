from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path('login/',  views.dashboard_login,  name='dashboard_login'),
    path('logout/', views.dashboard_logout, name='dashboard_logout'),

    # Overview
    path('', views.dashboard_home, name='dashboard_home'),

    # Projects
    path('projects/',              views.project_list,   name='dashboard_projects'),
    path('projects/add/',          views.project_add,    name='dashboard_project_add'),
    path('projects/<int:pk>/edit/', views.project_edit,  name='dashboard_project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='dashboard_project_delete'),

    # Blog posts
    path('posts/',                 views.post_list,   name='dashboard_posts'),
    path('posts/add/',             views.post_add,    name='dashboard_post_add'),
    path('posts/<int:pk>/edit/',   views.post_edit,   name='dashboard_post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='dashboard_post_delete'),

    # Contact messages
    path('messages/',                    views.message_list,   name='dashboard_messages'),
    path('messages/<int:pk>/',           views.message_detail, name='dashboard_message_detail'),
    path('messages/<int:pk>/delete/',    views.message_delete, name='dashboard_message_delete'),
]