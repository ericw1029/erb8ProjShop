from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/',views.login,name='login'),
    #path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/',views.logout,name='logout'),
    path('register/',views.register,name='register'),
    path('dashboard/',views.dashboard,name='dashboard'),

    path('password-reset/',
          auth_views.PasswordResetView.as_view(
              template_name="accounts/password_reset_form.html",
              #email_template_name="accounts/email/password_reset_email.html",
              email_template_name="accounts/password_reset_email.html",
              #success_url=reverse_lazy("accounts:password_reset_done") # Specify the namespaced URL
              success_url=reverse_lazy("pages:index")
          ),
          name='password_reset'),
    path('password-reset/done/',
          auth_views.PasswordResetDoneView.as_view(),
          name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
          auth_views.PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
    path('password-reset/complete/',
          auth_views.PasswordResetCompleteView.as_view(),
          name='password_reset_complete'),
]
