from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),

    path('password-change/', 
          auth_views.PasswordChangeView.as_view(
              template_name='accounts/password_change_form.html',
              success_url=reverse_lazy('accounts:password_change_done')
          ), 
          name='password_change'),
    path('password-change/done/', 
          auth_views.PasswordChangeDoneView.as_view(
              template_name='accounts/password_change_done.html'
          ), 
          name='password_change_done'),

    path('password-reset/',
          auth_views.PasswordResetView.as_view(
              template_name="accounts/password_reset_form.html",
              email_template_name="accounts/password_reset_email.html",
              success_url=reverse_lazy("accounts:password_reset_done")
          ),
          name='password_reset'),
    path('password-reset/done/',
          auth_views.PasswordResetDoneView.as_view(
              template_name="accounts/password_reset_done.html"
          ),
          name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(  
              template_name="accounts/password_reset_confirm.html",
              success_url=reverse_lazy("accounts:password_reset_complete")
          ),
          name='password_reset_confirm'),
    path('password-PasswordResetCompleteViewreset/complete/',
          auth_views.PasswordResetCompleteView.as_view(
              template_name="accounts/password_reset_complete.html"
          ),
          name='password_reset_complete'),
    path('password-reset-complete/',views.password_reset_complete,name='password-reset-complete'),
    path('password-reset-confirm/',views.password_reset_confirm,name='password-reset-confirm'),
    path('password-reset-complete/',views.password_reset_complete,name='password-reset-complete'),
    path('password-reset-done/',views.password_reset_done,name='password-reset-done'),
]
