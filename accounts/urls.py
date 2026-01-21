from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm' # This name must match exactly
    ),
    # path("dashboard/", views.dashboard, name="dashboard"),
    # path(
    #     "password-change/",
    #     auth_views.PasswordChangeView.as_view(
    #         template_name="accounts/password_change_form.html",
    #         success_url=reverse_lazy("accounts:password_change_done"),
    #     ),
    #     name="password_change",
    # ),
    # path(
    #     "password-change/done/",
    #     auth_views.PasswordChangeDoneView.as_view(
    #         template_name="accounts/password_change_done.html"
    #     ),
    #     name="password_change_done",
    # ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/password_reset_form.html",
            email_template_name="accounts/password_reset_email.html",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    # path(
    #     "password-reset/done/",
    #     auth_views.PasswordResetDoneView.as_view(
    #         template_name="accounts/password_reset_done.html"
    #     ),
    #     name="password_reset_done",
    # ),
    # path(
    #     "password-reset/<uidb64>/<token>/",
    #     auth_views.PasswordResetConfirmView.as_view(
    #         template_name="accounts/password_reset_confirm.html",
    #         success_url=reverse_lazy("accounts:password_reset_complete"),
    #     ),
    #     name="password_reset_confirm",
    # ),
    # path(
    #     "password-PasswordResetCompleteViewreset/complete/",
    #     auth_views.PasswordResetCompleteView.as_view(
    #         template_name="accounts/password_reset_complete.html"
    #     ),
    #     name="password_reset_complete",
    # ),
    # path(
    #     "password-reset-complete/",
    #     views.password_reset_complete,
    #     name="password-reset-complete",
    # ),
    # path(
    #     "password-reset-confirm/",
    #     views.password_reset_confirm,
    #     name="password-reset-confirm",
    # ),
    # path(
    #     "password-reset-complete/",
    #     views.password_reset_complete,
    #     name="password-reset-complete",
    # ),
    path("password-reset-done/", views.password_reset_done, name="password-reset-done"),
    path("change_password/", views.change_password, name="change_password"),
    path(
        "change-password/done/", views.change_password_done, name="change_password_done"
    ),
    # Password reset (for forgotten passwords)
    path("reset-password/", views.reset_password, name="reset_password"),
    path("reset-password/done/", views.reset_password_done, name="reset_password_done"),
    path(
        "reset/<uidb64>/<token>/",
        views.reset_password_confirm,
        name="reset_password_confirm",
    ),
    path("reset/done/", views.reset_password_complete, name="reset_password_complete"),
    path("profile/", views.profile, name="profile"),
    path("profile/create/<int:user_id>/", views.profile_create, name="profile_create"),
    path("profile/create/", views.profile_create, name="profile_create"),
    path("profile/<int:pk>/", views.profile_detail, name="profile_detail"),
    path("profile/<int:pk>/edit", views.edit_profile, name="edit_profile"),
    path("profile/<int:pk>/update/", views.profile_update, name="profile_update"),
]
