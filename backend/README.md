# 公司内部后台管理系统（后端）

Django 4.2 + DRF + SimpleJWT。业务代码在 `apps/`（员工、岗位、部门）。

完整启动步骤看仓库根目录的 `README.md`。这里只记后端注意点。

## 启动

在 `backend` 目录，先激活虚拟环境 `env`，再：

```bash
.\env\Scripts\Activate.ps1
python manage.py runserver
```

地址：`http://127.0.0.1:8000/`  
根路径没有页面，浏览器打开出现 404 是正常的。

数据库配置在 `backend/settings.py` 的 `DATABASES`，不要把密码写进本说明。

## 接口前缀

- 登录：`POST /api/login/`，传 `username`、`password`，返回 JWT
- 注册：`POST /api/register/`
- 当前登录人：`GET /api/user/info/`
- 人员概况：`GET /api/dashboard/`
- 员工：`/api/users/`
- 岗位 / 菜单 / 部门：`/api/roles/`、`/api/menus/`、`/api/departments/`

认证：请求头 `Authorization: Bearer <access_token>`
