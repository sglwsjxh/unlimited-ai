from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
import sys

_USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
_REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
_RESET_COLOR = "\033[0m" if _USE_COLOR else ""

api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    print("Error: NVIDIA_API_KEY environment variable not set.")
    sys.exit(1)

with open("sys_prompt3.txt", "r", encoding="utf-8") as f:
    sys_prompt = f.read()

client = ChatNVIDIA(
    model="openai/gpt-oss-120b",
    api_key=api_key,
    temperature=1,
    top_p=1,
    max_completion_tokens=16384,
    model_kwargs={
        "chat_template_kwargs": {
            "enable_thinking": True,
            "clear_thinking": False,
        }
    },
)

messages: list = [SystemMessage(content=sys_prompt)]

def chat_once(user_input: str) -> str:
    global messages

    messages.append(HumanMessage(content=user_input))

    printed_reasoning = False
    printed_separator = False
    full_content = ""

    for chunk in client.stream(messages):
        if chunk.additional_kwargs and "reasoning_content" in chunk.additional_kwargs:
            reasoning = chunk.additional_kwargs["reasoning_content"]
            if reasoning:
                print(
                    f"{_REASONING_COLOR}{reasoning}{_RESET_COLOR}",
                    end="",
                    flush=True,
                )
                printed_reasoning = True

        if chunk.content:
            if printed_reasoning and not printed_separator:
                print("\n\n", end="", flush=True)
                printed_separator = True
            print(chunk.content, end="", flush=True)
            full_content += chunk.content # type: ignore

    print("\n")

    messages.append(AIMessage(content=full_content))
    return full_content

def main():
    print("=== UNLIMITED AI 对话 ===")
    print("输入 exit / quit / q 退出\n")

    while True:
        try:
            user_input = input("请输入你的问题：")
        except (EOFError, KeyboardInterrupt):
            print("\n再见！")
            break

        stripped = user_input.strip()
        if stripped.lower() in ("exit", "quit", "q"):
            print("再见！")
            break

        if not stripped:
            continue

        print()
        chat_once(user_input)

if __name__ == "__main__":
    main()