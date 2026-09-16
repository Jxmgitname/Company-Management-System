# 公司内部后台管理系统（前端）

Vue2 + Element UI。页面在 `src/views/`（登录、员工、岗位、部门、人员概况）。

完整启动步骤看仓库根目录的 `README.md`。这里只记前端注意点。

## 启动

先保证后端 `python manage.py runserver` 已开着。再进入 `frontend` 目录：

```bash
npm install
npm run dev
```

已经装过依赖的，下次只要：

```bash
npm run dev
```

浏览器打开：`http://localhost:9528`

开发时代理：请求 `/dev-api` 会转到后端 `http://127.0.0.1:8000`。

登录后默认进入人员概况。

## 页面

- 登录：`src/views/login/`
- 员工 / 岗位 / 部门：`src/views/system/`
- 人员概况：`src/views/stats/`
- 接口：`src/api/`
- 菜单路由：`src/router/index.js`
