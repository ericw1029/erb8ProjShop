from django.urls import path
from . import views
#url define here is the endpoint e.g. xx/xxx/xxx/about
app_name ='pages'

urlpatterns = [
    path('',views.index,name='index'),
    path('about',views.about,name='about')
]