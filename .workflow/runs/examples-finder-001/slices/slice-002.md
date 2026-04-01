# slice-002 — `finder path` 与 PathSearch

### 1. 基本信息

- run_id: examples-finder-001
- slice_id: slice-002
- title: `finder path` 子命令、PathSearch、路径行输出与测试
- priority: P1
- owner: AI
- status: verified

### 2. 切片目标

在 slice-001 的 Walker 上实现 **按 basename 的 Python 正则**（`re.search`）与 `--type f|d|a` 过滤；提供 **`finder path`** CLI：解析 `--name`、`--type`、`--max-depth`、根路径；将匹配路径逐行输出至 stdout；非法 `--name` 正则 → stderr + 退出码 **3**；扫描成功完成（含零条路径）→ **0**。实现 **Output 中「纯路径一行一条」** 部分（`path:line:content` 留给 slice-003）。

### 3. 输入依据

- 设计章节：§5.1.2、§6.1、§6.4、§8.2、§8.4、§10.1（path 相关）
- 关联模块：CLI 入口（path 分支）、PathSearch、Walker、Output（路径行）
- 关联接口：`finder path`、名称正则匹配（实现计划 §4）
- 关联数据结构：`PathHit` 或等价（可直接输出字符串路径）
- 前置依赖：**slice-001**（verified）

### 4. 实现边界

#### 4.1 允许修改范围

- `examples/finder`：`path_search`（或等价）、`output`（**仅**路径行格式化函数）、CLI 中与 **`path` 子命令** 相关的解析与编排
- 测试：`finder path` 集成测试、PathSearch 单测、path 用 fixture
- 可扩展 `pyproject` 的 console_scripts 指向 CLI 入口（若 slice-001 未加）

#### 4.2 禁止修改范围

- 不得实现 `finder text` 的匹配逻辑与 `--fixed-strings`（属 slice-003）
- 不得弱化 slice-001 的路径安全校验（仅可调用与复用）
- 不在本切片单独定稿全文 README（slice-004）；但 `--help` 文案须与当前行为一致

### 5. 预期产出

- 代码文件：PathSearch、Output（路径部分）、CLI `path`
- 测试文件：`test_path_search.py`、`test_cli_path.py`（或等价）
- 配置文件：若需调整 entry point
- 其他产物：path 场景 fixture 目录

### 6. 验证要求

- 设计一致性检查：`--name` 对 **basename** 做 `re.search`（§4.1）；成功完成含零输出仍为 0（§8.4）
- 静态检查 / 类型检查：同仓库配置
- 单元测试：非法正则编译失败 → 映射退出码 3 的行为（CLI 或薄封装可测）
- 契约测试：子进程运行 `finder path`，断言退出码与 stdout 行数；`--type` f/d/a；`--max-depth`

### 7. 偏差与升级策略

#### 7.1 允许记录偏差的条件

- Windows 下路径显示格式（绝对/规范化）与 POSIX 差异须在后续 slice-004 README 中说明；本切片实现与注释一致即可

#### 7.2 必须升级人工处理的条件

- 若与 slice-001 的 Walker API 不兼容且需破坏安全约束，须停止并回溯 slice-001 或更新设计

### 8. 完成定义

- [ ] 代码已生成或修改
- [ ] 测试已补齐
- [ ] 自动检查通过
- [ ] 偏差已记录
- [ ] 结果已归档

**Backlog**：B-04（路径行部分）, B-05, B-06；B-13 中 path 用 fixture。
