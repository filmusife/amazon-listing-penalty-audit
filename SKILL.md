---
name: amazon-listing-penalty-audit
description: 以亚马逊最新 Seller Central 规则为底线，对任意品类 Listing（默认美国站）做 7 个隐性减分项加 3 个扩展项体检，纠偏后再按 COSMO 关系与 Rufus/Alexa for Shopping 可引用事实优化发现权重，而不是堆 A9 关键词。输出标题、Item highlights、五点、属性、图库 ALT、A+ ALT、Search Terms。在用户要检查静默降权、尺寸/属性不一致、变体错配、Browse Node、图片 ALT、Search Terms 竞品品牌、warranty/guarantee、描述与实物不符、30 天频繁调价、秒杀与改价、跨变体图片串色、夸大词、A+ 与子体不一致，或输入 /listing-audit、/penalty-audit、/隐性减分 时使用。不要用于从零写新 Listing、选品调研或纯评论分析。
metadata:
  short-description: 全品类官方规则底线+隐性减分；合规后按 Rufus/COSMO 优化，块外写思考、块内纯粘贴
---

# Amazon Listing 隐性减分体检

对指定站点 ASIN（默认 US）做 **静默降权体检**。规则按 **站点 + 品类** 套用，不按某个历史 ASIN 或某个厨房电器案例套用。

不是写新 Listing，也不是竞品调研。

## 双目标（必须同时满足）

1. **政策底线：** 先对齐该站点最新 Seller Central 规则。warranty / guarantee、促销语、夸大词、超长标题、图上徽章这类违规，必须先改掉。不能为了“保住当前排名”把违规词留在 PDP 上。
2. **发现权重：** 合规且字段一致之后，再优化自然发现。不要把旧 A9 堆词当北星。按三层写：
   - **Lexical retrieval（A9/A10）：** 标题/五点/ST 各出现一次核心同义词，进入候选集。禁止同一词连写或管道符堆砌。
   - **COSMO：** 用 who / where / when / 解决问题 / 场合 / 配件关系填 discovery 属性（intended_use、target_audience、occasion、item type），不要只把这些词塞进标题。
   - **Rufus / Alexa for Shopping：** 写可引用事实。数字和分类问题优先走属性；每条五点回答一个买家问题；A+ 正文、对比表、图上 overlay、ALT 都是检索源。空属性 = 助手无法回答。

Amazon 没有公布 Rufus 完整排名公式。第三方「必须覆盖 8/15 条 COSMO 关系」「去种 Q&A」只当启发式，有证据才映射，不要编场景。字段自相矛盾通常不会弹窗报警，但会少展示、提高 INAD，再反向压权重。纠偏是地板，发现层优化才是目的。

## 何时用 / 何时不用

**用：** 用户给了 ASIN，要查为什么排名上不去、要按减分项逐条修、要可进后台的改法、要覆盖全部颜色/尺寸/其他变体。

**不用：** 从零写标题五点（转 `amazon-listing-agent`）；选品/关键词挖掘（转对应调研 skill）；只分析评论痛点（转评论分析 skill，不要在本流程里抓全站评论）。

## 必做流程

1. **定站点和品类。** 默认 US。非美国站先拉该站点帮助页；拉不到则用 US 快照，并标 `MARKETPLACE_UNVERIFIED`。品类只读 [references/category-overlays.md](references/category-overlays.md) 里匹配的那一节，禁止把其他品类的机制词、单位、宣称套过来。
2. **先拉官方规则。** 写任何标题 / 五点 / Item highlights / ALT / ST / A+ 之前，打开 [references/amazon-policy.md](references/amazon-policy.md) 列出的 Seller Central 页面。拉到的现行规则覆盖快照。拉失败则用快照，并标 `POLICY_FETCH_FAILED`。
3. **收齐证据再下结论。** 最低用前台包 `frontend-min`；有后台/Keepa 再用 `backend-full`。缺字段标 `DATA_MISSING`，不要编。取证细节读 [references/evidence-collection.md](references/evidence-collection.md)。
4. **能数的不要眼看。** 标题/五点/ALT/ST 提取后，用 [scripts/scan_listing.py](scripts/scan_listing.py) 数字符、ST 字节、违禁词、ALT 语言、ASIN 污染。脚本计数优先于目测。
5. **第 1–7 项全部打分，再打第 8–10 扩展项。** 标准见 [references/seven-items.md](references/seven-items.md) 和 [references/extra-items.md](references/extra-items.md)。warranty / guarantee / 促销徽章并进第 9 项。
6. **每个子 ASIN 都要改**，不要只改用户点名的那一个颜色/尺码。
7. **数字以可测量证据为准：** 属性栏、A+、主图标注、五点必须同一套数。
8. **每条建议先写思考，再给代码块。** 思考写依据哪条官方规则、为什么这样改、以及服务哪一层（政策 / COSMO 关系 / Rufus 可引用事实 / Lexical 同义词）。禁止写「堆 A9 词」。代码块里只有能进 Seller Central 的原文。块前标题只用字段名。文案写法读 [references/copy-rules.md](references/copy-rules.md)；写字段时再读 [references/rufus-cosmo.md](references/rufus-cosmo.md)。

按需读 reference，不要一次全读。写标题/五点/属性/A+/ST 时读 [references/rufus-cosmo.md](references/rufus-cosmo.md)。只有需要看「思考 + 纯粘贴块」写法，或本品恰好是同类厨房小家电冲突时，才读 [references/example-B0FG6TJJGN.md](references/example-B0FG6TJJGN.md)。案例里的碗数、dB、burr、四色磨豆机 **不是通用规则**。

