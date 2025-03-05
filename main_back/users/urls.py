from django.urls import path, include

from users.views import GetListUsers, BanUser, MakeUserAdmin

urlpatterns = [
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('users/', GetListUsers.as_view(), name='get_list_users'),

    # Make a specific user an admin
    path('users/<int:user_id>/make_admin/', MakeUserAdmin.as_view(), name='make_user_admin'),

    # Ban a specific user
    path('users/<int:user_id>/ban/', BanUser.as_view(), name='ban_user'),
]