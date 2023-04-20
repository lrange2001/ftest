from django.urls import path,re_path,include
from rest_framework import routers
from appdeploy.views import AppView,AppApiView,AppRunApiview




route = routers.DefaultRouter()
route.register(r'app',AppView)

urlpatterns = [
    re_path('^api/',include(route.urls)),
    re_path('^app/',AppApiView.as_view()),
    re_path('^apprun/',AppRunApiview.as_view()),
]
