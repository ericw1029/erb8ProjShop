from django.urls import path
from . import views
#url define here is the endpoint e.g. xx/xxx/xxx/about
app_name ='pages'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('index',views.index,name='index'),
    path('about',views.about,name='about')
]