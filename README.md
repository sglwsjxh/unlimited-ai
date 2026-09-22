# unlimited AI

TUI 中的无限制的 AI 对话，支持 OpenAI 兼容格式的自定义 API
支持**langchain 多轮对话**，**rich 流式渲染markdown**

**AI 又不傻，为什么要限制它呢？**

 - sys_prompt 最新的版本，适合大多数大语言模型，效果较为强烈
 - sys_prompt1 适合 llama 系列的模型
 - sys_prompt2 适合 glm 系列的模型
 - sys_prompt3 适合 gpt-oss 系列的模型

## 使用方法
1. 克隆本仓库并安装依赖

```bash
git clone https://github.com/sglwsjxh/unlimited-ai.git
cd unlimited-ai

python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

2. 设置用户 API
 - 复制 `.env.example` 为 `.env`
 - 填写兼容 OpenAI Chat Completions API 的地址、API Key 和模型名

```bash
cp .env.example .env
```

> 可以在 `.env` 文件中修改 `SYS_PROMPT_FILE` 来适配不同的模型，或者自己设计 sys_prompt 来适配你自己的模型

## 开源协议
MIT License
