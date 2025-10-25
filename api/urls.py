from django.urls import path
from . import views
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

urlpatterns=[
    # Task Management
    path('tasks/', views.TaskListCreate.as_view(), name='Task_ListCreate'), # for listing all tasks and creating new tasks
    path('tasks/<pk>/', views.TaskRetrieveUpdateDelete.as_view(), name='Task_RetrieveUpdateDelete'), # primary-key based operations like - update,delete and read

    # Account Creation
    path('account/create/', views.AccountCreate.as_view(), name='create_account'),

    # JWT Routes for User Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
