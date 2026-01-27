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
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

from schema_graph.views import Schema


# urlpatterns = [
#     path('admin/', admin.site.urls),     
#     path('i18n/', include('django.conf.urls.i18n')),
#     path("schema/", Schema.as_view()),    
#     path('cart/', include('cart.urls', namespace='cart')),
#     path('orders/', include('orders.urls', namespace='orders')),  
#     path('accounts/',include('accounts.urls',namespace='accounts')),
#     path('reviews/', include('reviews.urls', namespace='reviews')), 
#     path("blogs/", include("blogs.urls", namespace="blogs")),
#     #path('accounts/',include('accounts.urls',namespace='accounts')),    
#     path('payment/', include('payment.urls', namespace='payment')),
#     path('coupons/', include('coupons.urls', namespace='coupons')),
#     path('',include('pages.urls',namespace='pages')), 
# ] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()
#"""
urlpatterns = i18n_patterns(
   path('admin/', admin.site.urls),    
   path(_('cart/'), include('cart.urls', namespace='cart')),
   path(_('orders/'), include('orders.urls', namespace='orders')),  
   path(_('accounts/'),include('accounts.urls',namespace='accounts')),
   path(_('reviews/'), include('reviews.urls', namespace='reviews')), 
   path(_("blogs/"), include("blogs.urls", namespace="blogs")),
   path(_('accounts/'),include('accounts.urls',namespace='accounts')),    
   path(_('payment/'), include('payment.urls', namespace='payment')),
   path(_('coupons/'), include('coupons.urls', namespace='coupons')),
   #path('rosetta/', include('rosetta.urls')),
   path('',include('pages.urls',namespace='pages')),  
)

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) + debug_toolbar_urls()

# admin.site.site_header ="Clinic Administrator"
# admin.site.site_title ="Clinic Admin Portal"
# admin.site.index_header ="Welcome to Clinic Portal"
