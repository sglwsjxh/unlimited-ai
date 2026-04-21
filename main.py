from openai import OpenAI
import os
import sys

_USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
_REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
_RESET_COLOR = "\033[0m" if _USE_COLOR else ""

try:
    with open("api_key.txt", "r", encoding="utf-8") as f:
        api_key = f.read().strip()
except FileNotFoundError:
    print("[-] 错误：未找到 api_key.txt 文件。请在项目根目录下创建一个名为 api_key.txt 的文件，并将您的 API 密钥粘贴到其中")
    sys.exit(1)

client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = api_key
)

with open("sys_prompt3.txt", "r", encoding="utf-8") as f:
    sys_prompt = f.read()

user_prompt = input("请输入你的问题：\n")
print()

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {"role":"system","content":sys_prompt},
        {"role":"user","content":user_prompt}
    ],
    temperature=1,
    top_p=1,
    max_tokens=16384,
    stream=True,
    extra_body={"chat_template_kwargs":{"enable_thinking":True,"clear_thinking":False}}
)

printed_reasoning = False
printed_separator = False

for chunk in completion:
    if not getattr(chunk, "choices", None):
        continue
    if len(chunk.choices) == 0 or getattr(chunk.choices[0], "delta", None) is None:
        continue
    delta = chunk.choices[0].delta
    reasoning = getattr(delta, "reasoning_content", None)
    if reasoning:
        print(f"{_REASONING_COLOR}{reasoning}{_RESET_COLOR}", end="")
        printed_reasoning = True
    if getattr(delta, "content", None) is not None:
        if printed_reasoning and not printed_separator:
            print("\n\n", end="")
            printed_separator = True
        print(delta.content, end="")