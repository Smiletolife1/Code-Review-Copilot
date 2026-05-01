import subprocess
from typing import Dict
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY")

def ask_llm(system_prompt: str, user_prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

def get_git_diff() -> str:
    result = subprocess.run(["git", "diff"], capture_output=True, text=True)
    return result.stdout

def style_agent(diff: str) -> str:
    return ask_llm("代码规范专家", f"检查代码规范问题:\n{diff}")

def security_agent(diff: str) -> str:
    return ask_llm("安全专家", f"检查安全问题:\n{diff}")

def performance_agent(diff: str) -> str:
    return ask_llm("性能专家", f"检查性能问题:\n{diff}")

def summary_agent(results: Dict[str, str]) -> str:
    return ask_llm("技术负责人", f"总结评审:\n{results}")

def run():
    diff = get_git_diff()
    if not diff.strip():
        print("No changes detected")
        return

    style = style_agent(diff)
    security = security_agent(diff)
    performance = performance_agent(diff)

    summary = summary_agent({
        "style": style,
        "security": security,
        "performance": performance
    })

    with open("report.md", "w", encoding="utf-8") as f:
        f.write("# Code Review Report\n\n")
        f.write(style + "\n\n")
        f.write(security + "\n\n")
        f.write(performance + "\n\n")
        f.write(summary)

    print("Report generated: report.md")

if __name__ == "__main__":
    run()
