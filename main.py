from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from rich.console import Console, Group
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text
from rich.rule import Rule
from dotenv import load_dotenv
import os
import sys

load_dotenv()
console = Console()

api_key = os.getenv("NVIDIA_API_KEY")
if not api_key:
    console.print("[bold red]Error: NVIDIA_API_KEY 环境变量未设置。[/bold red]")
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

    reasoning_text = ""
    content_text = ""

    def build():
        parts = []
        if reasoning_text:
            parts.append(Text(reasoning_text, style="dim"))
        if reasoning_text and content_text:
            parts.append(Text(""))
        if content_text:
            parts.append(Markdown(content_text))
        return Group(*parts) if parts else Text("")

    with Live(
        build(),
        console=console,
        refresh_per_second=8,
        vertical_overflow="visible",
    ) as live:
        for chunk in client.stream(messages):
            if chunk.additional_kwargs and "reasoning_content" in chunk.additional_kwargs:
                r = chunk.additional_kwargs["reasoning_content"]
                if r:
                    reasoning_text += r

            if chunk.content:
                content_text += chunk.content   # type: ignore

            live.update(build())

    console.print()
    messages.append(AIMessage(content=content_text))
    return content_text

def main():
    console.print(Rule("[bold cyan] UNLIMITED AI [/bold cyan]"))
    console.print("输入 [bold]exit[/bold] / [bold]quit[/bold] / [bold]q[/bold] 退出\n")

    while True:
        try:
            user_input = console.input("[bold green]> [/bold green]")
        except (EOFError, KeyboardInterrupt):
            console.print("\n[bold]再见！[/bold]")
            break

        stripped = user_input.strip()
        if stripped.lower() in ("exit", "quit", "q"):
            console.print("[bold]再见！[/bold]")
            break

        if not stripped:
            continue

        console.print()
        chat_once(user_input)

if __name__ == "__main__":
    main()