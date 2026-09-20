---
name: amazon-listing-penalty-audit
description: 按亚马逊 Listing 的 7 个隐性减分项体检美国站 ASIN，并给出可粘贴的字段/标题/五点/ALT/Search Terms 改法。在用户要检查 Listing 静默降权、尺寸不一致、变体错配、Browse Node、图片 ALT、Search Terms 竞品品牌、描述与实物不符、30 天频繁调价，或输入 /listing-audit、/penalty-audit、/隐性减分 时使用。不要用于从零写新 Listing、选品调研或纯评论分析。
metadata:
  short-description: 7项隐性减分体检并输出可粘贴改法
---

# Amazon Listing 7项隐性减分体检

对指定站点 ASIN（默认 US）做 **静默降权体检**，不是写新 Listing，也不是竞品调研。

核心原则：A9 对 Listing 是综合判定，不是累加。字段自相矛盾不会报警，但会少给展示、提高 “Item not as described” 退货，再反向压权重。

## 何时用 / 何时不用

**用：** 用户给了 ASIN，要查为什么排名上不去、要按 7 个减分项逐条修、要可粘贴改法、要覆盖全部颜色/尺寸变体。

**不用：** 从零写标题五点（转 `amazon-listing-builder`）；选品/关键词挖掘（转对应调研 skill）；只分析评论痛点（转 `review-analysis`）。

## 必做流程

1. 收齐证据后再下结论。缺后台字段就标 `DATA_MISSING`，不要编。
2. 7 项全部打分，再给改法。不要只评不改，也不要只改不说明原因。
3. **每个子 ASIN 都要改**，不要只改用户点名的那一个颜色。
4. 数字以可测量证据为准：属性栏、A+、主图标注、五点必须同一套数。
5. 输出必须能直接粘贴到 Seller Central。

先读 [references/seven-items.md](references/seven-items.md) 拿判定标准。收集数据时读 [references/evidence-collection.md](references/evidence-collection.md)。写标题/五点/ALT/ST 时读 [references/copy-rules.md](references/copy-rules.md)。出报告时用 [references/report-template.md](references/report-template.md)。非显然判定（尺寸图 vs 属性栏、图文数字打架、变体图顺序不同）对照 [references/example-B0FG6TJJGN.md](references/example-B0FG6TJJGN.md)。

## 7 项（按影响从高到低）

| # | 项 | 影响 | 前端能否判死 |
|---|---|---|---|
| 1 | Size / Weight / Dimensions 多处不一致 | 高 | 能 |
| 2 | Variation theme 与真实差异错配 | 高 | 主题能；文案对齐能 |
| 3 | Browse node 多选或错选 | 中高 | 前台主节点能；后台完整节点 `DATA_MISSING` |
| 4 | 图片 ALT 空白或中文 | 低 | 大概率能（看 colorImages / 实图） |
| 5 | Search Terms 埋竞品品牌或 ASIN | 高 | 前台文案能；ST 本身 `DATA_MISSING`，给整段替换 |
| 6 | 描述/图片数字与实物不符 | 中高 | 内部矛盾能；实物未量则标待复核 |
| 7 | 30 天改价超过 5 次 | 中高 | Keepa 能近似 |

优先修 **高影响 + 低难度**：#1、#3、#5。不要同一天大改英雄子体标题 + 主图 + 五点。

## 铁律

- 禁止把竞品品牌、竞品 ASIN、best、#1、free shipping 写入标题/五点/ST/ALT。
- 禁止把刀片机写成 burr，禁止无证据写 wet grinding、dishwasher safe、具体功率。
- 禁止编造重量、功率、实验室噪音。没有铭牌/实测就留空并写清要用户补。
- 标题已有稳定小类排名的英雄子体，默认 **不改标题**，只把其他变体标题靠过去。
- 变体主题正确但文案分裂，判定为第 2 项“主题通过、内容不通过”，不要拆组。
- 尺寸以卡尺为准；若无卡尺，优先用 **主图尺寸标注**，而不是属性栏里看起来更整的数字。
- 杯数、分贝、尺寸只要出现在图上，就必须和五点/A+/属性一致。打架时取可测量或更保守的那套，并改掉其余位置。
- Search Terms：美国站 ≤249 字节，空格分隔，全小写，不重复前台词。后台无法读取时，输出一整段替换稿，不要“建议检查一下”。

## 交付

- 聊天里给结论表 + 最高优先级粘贴块（尺寸属性、ST、标题策略）。
- 完整报告写到 `outputs/{ASIN}-penalty-audit.md`（或用户指定目录）。
- 报告结构见 [references/report-template.md](references/report-template.md)。
- 四色/多变体必须按 **槽位实图** 写 ALT，不要假设所有颜色图顺序相同。
