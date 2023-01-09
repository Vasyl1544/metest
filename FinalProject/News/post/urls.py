from django.urls import path, include
from post.views import *
from django.conf.urls import url
from post import views as core_views

app_name = 'post'
urlpatterns = [
    path('', post_list, name='post_list'),
    path('create/', post_create, name='create'),
    path('delete/<int:id>/', post_delete, name='delete'),
    path('detail/<int:id>/', post_detail, name='detail'),
    path('update/<int:id>/', post_update, name='update'),
    url(r'^signup/$', core_views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),

]



















