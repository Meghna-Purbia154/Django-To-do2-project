from django.urls import path
from . import views

urlpatterns = [
    # TASK CRUD
    path('', views.task_list, name='task-list'),
    path('task/<int:pk>/', views.task_detail, name='task-detail'),
    path('task/add/', views.task_create, name='task-add'),
    path('task/<int:pk>/edit/', views.task_update, name='task-edit'),
    path('task/<int:pk>/delete/', views.task_delete, name='task-delete'),

    # AUTH
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.login_view, name='login'),

    # CATEGORIES
    path('categories/', views.category_list, name='category-list'),
    path('category/<int:pk>/', views.category_tasks, name='category-tasks'),

    # NOTIFICATIONS
    path('notifications/', views.notification_list, name='notification-list'),

    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
]
