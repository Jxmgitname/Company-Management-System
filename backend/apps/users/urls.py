from django.urls import path
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet,LoginView, RegisterView,UserInfoView, DashboardView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('user/info/', UserInfoView.as_view(), name='user-info'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]

urlpatterns += router.urls
