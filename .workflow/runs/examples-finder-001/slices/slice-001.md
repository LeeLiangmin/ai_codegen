# slice-001 — 公共类型、路径安全与 Walker

### 1. 基本信息

- run_id: examples-finder-001
- slice_id: slice-001
- title: 公共类型、路径规范化/根下校验、Walker（深度、默认不跟随 symlink）
- priority: P0
- owner: AI
- status: verified

### 2. 切片目标

交付最小可验证的**遍历内核**：`SearchOptions`/`SearchRoot` 等与 §7.1 对齐的数据结构；根路径解析、规范化及「路径必须留在根子树内」的校验 API；在 `maxDepth` 与 `followSymlinks=false`（默认）下安全枚举文件系统节点，并具备供后续切片使用的迭代接口（生成器或等价）。不包含 `finder path`/`finder text` 子命令与内容匹配。

### 3. 输入依据

- 设计章节：`finder.normalized.md` §4.1、§4.2、§6.2、§7.1、§9.2（遍历相关）、§12.1 Slice A
- 关联模块：公共类型与选项、Walker；路径校验（与 CLI 启动校验共享逻辑）
- 关联接口：路径规范化与根下校验；Walker 迭代协议（实现计划 §4）
- 关联数据结构：`SearchRoot`、`SearchOptions`（及后续 `PathHit`/`TextHit` 类型定义可一并落地为 dataclass/TypedDict 等，供后续切片引用）
- 前置依赖：无

### 4. 实现边界

#### 4.1 允许修改范围

- `examples/finder/` 下包目录：新建 `pyproject.toml`（若尚无）、包源码中 **`types`/`models`、`paths`（或 `pathutil`）、`walker`（或等价命名）** 模块
- 测试：`examples/finder/tests/`（或仓库约定路径）中 **仅** Walker、路径校验、类型相关的单测
- 测试 fixture：仅服务于本切片验证的目录树（深度、不跟随 symlink、树外 symlink 等）

#### 4.2 禁止修改范围

- 不得实现 `finder path` / `finder text` 的完整 CLI 子命令（可保留占位入口由后续切片替换）
- 不得实现 PathSearch、ContentSearch、完整 Output（允许占位模块空文件若利于包结构）
- 不得编写面向最终用户的 `README.md` 完整稿（slice-004 负责）；本切片可在代码注释中简述编码策略占位

### 5. 预期产出

- 代码文件：`examples/finder` 内类型定义、路径工具、Walker 实现
- 测试文件：`test_paths.py`、`test_walker.py`（或合并为清晰模块）
- 配置文件：`pyproject.toml` / 包布局（若本切片首次建立）
- 其他产物：无

### 6. 验证要求

- 设计一致性检查：默认不跟随 symlink；深度从根为 0；join 后校验仍在根下（§4.1、§6.2）
- 静态检查：与 `pyproject` 中已配置工具一致（若尚无，slice-004 可补；本切片至少保证 `python -m compileall` 通过）
- 类型检查：若已启用 mypy/pyright，须通过；未启用则跳过
- 单元测试：根不存在/非目录的校验行为（供 CLI 映射码 3 的**库层**行为）；深度边界；不跟随 symlink 时不逃逸出根；权限不足时跳过或警告策略与实现注释一致
- 契约测试：本切片无 CLI 契约；可选对 Walker 生成路径序列做快照式断言

### 7. 偏差与升级策略

#### 7.1 允许记录偏差的条件

- Walker API 形态（生成器 vs 回调）可与计划字面不同，但须被 slice-002/003 消费且不弱化安全校验

#### 7.2 必须升级人工处理的条件

- 无法在不大改设计的前提下实现「不跟随 symlink 仍防止路径逃逸」时，须暂停并更新 `risks.md` / 人工确认

### 8. 完成定义

满足以下条件方可标记完成：

- [ ] 代码已生成或修改
- [ ] 测试已补齐
- [ ] 自动检查通过（本切片范围内）
- [ ] 偏差已记录（`state.md` 或验证报告）
- [ ] 结果已归档（`slice-verify` 报告路径后续写入）

**Backlog**：B-01, B-02, B-03；B-13 中与 Walker/深度/symlink 相关的 fixture。
