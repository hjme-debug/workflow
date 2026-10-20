import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL") or None,
)

MODEL = os.getenv("MODEL", "deepseek-chat")


def ask_llm(prompt):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


def clean_code(text):
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines)
    return text


def coding_agent(state):
    print("\n[编码 Agent] 根据需求生成初始代码...")
    prompt = f"""
You are a coding agent. Write Python code for the following requirement:
{state['requirement']}
Return only the code, no explanation.
"""
    state["code"] = clean_code(ask_llm(prompt))
    return state


def review_agent(state):
    print("\n[审查 Agent] 正在审查代码...")
    prompt = f"""
You are a code review agent. Review the following Python code.
Return a JSON object with:
- "passed": true or false
- "issues": a list of strings describing problems

Code:
{state['code']}
"""
    raw = ask_llm(prompt).replace("```json", "").replace("```", "").strip()
    try:
        data = json.loads(raw)
        state["passed"] = bool(data.get("passed", False))
        state["issues"] = data.get("issues", [])
    except Exception:
        state["passed"] = False
        state["issues"] = ["无法解析审查结果"]
    return state


def fix_agent(state):
    print("\n[修复 Agent] 根据审查意见修复代码...")
    prompt = f"""
You are a fix agent. Fix the following Python code based on the review issues.
Original code:
{state['code']}

Issues:
{state['issues']}

Return only the fixed code, no explanation.
"""
    state["code"] = clean_code(ask_llm(prompt))
    state["iteration"] += 1
    return state


def run_workflow():
    state = {
        "requirement": "写一个 Python 函数 divide(a, b)，处理除以 0 的情况，返回友好提示。",
        "code": "",
        "passed": False,
        "issues": [],
        "iteration": 0,
        "max_iterations": 3,
    }

    state = coding_agent(state)
    print("初始代码：\n", state["code"])

    while not state["passed"] and state["iteration"] < state["max_iterations"]:
        state = review_agent(state)
        print(f"审查通过？ {state['passed']}")
        print("问题：", state["issues"])

        if not state["passed"]:
            state = fix_agent(state)
            print("修复后代码：\n", state["code"])

    print("\n" + "=" * 50)
    print("最终代码：\n", state["code"])
    print("最终审查状态：", "通过" if state["passed"] else "未通过")
    print("剩余问题：", state["issues"])
    print("=" * 50)


if __name__ == "__main__":
    run_workflow()