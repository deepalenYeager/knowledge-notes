# 本地知识盲点管理系统

前后端分离的个人笔记应用。

## 运行后端

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

SQLite 数据库默认存放在 `data/knowledge.db`，启动时会自动创建表。

## 运行前端（开发模式）

```bash
cd frontend
npm install
npm run dev
```

Vite 已配置 `/api` 代理到 `http://localhost:8000`。

## 前端构建并由后端托管（可选）

```bash
cd frontend
npm run build
# 之后直接运行 uvicorn，FastAPI 会从 frontend/dist 提供静态文件
```

## 主要功能

- 知识点增删改查、富文本正文（Quill）
- 标题/正文模糊搜索、标签过滤、按更新时间倒序
- 标签统计 `/api/tags`，数据导出 `/api/export`

