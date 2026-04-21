# unlimited AI

**AI 又不傻，为什么要限制它呢？**

 - sys_prompt1 和 sys_prompt2 是适合 llama 系列和 glm 系列的模型
 - sys_prompt3 是适合 gpt-oss 系列的模型

## 使用方法
1. 克隆本仓库并安装依赖

```bash
git clone https://github.com/sglwsjxh/unlimited-ai.git
cd unlimited-ai

python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

pip install openai
```

2. 设置用户 API
 - 从 [NVIDIA AI 平台](https://build.nvidia.com/settings/api-keys) 获取 API Key
 - 设置环境变量

```bash
cp .env.example .env

# 编辑 .env 文件，将 NVIDIA_API_KEY 的值替换为你的 API Key
```

> 可以在 main.py 中修改 sys_prompt 来适配不同的模型，或者自己设计 sys_prompt 来适配你自己的模型

## 开源协议
MIT License