from django.urls import path

from authors.views import (dashboard, dashboard_post_delete,
                           dashboard_post_edit, dashboard_post_like,
                           dashboard_post_new, login_create, login_view,
                           logout_view, register_create, register_view)

urlpatterns = [
    path("register/", register_view, name='authors-register'),
    path("register/create/", register_create, name='authors-create'),
    path("login/", login_view, name='authors-login'),
    path("login/create/", login_create, name='authors-login-create'),
    path("logout/", logout_view, name='authors-logout'),
    path("dashboard/", dashboard, name="authors-dashboard"),
    path("dashboard/post/new", dashboard_post_new, name="authors-dashboard-post-new"),
    path("dashboard/post/<int:id>/edit", dashboard_post_edit, name="authors-dashboard-post-edit"),
    path("dashboard/post/delete", dashboard_post_delete, name="authors-dashboard-post-delete"),
    path("dashboard/post/like", dashboard_post_like, name="authors-dashboard-post-like"),
]

