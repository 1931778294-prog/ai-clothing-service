# 简衣服饰 · AI 智能电商客服系统

> **在线体验（点开即用，无需安装）：https://1931778294-prog.github.io/ai-clothing-service/**

基于大模型（DeepSeek）的电商服装店智能客服，可直接多轮对话，覆盖**商品咨询、多轮尺码推荐、售后政策、优惠计算、超纲拒答、情绪识别与人工转接**等真实电商客服场景。

业务原型最初在 Coze（扣子）平台完成 Prompt 与知识库验证，后因平台额度限制，独立用 **DeepSeek API + FastAPI** 重写为端到端、可自主部署的完整项目，并提供一个**零服务器成本、可公网访问的在线 Demo**。

---

## 一、在线 Demo 怎么跑起来的（架构）

项目包含两种等价实现，共用同一套「系统提示词 + 店铺知识库」与对话逻辑：

### 1. 在线版（当前部署，免服务器）
```
浏览器 (docs/index.html)
   │  组装：系统提示词(知识库) + 最近10轮历史 + 本轮问题
   │  直接 HTTPS 调用（已验证 DeepSeek 支持 CORS）
   ▼
DeepSeek 大模型 API ──► 严格按知识库回答
```
- 托管：**GitHub Pages**（免费、免备案）
- 纯前端单文件，无需后端服务器
- 密钥支持 `localStorage` 覆盖，不写死依赖

### 2. 后端版（生产级写法，`main.py`）
```
浏览器 (static/index.html)
   │  POST /chat {message, history}（同源，无跨域问题）
   ▼
FastAPI 后端 (main.py)
   │  组装消息 + 密钥中转（DEEPSEEK_API_KEY 只存服务端环境变量）
   ▼
DeepSeek 大模型 API
```
- 密钥不暴露给浏览器，是生产环境的标准做法
- 单 FastAPI 服务同时托管页面与接口，提供 `Dockerfile`，可部署到任意容器平台

> **工程权衡说明**：在线 Demo 为零服务器成本采用浏览器直连；生产环境应使用 `main.py` 后端版，把 API Key 留在服务端并设置用量上限。

---

## 二、核心功能

- **商品知识问答**：6 款服饰的价格、颜色、尺码、材质、发货信息，严格依据内置知识库回答
- **多轮尺码推荐**：先主动询问身高体重，结合上下文与尺码表给出推荐尺码和理由
- **售后政策解答**：7 天无理由、质量问题、换货运费等规则分点输出
- **优惠计算**：新客立减、满 199 减 15、满 299 减 30 的组合计算
- **防幻觉约束**：知识库之外的问题明确拒答并引导人工，不编造
- **情绪识别 / 转人工**：识别投诉、退款争议等场景，固定话术 + 自动生成工单要点
- **多轮上下文**：前端维护最近 10 轮历史，支持连续追问（如尺码多轮推荐）

---

## 三、技术栈

| 层 | 技术 |
|---|---|
| 大模型 | DeepSeek（deepseek-chat），OpenAI 兼容接口，temperature 0.3 |
| 后端 | Python + FastAPI + Uvicorn（`main.py`） |
| 前端 | 原生 HTML + TailwindCSS，聊天界面、快捷提问、打字动效 |
| 在线部署 | GitHub Pages（`docs/` 目录） |
| 容器化 | Dockerfile（兼容 7860 / 平台注入 PORT） |

---

## 四、目录结构

```
ai-clothing-service/
├── docs/index.html      # 在线版（GitHub Pages 部署，浏览器直连 DeepSeek）
├── static/index.html    # 后端版前端页面
├── main.py              # FastAPI 后端（系统提示词+知识库、/chat、密钥走环境变量）
├── api/index.py         # Vercel Serverless 入口（备选部署方式）
├── requirements.txt
├── Dockerfile
├── test_api.py          # 8 个场景的自动化测试脚本
└── README.md
```

---

## 五、本地运行（后端版）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置密钥（.env 文件，不会被提交）
echo DEEPSEEK_API_KEY=你的DeepSeek密钥 > .env

# 3. 启动
python main.py
# 打开 http://127.0.0.1:8000
```

## 六、Docker 部署

```bash
docker build -t jianyi-kefu .
docker run -p 7860:7860 -e DEEPSEEK_API_KEY=你的密钥 jianyi-kefu
```
