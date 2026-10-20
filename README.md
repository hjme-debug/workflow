三 Agent 代码审查 Workflow



简介

本项目实现了一个简单的三 Agent 协作 Workflow：编码 Agent → 审查 Agent → 修复 Agent。所有 Agent 通过共享 state 字典通信。



功能

\- 编码 Agent：根据需求生成 Python 代码

\- 审查 Agent：审查代码，输出是否通过和问题列表

\- 修复 Agent：根据审查意见修复代码

\- 状态共享：三个 Agent 共用一个 state 字典

\- 流程控制：顺序执行 + 条件循环（最多 3 次）

\- 最终输出：修复后的代码和审查结果



环境要求

\- Python 3.10+

\- DeepSeek / OpenAI 兼容 API Key



安装依赖

pip install -r requirements.txt



配置

复制 .env.example 为 .env，填入你的 API Key：

OPENAI\_API\_KEY=你的key

OPENAI\_BASE\_URL=https://api.deepseek.com

MODEL=deepseek-chat



运行

python workflow.py



项目结构

mini-workflow-3agents/

&#x20; workflow.py          主程序

&#x20; requirements.txt     依赖包

&#x20; README.md            说明文档

&#x20; Design.md            设计文档

&#x20; .env.example         环境变量模板





