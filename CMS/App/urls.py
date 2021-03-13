from django.urls import path
from django.conf.urls import url

from .views import *

urlpatterns = [
        path("create-user/", CreateUser.as_view(), name="Create Author"),
        path('signin/', SignIn.as_view(), name="Sign In"),
        path('content/', CreateContent.as_view(), name="Create content")
        ]
