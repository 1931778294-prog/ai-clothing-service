# 简衣服饰 · AI 智能电商客服系统

基于大模型（DeepSeek）+ FastAPI 的电商服装店智能客服，可直接对话，覆盖商品咨询、多轮尺码推荐、售后政策、优惠计算、超纲拒答、情绪识别与人工转接等真实电商客服场景。

> 前期在 Coze（扣子）平台完成业务原型与 Prompt 验证，后因平台额度限制，独立用 DeepSeek API + FastAPI 重写为端到端、可自主部署的完整 Demo。

## 在线体验

部署后访问 Render 公网地址即可（打开就是客服界面，无需安装任何东西）。

## 技术栈

- **大模型**：DeepSeek（deepseek-chat），OpenAI 兼容接口
- **后端**：Python + FastAPI + Uvicorn，负责对话接口、多轮历史组装、密钥中转
- **前端**：原生 HTML + TailwindCSS，聊天界面、快捷提问、打字动效
- **部署**：Render（Web Service），单服务同时托管页面与接口

## 系统架构

```
浏览器 (index.html)
   │  POST /chat {message, history}
   ▼
FastAPI 后端 (main.py)
   │  组装：系统提示词(店铺知识库) + 最近10轮历史 + 本轮问题
   ▼
DeepSeek 大模型 API ──► 严格按知识库回答，返回客服回复
```

## 核心功能

1. **商品知识问答**：6 款服饰的价格、颜色、尺码、材质、发货信息，严格依据内置知识库回答
2. **多轮尺码推荐**：先主动询问身高体重，结合上下文与尺码表给出推荐尺码和理由
3. **售后政策解答**：7 天无理由、质量问题、换货运费等规则分点输出
4. **防幻觉约束**：知识库之外的问题明确拒答并引导人工，不编造信息
5. **情绪识别 + 人工转接**：识别投诉/激动情绪，先安抚再转人工，并自动生成工单要点
6. **多轮上下文记忆**：前端携带对话历史，后端只保留最近 10 轮以控制 token
7. **密钥安全**：API Key 仅通过环境变量读取，`.env` 被 `.gitignore` 排除，不进公开仓库

## 目录结构

```
ai-clothing-service/
├── main.py              # FastAPI 后端：/chat 接口 + 系统提示词/知识库
├── static/
│   └── index.html       # 客服聊天前端
├── test_api.py          # 8 场景自动化测试脚本
├── requirements.txt
├── .env.example         # 环境变量模板（复制为 .env 填 Key）
└── .gitignore
```

## 本地运行

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 Key：复制 .env.example 为 .env，填入 DeepSeek API Key
#    DEEPSEEK_API_KEY=sk-xxxx

# 3. 启动
python main.py

# 4. 浏览器打开
http://127.0.0.1:8000
```

## 自动化测试

保持服务运行，另开终端执行：

```bash
python test_api.py
```

覆盖 8 个场景：商品查询、尺码多轮推荐、售后、超纲拒答、投诉转人工、优惠计算、物流咨询。

## Render 部署要点

- Build Command：`pip install -r requirements.txt`
- Start Command：`uvicorn main:app --host 0.0.0.0 --port $PORT`
- 环境变量：`DEEPSEEK_API_KEY` = 你的 Key
- 免费实例闲置会休眠，首次访问约 30-60 秒唤醒，面试前提前打开一次即可
