from django.urls import path
from users_auth.views import (
    UserListView,
    get_department_designation,
    CreateUserView,
    DeleteUserView,
    UserRequestListView,
)
app_name= "users_auth"
urlpatterns = [
    path("users/", UserListView.as_view(), name="user-list"),
    path("requests/", UserRequestListView.as_view(), name="users-requests"),        
    path("users/unverify-user/<int:pk>/", UserListView.unverify_user, name="unverify-user"),
    path("singup/user-dept-desg/<int:college_id>/",get_department_designation , name="user-dept-desg"),
    path(
        "requests/batch-requests-verify/",
        UserRequestListView.batch_requests_verify,
        name="batch-requests-verify",
    ),
    
    path("singup/", CreateUserView.as_view(), name="add-user"),
    # path("update-user/<int:pk>/", UpdateUserView.as_view(), name="update-user"),
    path("delete-user/<int:pk>/", DeleteUserView.as_view(), name="delete-user"),
]
