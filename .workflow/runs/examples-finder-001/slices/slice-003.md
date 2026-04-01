# slice-003 — `finder text` 与 ContentSearch

### 1. 基本信息

- run_id: examples-finder-001
- slice_id: slice-003
- title: `finder text`、ContentSearch、glob、编码/二进制策略与测试
- priority: P2
- owner: AI
- status: verified

### 2. 切片目标

在 slice-001 Walker 上实现 **按文件逐行** 的内容搜索：**默认正则**；`--regex` 与 `--fixed-strings` 互斥；支持 `--max-depth`、`--glob` / `--glob-exclude`（与设计 §8.1 一致）；输出 **`path:line:content`**（Output 的 TextHit 部分）。固定 **一种** 编码失败策略（跳过或诊断）及二进制启发式 **或** 在代码注释 + 简短开发者说明中与设计 §9.2 一致，完整用户向说明由 slice-004 README 收束。

### 3. 输入依据

- 设计章节：§5.1.1、§6.3、§8.1、§9.2、§10.1（text 相关）
- 关联模块：ContentSearch、CLI（text 分支）、Walker、Output（TextHit 格式化）
- 关联接口：`finder text`、单行内容匹配（实现计划 §4）
- 关联数据结构：`TextHit`（§7.1）
- 前置依赖：**slice-001**（verified）

### 4. 实现边界

#### 4.1 允许修改范围

- `examples/finder`：`content_search`（或等价）、`output`（**追加** TextHit 格式化，与 slice-002 路径格式化共存）、CLI **`text` 子命令**、glob 过滤与 Walker 的组合逻辑
- 测试：ContentSearch 单测、`finder text` 集成测试、text 用 fixture
- 可增 `pyproject` 依赖（保持最少，优先标准库）

#### 4.2 禁止修改范围

- 不得改变 slice-002 已交付的 `finder path` 行为与 CLI 契约（仅可因共享 CLI 框架做无行为变更的重构，须在验证报告中说明）
- 不得删除或弱化路径根下校验
- 全文 README 定稿属 slice-004；本切片须在代码注释中写明编码/二进制策略选择

### 5. 预期产出

- 代码文件：ContentSearch、Output（TextHit）、CLI `text`
- 测试文件：`test_content_search.py`、`test_cli_text.py`（或等价）
- 配置文件：按需
- 其他产物：含特殊字符字面匹配、正则默认的 fixture

### 6. 验证要求

- 设计一致性检查：未指定 `--fixed-strings` 时 pattern 按正则；字面模式下特殊字符不当作正则；零命中退出码 **0**
- 静态检查 / 类型检查：同仓库配置
- 单元测试：至少一种内容匹配；`--fixed-strings` 与默认正则对比
- 契约测试：子进程 `finder text`，非法根/非法 pattern → **3**（若在本切片暴露）

### 7. 偏差与升级策略

#### 7.1 允许记录偏差的条件

- 单行长度上限常数取值可在合理范围内实现，须在注释标明；超长行截断策略与 §6.3 一致

#### 7.2 必须升级人工处理的条件

- 编码策略无法二选一并写清时，或 glob 与 Walker 组合导致路径逃逸风险时，须停止并更新风险/设计

### 8. 完成定义

- [ ] 代码已生成或修改
- [ ] 测试已补齐
- [ ] 自动检查通过
- [ ] 偏差已记录
- [ ] 结果已归档

**Backlog**：B-04（TextHit 格式化部分）, B-07, B-08, B-09, B-10；B-13 中 text 用 fixture。
