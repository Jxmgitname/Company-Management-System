# 公司内部后台管理系统

系统功能：给公司内部管理员用的后台，管员工账号、岗位和部门，登录后先看全公司有多少人、人在哪些部门。

技术栈：Vue + Django + MySQL

## 一、整体

左边两个菜单：**组织人事**（员工、岗位、部门）、**人员概况**。

### 1. 登录

输入账号和密码，点「登录」。密码不对或账号被停用，都进不去。

![登录](docs/images/login.png)

### 2. 人员概况

登录后的第一页。上面三张卡片是员工、岗位、部门各有多少；左边饼图看人在哪些部门，右边柱状图看各岗位有多少人。

![人员概况](docs/images/stats.png)

### 3. 员工管理

员工名单：账号、姓名、手机号、部门、岗位。开关打开表示能登录，灰色表示暂时停用（账号还在，只是进不了系统）。

![员工管理](docs/images/user-list.png)

### 4. 岗位管理

岗位就是工作职务，例如运营专员、财务专员、前端工程师。

![岗位管理](docs/images/role-list.png)

### 5. 部门管理

公司组织架构。大部门下面可以挂小组，例如开发部下有前端组、后端组。

![部门管理](docs/images/dept-list.png)

---

## 二、具体功能

员工、岗位、部门都是同一套操作：搜索、新增、编辑、删除。删之前会再确认一次。不能删除自己正在登录的账号。

### 1. 员工管理

**增：** 点绿色「新增」，填账号、密码、姓名、手机号、部门、岗位，点确定。

![新增员工](docs/images/user-create.png)

**查：** 输入账号或姓名，点「查询」。例如搜「张浩」，只留下这一条。

![查询员工](docs/images/user-search.png)

**改：** 点「编辑」，改部门、岗位等。密码空着表示不改密码。

![编辑员工](docs/images/user-update.png)

**删：** 点「删除」会先问一句，确认后才去掉。

![删除员工](docs/images/user-delete.png)

### 2. 岗位管理

**增：** 点「新增」，填岗位名称、英文编码、描述。

![新增岗位](docs/images/role-create.png)

**查：** 按名称或编码搜索。例如搜「测试」，只留下测试工程师。

![查询岗位](docs/images/role-search.png)

**改：** 点「编辑」，改名称、编码或描述。

![编辑岗位](docs/images/role-update.png)

**删：** 点「删除」后确认，才会去掉这个岗位。

![删除岗位](docs/images/role-delete.png)

### 3. 部门管理

**增：** 点「新增」，填部门名称、负责人、排序。上级部门不选，就是最外层的大部门。

![新增部门](docs/images/dept-create.png)

**查：** 按部门名称或负责人搜索。例如搜「市场部」，只留下这一条。

![查询部门](docs/images/dept-search.png)

**改：** 点「编辑」，可改名称、负责人、排序，或改它挂在哪个上级下面。

![编辑部门](docs/images/dept-update.png)

**删：** 点「删除」后确认，才会去掉这个部门。

![删除部门](docs/images/dept-delete.png)

---

## 三、本机运行

- 前端：Vue2 + Element UI
- 后端：Django 4.2 + Django REST Framework
- 登录：JWT（账号 + 密码换令牌）
- 数据库：MySQL

### 1. 环境准备

- Python 3
- Node.js
- MySQL（已启动）

### 2. 数据库

#### 2.1 建库

库名：`databasename_admin_system_0913`  
字符集：`utf8mb4`

#### 2.2 改配置

文件：`backend/backend/settings.py`

库名、账号在 `DATABASES` 里改成你本机的。

### 3. 启动后端

进入后端目录：

```bash
cd backend
```

第一次需要创建虚拟环境（已有 `backend/env` 则跳过这一步）：

```bash
python -m venv env
```

Windows PowerShell 激活虚拟环境：

```bash
.\env\Scripts\Activate.ps1
```

提示符前面出现 `(env)` 后再安装依赖、建表、创建管理员：

```bash
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

`createsuperuser` 时按提示输入用户名和密码。

后端地址：`http://127.0.0.1:8000/`

接口前缀：`/api/`。不要只打开根地址，没有首页，出现 404 是正常的。

已经建过环境、装过依赖的，下次只要：

```bash
cd backend
.\env\Scripts\Activate.ps1
python manage.py runserver
```

### 4. 启动前端

另开一个终端，进入前端目录：

```bash
cd frontend
npm install
npm run dev
```

已经装过依赖的，下次只要：

```bash
cd frontend
npm run dev
```

浏览器打开：`http://localhost:9528`

登录后默认进入人员概况。Access Token 有效期 2 小时，过期后重新登录即可，数据不会丢。

### 5. 目录说明

```text
公司内部后台管理系统/
  backend/                 Django 项目
    apps/users/            登录、员工、当前登录人、统计
    apps/system/           岗位、部门
    env/                   Python 虚拟环境
    backend/settings.py    数据库、JWT、跨域
  frontend/                Vue 后台
    src/views/system/      员工、岗位、部门页面
    src/views/stats/       人员概况
    src/api/               对应接口
    src/router/index.js    菜单路由
```

### 6. 主要接口

登录成功后，请求头带：`Authorization: Bearer <token>`。

| 说明     | 方法 | 地址 |
| -------- | ---- | ---- |
| 登录     | POST | `/api/login/` |
| 当前登录人 | GET  | `/api/user/info/` |
| 人员概况 | GET  | `/api/dashboard/` |
| 员工     | 增删改查 | `/api/users/` |
| 岗位     | 增删改查 | `/api/roles/` |
| 部门     | 增删改查 | `/api/departments/` |
