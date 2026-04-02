from django.urls import path

from .views import (
    MemberView,
    MembershipView,
    UpdateDeleteRetrieveView,
    UserView,
    WorkView,
    WorkspaceView,
)

urlpatterns = [
    path("register/", UserView.as_view(), name="create_user"),
    path("users/<int:pk>/", UpdateDeleteRetrieveView.as_view(), name="user_detail"),
    path("workspaces/", WorkspaceView.as_view(), name="workspace_list"),
    path("workspaces/<int:pk>/", WorkView.as_view(), name="workspace_detail"),
    path("memberships/", MemberView.as_view(), name="membership_list"),
    path("memberships/<int:pk>/", MembershipView.as_view(), name="membership_detail"),
]
