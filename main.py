"""
unlimited-ai - 基于 LangChain 的命令行聊天客户端
Copyright (C) 2026 清木殇

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from langchain_openai import ChatOpenAI
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
console.clear()

base_url = os.getenv("BASE_URL")
if not base_url:
    console.print("[bold red]Error: BASE_URL 环境变量未设置。[/bold red]")
    sys.exit(1)

api_key = os.getenv("API_KEY")
if not api_key:
    console.print("[bold red]Error: API_KEY 环境变量未设置。[/bold red]")
    sys.exit(1)

model_name = os.getenv("MODEL_NAME") or os.getenv("MODAL_NAME")
if not model_name:
    console.print("[bold red]Error: MODEL_NAME 或 MODAL_NAME 环境变量未设置。[/bold red]")
    sys.exit(1)

sys_prompt_file = os.getenv("SYS_PROMPT_FILE")
if not sys_prompt_file:
    console.print("[bold red]Error: SYS_PROMPT_FILE 环境变量未设置。[/bold red]")
    sys.exit(1)

with open(sys_prompt_file, "r", encoding="utf-8") as f:
    sys_prompt = f.read()

client = ChatOpenAI(
    model=model_name,
    api_key=api_key,
    base_url=base_url,
    temperature=1,
    top_p=0.95
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
