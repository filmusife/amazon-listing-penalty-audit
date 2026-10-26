---
name: listing-audit
description: 以亚马逊最新 Seller Central 规则为底线，对任意品类 Listing（默认美国站）做 7 个隐性减分项加 3 个扩展项体检，深度结合 A9/COSMO 意图图谱与 Rufus 购物助手算法机制，输出以提升点击率（CTR）与转化率（CVR）为核心的落地诊断报告与全套合规文案。支持 0-100 风险量化评分、爬虫管道符智能清洗防误判、HTML 页面原生解析提取、移动端 65 字符首屏呈现模拟、2024年8月15日五点新规（无句号/无违禁符号）排查、EPA/FIFRA 农药杀菌排查、FDA 医疗疾病声称排查、FTC 纺织品排查、商标防爆雷、Rufus 事实就绪度评分与 5 组拟真问答压力测试、全变体 PartialUpdate 安全平铺表格（Flat Table TSV）。输出标题、Item highlights、五点、属性、图库 ALT、A+ ALT（严格遵循官方 ≤100 字符硬性限制）、Search Terms。在用户要检查静默降权、尺寸/属性不一致、变体错配、Browse Node、图片 ALT、Search Terms 竞品品牌、warranty/guarantee、描述与实物不符、30 天频繁调价、秒杀与改价、跨变体图片串色、夸大词、A+ 与子体不一致，或输入 /listing-audit、/amazon-listing-penalty-audit、/penalty-audit、/隐性减分 时使用。不要用于从零写新 Listing、选品调研或纯评论分析。
metadata:
  short-description: 全品类官方最新规则+10项隐性体检+CTR/CVR双轮驱动+0-100评分+PartialUpdate平铺表格+Rufus事实就绪度
---

# Amazon Listing 隐性减分体检与 CTR/CVR 增长审计

对指定站点 ASIN（默认 US）做 **政策底线体检与算法商业增长诊断**。规则按 **站点 + 品类** 套用，不套用历史个案。

不是从零写 Listing，也不是泛选品调研。

## 双目标（必须同时满足）

1. **政策底线（Floor）：** 严格对齐 Seller Central 最新规则。彻底清除 warranty/guarantee 承诺、主观绝对化夸大词、超 200 字符抑制、图上违禁徽章、EPA/FIFRA 未申报杀菌词、FDA 违规医疗疾病声称、FTC 竹纤维违规宣称、第三方注册商标侵权词（Velcro, Thermos 等）、未认证绿色环保词（eco-friendly）及 2024 年 8 月 15 日五点新规禁用的特殊符号（`™ ® © … ✓ ❌` 等）。不得为“保当前排名”保留违规词。
2. **算法流量与商业增长（CTR & CVR Engine）：** 合规纠偏后，全面围绕亚马逊现行算法（A9/A10 检索召回、COSMO 意图常识图谱、Rufus 生成式购物助手）优化点击率与转化率：
   - **点击率（CTR）引擎**：标题采用**前 60–80 字符黄金区**，前置【品牌 + 核心品类词 + 核心规格】，确保移动端与 App 搜索卡片折叠前一目了然，捕获买家首屏点击；主图严格白底且产品占比 ≥ 85%。
   - **自然搜索召回（Lexical Retrieval）**：标题 80–180 字符高权重安全索引区容纳核心同义词与长尾词；ST 严格 < 250 字节补足前台未覆盖的同义词与长尾意图。
   - **转化率（CVR）与防退货引擎**：Item highlights（≤125 字符）锁定移动端 3 秒速读；五点描述按“人群定位 → 核心性能 → 便捷操作 → 丰富场景 → 明确配件与保养”结构化推进，句末无句号；统一物理度量衡，明确 `included_components`，彻底消灭“货不对板”（INAD）差评与退货。
   - **Rufus / Alexa for Shopping 截流**：填满属性与 A+ 知识库，使 AI 购物助手在买家提问时给出正面、明确的回答并主动推荐本品。

## 何时用 / 何时不用

**用：** 用户给了 ASIN，要查为什么排名上不去、要按减分项逐条修、要可进后台的改法、要解决移动端搜索截断与点击率下滑、要覆盖全部颜色/尺寸变体，或需要一键导入官方库存模板的标准平铺表格（Flat Table TSV）。