## 体检项（1–7 核心，8–10 扩展）

| # | 项 | 影响 | 前端能否判死 |
|---|---|---|---|
| 1 | Size / Weight / Dimensions 多处不一致 | 高 | 能 |
| 2 | Variation theme 与真实差异错配 | 高 | 主题能；文案对齐能 |
| 3 | Browse node 多选或错选 | 中高 | 前台主节点能；后台完整节点 `DATA_MISSING` |
| 4 | 图片 ALT 空白、错语言或空泛 | 低 | 大概率能（图库 + A+ 实图） |
| 5 | Search Terms 埋竞品品牌或 ASIN | 高 | 前台文案能；ST 本身 `DATA_MISSING`，给整段替换 |
| 6 | 描述/图片数字与实物不符 | 中高 | 内部矛盾能；实物未量则标待复核 |
| 7 | 30 天 list price 改价超过 5 次 | 中高 | Keepa 能近似；须先排除秒杀/券 |
| 8 | 跨变体图片串色 / 规格图错配 | 高 | 能（对照各子体实图） |
| 9 | 夸大词 / 比较词 / 政策违禁词 | 高 | 能 |
| 10 | A+ 对比表 / FAQ / 视频与当前子体不一致 | 中高 | 能 |

优先修 **高影响 + 低难度**：#1、#3、#5、#9。不要同一天大改英雄子体标题 + 主图 + 五点。

## 铁律

- 禁止把 warranty / guarantee / money-back / 100% quality guaranteed 写入标题、五点、图、A+、ALT、ST。保修只进 Warranty 文档或专用属性。
- 禁止把竞品品牌、竞品 ASIN、best、#1、促销语写入 PDP 营销字段或 ST。
- 实验室噪音、铭牌功率、未称重的重量：没有铭牌/实测就留空，并在思考区写清要用户补。
- 新写或重写的 **美国站** 标题默认 ≤75 字符（含空格）；溢出卖点进 Item highlights（≤125，逗号短语，不是句子）。其他站点不要默认套 75 字，拉到当地规则再判。英雄子体“排名好就不动标题”**不能**覆盖政策违规标题。
- 变体主题正确但文案分裂，判定为第 2 项“主题通过、内容不通过”，不要拆组。
- 尺寸以卡尺为准；若无卡尺，优先用 **主图/尺码图上的标注**，而不是属性栏里看起来更整的数字。
- 容量、功率、分贝、尺寸、件数、成分百分比，只要出现在图上，就必须和五点/A+/属性一致。打架时取可测量或更保守的那套，并改掉其余位置。
- Search Terms：美国站 <250 字节，空格分隔，全小写，不重复前台词。后台无法读取时，输出一整段替换稿。同一父体通常共用一段 ST；变体词已在标题末尾就不要再堆进 ST。
- **粘贴块纯度：** 代码块里只放 Seller Central 原文。中文说明、为什么改、不要改、改图后，一律写在代码块外的思考区。
- **块前标题只用字段名**，例如 `标题（Navy, Size M）`、`五点（全变体共用）`、`图库 ALT（White）`。禁止写“可复制”“可粘贴”。
- **第 7 项只计卖家 list price 真实改价。** Keepa 上 V 型回落、List Price 不动而 Buy Box 下跌、带 Lightning / 7-day deal / coupon 标记的，一律当促销，不定不通过。分不清就 `DATA_MISSING`。已经在做秒杀/券时，不要改口令成“锁价、停活动”。
- **每个已分析的 A+ 图都要给一句符合站点语言的 ALT**，按模块从上到下、图从左到右编号。完整 ALT 清单必须出现在报告文件；聊天不得用“见文件”代替而漏写模块。
- 不要把一个品类的机制词套到另一个品类（刀片机写 burr、服装写 watt、个护写 cup capacity）。

## 交付

- 聊天里给结论表 + Rufus/COSMO 覆盖缺口（谁用、在哪用、箱内有什么、使用边界）+ 最高优先级代码块（通常是统一属性/尺寸、ST、标题策略；若第 4/8 项不通过，再给受影响的图库 ALT 和 **A+ ALT**）。需要缩短标题时同时给 Item highlights。
- 完整报告写到 `outputs/{ASIN}-penalty-audit.md`（或用户指定目录），结构见 [references/report-template.md](references/report-template.md)。
- 变体 ≥5 个时，聊天可只放英雄子体 + 1 个问题子体的粘贴块，其余子体必须写进报告，不能漏审。
- 多变体必须按 **槽位实图** 写图库 ALT；A+ 按页面模块顺序写 ALT。

## 发出前自检

- 有没有把其他品类的单位/机制词套到本品？
- 是否审了全部子 ASIN，而不是只改用户点名的那一个？
- 代码块里有没有中文、夹注、操作说明？
- 英雄标题：合规且排名稳 → 不出标题块；违规 → 必须改。
- 第 7 项是否把秒杀/券当成频繁改价？
- 已分析的 A+ 图是否都有 ALT？
- 思考区是否写了政策 / COSMO / Rufus 层，而不是「堆 A9 词」？
- 属性 intended_use / target_audience 等 discovery 字段是否给了可填值，而不是只改标题？
- 有没有把 15 条 COSMO 关系或 Q&A 种草写成铁律？
