from django.db.models import Q
import jwt
from django.conf import settings
from rest_framework import mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Count
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

#from backend.response import success_response
from backend.response import error_response, success_response
from users.models import User
from system.models import Role, Department 
from users.serializers import (
    RegisterSerializer,
    UserCreateUpdateSerializer,
    UserSerializer,
)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    def post(self, request, *args, **kwargs):
        username = (request.data.get('username') or '').strip()
        password = request.data.get('password') or ''
        if not username or not password:
            return error_response('请输入账号和密码', code=400, status_code=400)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return error_response('账号或密码不正确', code=400, status_code=400)
        if not user.status:
            return error_response('账号已停用', code=400, status_code=400)

        refresh = RefreshToken.for_user(user)
        return success_response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, message='登录成功')

class UserInfoView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        return success_response({
            'username': user.username,
            'name': user.nickname or user.username,
            'avatar': user.avatar or 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
        })

class DashboardView(APIView):
    def get(self, request, *args, **kwargs):
        user_count = User.objects.count()
        role_count = Role.objects.count()
        dept_count = Department.objects.count()
        by_dept = []
        for dept in Department.objects.annotate(total=Count('users')):
            by_dept.append({
            'name': dept.name,
            'value': dept.total
        })
        by_role = []
        for role in Role.objects.annotate(total=Count('users')):
            by_role.append({
            'name': role.name,
            'value': role.total
        })
        return success_response({
            'user_count': user_count,
            'role_count': role_count,
            'dept_count': dept_count,
            'by_dept': by_dept,
            'by_role': by_role
        })
class RegisterView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success_response(UserSerializer(user).data, message='注册成功', status_code=status.HTTP_201_CREATED)


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    queryset = User.objects.all()
    def get_queryset(self):
        qs = super().get_queryset()
        keyword = (self.request.query_params.get('username') or '').strip()
        if keyword:
            qs = qs.filter(
                Q(username__icontains=keyword) | Q(nickname__icontains=keyword)
            )
        return qs

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return UserCreateUpdateSerializer
        return UserSerializer
    # 新增用户
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success_response(
            UserSerializer(user).data,
            message='员工创建成功',
            status_code=status.HTTP_201_CREATED
    )
    # 修改用户
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success_response(UserSerializer(user).data, message='员工已更新')
     # 删除用户
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.pk == request.user.pk:
            return error_response('不能删除当前登录账号', code=400, status_code=400)
        instance.delete()
        return success_response(message='删除成功')