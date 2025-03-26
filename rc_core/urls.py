from django.urls import path

from . import views as rc_core

urlpatterns = [
    path('add-user',rc_core.AddNewUserView.as_view(),name='adduser'),
    path('manage-users',rc_core.ManageUserView.as_view(),name='manageusers'),
]