# 待确认项清单 — examples-finder-001

与 `.workflow/docs/design/finder.normalized.md` 对照：**当前无开放 [待确认] 占位**（v0.4）。

---

## 已决策（人工）

| ID | 项 | 决策 |
| --- | --- | --- |
| U-01 | 语言与包管理 | **Python 3.10+**，**uv** |
| U-02 | `finder text` 默认匹配 | **正则**（默认等价 `--regex`）；`--fixed-strings` 字面 |
| U-03 | `finder path --name` | **正则**，basename `re.search`；编译失败 → 3 |
| U-04 | SIGINT 退出码 | **Unix / Unix 类：130**；Windows 以实现为准，README 说明 |
| （退出码） | 成功完成（含零输出） | **0** |

---

## 历史记录（已被新决策取代）

| 原记录 | 说明 |
| --- | --- |
| 无匹配时退出码 1 | §8.4 已改为成功完成 **0** |
| SIGINT 码未定义 | v0.4：Unix **130** |
