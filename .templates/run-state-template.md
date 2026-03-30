# Run 状态文件模板

## 1. 基本信息

- run_id:
- name:
- objective:
- design_doc:
- created_at:
- updated_at:
- status: created / intake / normalized / planned / sliced / implementing / verifying / curated / closed / failed

## 2. 当前阶段

- current_stage:
- current_slice:
- stage_owner:
- retry_count:

## 3. 阶段结果摘要

| stage | status | input | output | checks | notes |
| --- | --- | --- | --- | --- | --- |
| intake | pending |  |  |  |  |
| normalize | pending |  |  |  |  |
| plan | pending |  |  |  |  |
| slice | pending |  |  |  |  |
| implement | pending |  |  |  |  |
| verify | pending |  |  |  |  |
| curate | pending |  |  |  |  |
| close | pending |  |  |  |  |

## 4. 切片状态

| slice_id | title | status | dependency | verify_status | deviation | notes |
| --- | --- | --- | --- | --- | --- | --- |
|  |  | pending |  | pending | none |  |

## 5. 风险与阻塞

- 当前风险：
- 当前阻塞：
- 是否需要人工介入：yes / no
- 人工介入原因：

## 6. 产物索引

- implementation_plan:
- slices_index:
- verification_reports:
- traceability_matrix:
- final_index:

## 7. 恢复策略

- 最近成功阶段：
- 可恢复起点：
- 恢复前置条件：
- 恢复说明：
