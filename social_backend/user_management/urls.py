from django.urls import re_path
from rest_framework import routers
from . import views
from django.urls import path

router = routers.SimpleRouter()

urlpatterns = [re_path(r"^login/$", views.LoginView.as_view(), name="login"),
path("sign-up/", views.UserSignupView.as_view()),
path("find-user/", views.FindUser.as_view()),
path('send-request/<int:receiver_id>/', views.SendFriendRequest.as_view(), name='send-friend-request'),
path('accept-reject-request/<int:friend_request_id>/<str:action>/', views.AcceptRejectFriendRequest.as_view(), name='accept-reject-friend-request'),
path('friends/', views.ListFriends.as_view(), name='list-friends'),
path('pending-requests/', views.ListPendingFriendRequests.as_view(), name='list-pending-requests'),
]
