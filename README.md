# 🥳 Birthday Calendar & Reminder (生日日历与提醒)

这是一个基于 FastAPI 构建的生日日历和提醒应用程序，支持公历和农历生日，并通过企业微信机器人发送提醒。它提供了一个简单的 Web 界面来管理生日信息。

## 1 ✨ 功能特性

*   **生日管理：** 轻松添加、查看和删除生日信息。
*   **多日历支持：** 同时支持公历 (Gregorian) 和农历 (Lunar) 生日。
*   **灵活提醒：** 为每个生日设置多个提醒时间点。
*   **企业微信通知：** 通过配置企业微信群机器人 Webhook URL，在生日到来时自动发送通知。
*   **Web 用户界面：** 直观的网页界面，方便用户操作。
*   **Docker 化部署：** 提供 `Dockerfile` 和 `docker-compose.yml`，简化部署流程。
<img width="2160" height="1308" alt="image" src="https://github.com/user-attachments/assets/db912462-bd36-4974-9727-61d64f3153fe" />
<img width="1284" height="329" alt="image" src="https://github.com/user-attachments/assets/189434a1-2bd6-4204-9b0e-7bf54c50481a" />
![a2ed8902856bc0639fe6e396eafc01d1](https://github.com/user-attachments/assets/76245c7f-bf5e-4b68-bc62-2b54b17c3407)

## 2 🚀 技术栈

*   **后端框架：** [FastAPI](https://fastapi.tiangolo.com/) (Python)
*   **数据库：** [SQLite](https://www.sqlite.org/index.html)
*   **ORM：** [SQLAlchemy](https://www.sqlalchemy.org/) (异步支持)
*   **后台任务调度：** [APScheduler](https://apscheduler.readthedocs.io/)
*   **模板引擎：** [Jinja2](https://jinja.palletsprojects.com/)
*   **前端：** [Bootstrap](https://getbootstrap.com/) (用于 UI 样式)
*   **容器化：** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)

## 3 🛠️ 部署指南

本项目推荐使用 Docker 和 Docker Compose 进行部署。

### 3.1 前提条件

*   [Git](https://git-scm.com/): 用于克隆代码仓库。
*   [Docker](https://docs.docker.com/get-docker/): 容器化平台。
*   [Docker Compose](https://docs.docker.com/compose/install/): 用于管理多容器 Docker 应用。

### 3.2 本地开发或服务器部署

1.  **克隆代码仓库：**

    ```bash
    git clone https://github.com/Subwoofer91/birthday_calendar.git
    cd birthday_calendar
    ```

2.  **配置环境变量 (`.env`)：**
    在项目根目录下创建一个名为 `.env` 的文件，用于存储敏感信息和配置。其中最重要的是企业微信机器人的 Webhook URL。

    ```ini
    # .env 文件示例
    # 
    # 企业微信机器人 Webhook URL
    # 你需要从你的企业微信群机器人设置中获取此 URL。
    # 格式通常为：https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_ROBOT_KEY
    WECOM_WEBHOOK_URL="YOUR_WECOM_WEBHOOK_URL"

    # 可选：如果需要设置时区，例如亚洲/上海
    # TZ="Asia/Shanghai" 
    ```
    请将 `YOUR_WECOM_WEBHOOK_URL` 替换为你实际的 Webhook URL。

3.  **使用 Docker Compose 启动服务：**
    运行以下命令来构建 Docker 镜像并启动容器。

    ```bash
    docker compose up -d --build
    ```
    *   `-d` 参数表示在后台运行容器。
    *   `--build` 参数确保 Docker 重新构建镜像 (如果你修改了 `Dockerfile` 或 `requirements.txt`)。

4.  **访问应用程序：**
    应用程序默认会在容器的 `8000` 端口运行。
    *   **本地开发：** 在浏览器中访问 `http://localhost:8000`
    *   **服务器部署：** 在浏览器中访问 `http://你的服务器公网IP:8000`

    **注意：** 如果你在云服务器上部署，请确保你的服务器防火墙或云服务商的安全组已开放 `8000` 端口的入站流量。

## 4 🖥️ 使用说明

1.  **访问主页：** 打开浏览器，导航到应用程序地址 (`http://localhost:8000` 或 `http://你的服务器公网IP:8000`)。
2.  **添加生日：**
    *   在页面底部的表单中填写生日信息（姓名、公历日期、农历日期等）。
    *   你可以通过点击 "添加提醒" 按钮为该生日设置多个提醒时间（例如，生日当天、生日提前一天等）。
3.  **查看生日：** 页面会显示即将到来的生日列表。
4.  **删除生日：** 点击生日旁边的 "删除" 按钮可以移除对应的生日记录。

## 5 📂 项目结构

```
.
├── .env                  # 环境变量配置文件 (部署时创建)
├── birthdays.db          # SQLite 数据库文件 (由应用自动创建和管理)
├── docker-compose.yml    # Docker Compose 配置文件
├── Dockerfile            # Docker 镜像构建文件
├── requirements.txt      # Python 依赖列表
└── app/                  # 应用程序核心代码
    ├── __init__.py
    ├── crud.py           # 数据库操作 (CRUD) 逻辑
    ├── database.py       # 数据库连接和会话管理
    ├── main.py           # FastAPI 主应用，定义路由和启动逻辑
    ├── models.py         # SQLAlchemy 数据库模型
    ├── scheduler.py      # 后台任务调度 (检查生日提醒)
    ├── schemas.py        # Pydantic 数据验证模型
    ├── utils.py          # 工具函数 (如日期计算、发送通知)
    └── templates/        # Jinja2 网页模板
        ├── base.html
        └── index.html    # 主页界面
```

## 6 🤝 贡献

欢迎任何形式的贡献！如果你有任何建议、功能请求或 bug 报告，请随时提交 Issue 或 Pull Request。

## 7 📄 许可证

MIT
