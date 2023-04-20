from django.urls import path,include,re_path
from rest_framework import routers
from server.views import GroupView,ServerView,gather_node,ServerdetailsView,One_click_synchronization,NodeSX,UpdateNode
from server.other import auth_login
from rest_framework.authtoken import views as auth_token_views

route = routers.DefaultRouter()
route.register(r'group',GroupView)
route.register(r'server',ServerView)
route.register(r'serverdetais',ServerdetailsView)
urlpatterns = [
    path('api/',include(route.urls)),

]


urlpatterns += [
    re_path('^login/',auth_login.CustomAuthToken.as_view()),
    re_path('^updatePassword/',auth_login.UpdatePassword.as_view()),
    re_path('^gather_node/',gather_node.as_view()),
    re_path('^synchronization/',One_click_synchronization.as_view()),
    re_path('^NodeHostname/',NodeSX.as_view()),
    re_path('^UpdateHostname/',UpdateNode.as_view())
]