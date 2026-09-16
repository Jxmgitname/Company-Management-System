from django.db.models import Q, Count
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from backend.response import error_response, success_response
from system.models import Department, Menu, Role
from system.serializers import DepartmentSerializer, MenuSerializer, RoleSerializer

# 菜单管理
class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
# 角色管理
class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().prefetch_related('menus')
    def get_queryset(self):
        qs = super().get_queryset()
        keyword = (self.request.query_params.get('name') or '').strip()
        if keyword:
            qs = qs.filter(
                Q(name__icontains=keyword) | Q(code__icontains=keyword)
            )
        return qs.annotate(userCount=Count('users', distinct=True))       
    serializer_class = RoleSerializer
    # 新增角色
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()
        return success_response(RoleSerializer(role).data, message='岗位创建成功', status_code=status.HTTP_201_CREATED)
     # 修改角色
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        role = serializer.save()
        return success_response(RoleSerializer(role).data, message='岗位已更新')
     # 删除角色
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message='删除成功')
# 部门管理
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    def get_queryset(self):
        qs = super().get_queryset()
        keyword = (self.request.query_params.get('name') or '').strip()
        if keyword:
            qs = qs.filter(
                Q(name__icontains=keyword) | Q(leader__icontains=keyword)
            )
        return qs
    serializer_class = DepartmentSerializer
    # 新增部门
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()
        return success_response(DepartmentSerializer(department).data, message='部门创建成功', status_code=status.HTTP_201_CREATED)
     # 修改部门
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()
        return success_response(DepartmentSerializer(department).data, message='部门已更新')
     # 删除部门
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return success_response(message='删除成功')