**不用：** 从零写全新 Listing（转 `amazon-listing-agent`）；选品/关键词挖掘（转对应调研 skill）；只分析评论痛点（转评论分析 skill）。

## 必做流程

1. **定站点和品类。** 默认 US。非美国站先拉该站点帮助页；拉不到则用 US 快照，并标 `MARKETPLACE_UNVERIFIED`。品类只读 [references/category-overlays.md](references/category-overlays.md) 匹配节（含新增汽配与宠物类目）。
2. **拉官方现行规则。** 打开 [references/amazon-policy.md](references/amazon-policy.md) 列出的 Seller Central 页面，现行规则覆盖快照。拉失败标 `POLICY_FETCH_FAILED`。
3. **收齐证据并严格清洗数据。** 最低用前台包 `frontend-min`；有后台/Keepa 再用 `backend-full`。
   - **HTML 原生解析提效**：若有抓取到的原生网页，直接执行 `python scripts/scan_listing.py --html pdp.html --format summary`，自动提取 `#productTitle`、`#bylineInfo`、`#feature-bullets`、`#productOverview_feature_div`、图库与 A+ ALT，无需手动拼凑 JSON。
   - **数据解耦铁律**：提取标题时若存在管道符 ` | `，优先判断是否为爬虫/ERP（如领星）拼接了【标题 + Item highlights】或【标题 + 类目/品牌】。**必须先完成数据清洗解耦，严禁将数据抓取的管道符诬陷为卖家违规，更严禁臆造“亚马逊系统因管道符将标题腰斩”！**
4. **能数的不要眼看。** 提取字段后，用 [scripts/scan_listing.py](scripts/scan_listing.py) 执行确定性扫描，数字符、ST 字节、违禁词、ALT 语言、ASIN 污染、EPA 词、FDA 医疗词、FTC 纺织词、商标侵权词与 3D 尺寸冲突。
5. **打分与 CTR/CVR 诊断。** 输出 **0–100 综合健康分**。并在报告中呈现 **移动端 65 字符首屏呈现模拟** 与 CTR/CVR 诊断分析。
6. **每个子 ASIN 都要改**，变体文案保持统一模板，仅替换变体词。
7. **数字以可测量证据为准：** 属性栏、A+、主图标注、五点必须同一套数。
8. **每条建议先写思考，再给代码块。** 思考写依据哪条官方规则、为什么这样改、服务哪一层（政策 / CTR 黄金区 / COSMO 关系 / Rufus 事实 / A9 索引）。代码块里只有 Seller Central 纯英文原文。写法读 [references/copy-rules.md](references/copy-rules.md) 和 [references/rufus-cosmo.md](references/rufus-cosmo.md)。
9. **双轨交付与 Rufus 问答压力测试：** 既给单字段独立英文粘贴块，又在报告末尾提供整套全子体 **亚马逊标准平铺表格（Flat Table / TSV 格式）**。执行 **Rufus 事实就绪度量化评分与 5 组模拟问答压力测试**，验证事实回答闭环。

出报告时严格遵照 [references/report-template.md](references/report-template.md)。

## 体检项（1–7 核心，8–10 扩展）

| # | 项 | 影响 | 前端能否判死 |
|---|---|---|---|
| 1 | Size / Weight / Dimensions 多处不一致 | 高 | 能 |
| 2 | Variation theme 与变体文案一致性 | 高 | 主题能；文案对齐能 |
| 3 | Browse node 多选或错选 | 中高 | 前台主节点能；后台完整节点 `DATA_MISSING` |
| 4 | 图片 ALT 空白、错语言、空泛或超限（A+ ALT >100字符） | 低 | 大概率能（图库 + A+ 实图） |
| 5 | Search Terms 埋竞品品牌/ASIN/超250字节 | 高 | 前台文案能；ST 本身 `DATA_MISSING`，给整段替换 |
| 6 | 描述/图片数字与实物不符（含图片拼写错误） | 中高 | 内部矛盾能；实物未量则标待复核 |
| 7 | 30 天 list price 改价超过 5 次 | 中高 | Keepa 能近似；须先排除秒杀/券 |
| 8 | 跨变体图片串色 / 规格图错配（缺尺寸图） | 高 | 能（对照各子体实图） |
| 9 | 夸大词 / 政策违规词 / 2024新规符号排查 | 高 | 能 |
| 10 | A+ 对比表 / FAQ / 视频与当前子体不一致 | 中高 | 能 |

