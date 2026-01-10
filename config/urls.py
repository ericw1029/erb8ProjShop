"""
URL configuration for conf project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf.urls.static import static
from django.conf import settings
#https://django-debug-toolbar.readthedocs.io/en/latest/installation.html
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),  
    path('accounts/',include('accounts.urls',namespace='accounts')),    
    path('',include('pages.urls',namespace='pages')),  
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()


# admin.site.site_header ="Clinic Administrator"
# admin.site.site_title ="Clinic Admin Portal"
# admin.site.index_header ="Welcome to Clinic Portal"
