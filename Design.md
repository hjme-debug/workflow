设计文档



架构

三个 Agent 顺序执行，共享一个 state 字典。



流程图

\[需求] → \[编码 Agent] → \[审查 Agent] → (通过?) → 是 → \[输出]

&#x20;                           ↑                ↓ 否

&#x20;                           └── \[修复 Agent] ←┘



状态管理

state 包含：

\- requirement：需求描述

\- code：当前代码

\- passed：审查是否通过

\- issues：审查发现的问题列表

\- iteration：当前迭代次数

\- max\_iterations：最大迭代次数



Agent 通信

每个 Agent 读取 state 中的字段，处理后再写回 state。审查 Agent 设置 passed 和 issues，主流程根据 passed 决定是否调用修复 Agent。



可扩展性

\- 新增 Agent：只需增加一个函数，并在主流程中调用。

\- 修改流程：调整 run\_workflow 中的顺序和条件。

\- 支持并行：可将独立 Agent 放入线程。

