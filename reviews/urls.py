from django.urls import path
from . import views
from django.utils.translation import gettext_lazy as _

app_name = 'reviews'

urlpatterns = [
    path('add/<int:product_id>/', views.add_review, name='add_review'),
    path('edit/<int:review_id>/', views.edit_review, name='edit_review'),
]

"""
urlpatterns = [
    path(_('add/<int:product_id>/'), views.add_review, name='add_review'),
    path(_('edit/<int:review_id>/'), views.edit_review, name='edit_review'),
]
"""