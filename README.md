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

2. 在根目录下创建一个名为 `api_key.txt` 的文件，并从 [NVIDIA AI 平台](https://build.nvidia.com/settings/api-keys) 获取 API Key，粘贴到 `api_key.txt` 中并保存。

> 可以在 main.py 中修改 sys_prompt 来适配不同的模型，或者自己设计新的 sys_prompt 来适配你喜欢的模型

## 开源协议
MIT License