优先修 **高影响 + 低难度**：#1、#3、#5、#9。不要同一天大改英雄子体标题 + 主图 + 五点。

## 铁律

- **抓取清洗与理性定性**：爬虫或系统数据中的管道符 ` | ` 绝大多数为字段拼接物，体检必须自动解耦清洗，**严禁将管道符判定为卖家滥用，严禁谎称系统截断**。
- **标题双层架构**：
  - 前 60–80 字符黄金区（CTR 命脉）：必须完整露出【品牌 + 核心词 + 核心规格】，确保移动端卡片折叠前抓住买家；
  - 80–180 字符长尾索引区：容纳材质、场景、长尾同义词，确保 A9/COSMO 自然搜索流量；
  - 官方硬性上限为 200 字符（超限触发搜索抑制）。**严禁机械式把标题强行砍成 ≤75 字符而丢弃长尾词！**
- **五点描述（2024年8月15日新规）**：推荐 3–5 条，单条建议 150–240 字符，总长建议 ≤ 1,000 字符；**短语末尾严禁加句号**；严禁整条 ALL CAPS；**严禁任何特殊符号/Emoji**（`™ ® © … † ‡ ± ~ € £ ¥ ✓ ❌ ★ 【】` 等）；严禁保修与未认证绿色词。
- **Item highlights**：官方硬性限制 ≤ 125 字符，逗号短语，作为移动端详情页 3 秒首屏转化核心。
- **A+ 图片 ALT 官方硬性上限**：每个 A+ 图 ALT **严格不得超过 100 字符（≤ 100 characters，含空格）**，超出后台直接报错拦截无法保存。推荐 50–95 字符。
- **Search Terms**：美国站严格小于 250 字节（< 250 bytes，以 UTF-8 字节计算），空格分隔，全小写，不重复前台词，无品牌，无 ASIN。
- **保修政策**：禁止把 warranty / guarantee / money-back 写入标题、五点、图、A+、ALT、ST。保修只进 Warranty 专用属性。
- **合规排查**：严禁非 EPA 备案产品在文案中出现 `anti-microbial`、`antibacterial`、`mold-resistant` 等杀菌词；严禁 FDA 违规医疗疾病治愈宣称（`cure`, `treats arthritis`）；严禁 FTC 纺织品未标明 `rayon/viscose from bamboo`；严禁将 `Velcro`、`Thermos` 等注册商标误用为通用词；严禁未认证环保词（`eco-friendly`）。
- **Flat Table 安全更新铁律**：批量上传平铺表格中 `update_delete` 列 **必须 100% 显式填写 `PartialUpdate`**，严禁留空或填 `Update`，防后台未提供字段被全量抹除清空！
- **英雄子体原则**：英雄子体若标题已合规且小类排名稳定，不要为了“更美观”改标题（思考区写“不动”）；若含违规词（warranty、商标侵权、超 200 字符抑制），必须改。
- **双轨交付**：必须同时提供单字段独立纯英文代码块（零中文）和批量导入的标准平铺表格（Flat Table TSV）。
- **Rufus 事实就绪度量化与 5 组模拟问答测试**：报告必须评估 0-100 事实就绪度，并检验买家核心问题（人群、规格、配件、场景、维护边界）的事实闭环。

## 发出前自检

- 是否对爬虫数据进行了清洗，杜绝将管道符误判为卖家违规？
- 标题前 65 字符是否完整呈现了品牌与核心品类，以保障移动端 CTR？
- 标题总长是否在 120–180 字符安全索引区内（未超 200 字符抑制红线）？
- 每张 A+ 图片的 ALT 是否严格控制在 ≤ 100 字符以内？
- 五点描述是否符合 2024 新规（无句号、无 ™/®/Emoji 等违禁符号）？
- Search Terms 字节数是否用 UTF-8 计算严格 < 250 字节？
- Flat Table TSV 表格中 `update_delete` 是否填写为 `PartialUpdate`？
- 思考区是否从 CTR / CVR / 政策 / COSMO / Rufus 层面给出依据，而非空洞说教？
- 是否提供了全子体标准平铺表格（Flat Table TSV）与 Rufus 5 组问答测试？
