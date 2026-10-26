# 完整体检报告结构与交付模板

把完整体检报告写入 `outputs/{ASIN}-penalty-audit.md`。聊天对话中输出结论摘要、评分卡、CTR/CVR 增长诊断、核心 Diff 对比、高优先级代码块及标准平铺表格。

---

## 报告标准 Markdown 模板

```markdown
# {ASIN} ({站点}) Listing 隐性减分体检与 CTR/CVR 算法增长诊断报告

## 1. 综合诊断与健康评分卡（0–100 Health Scorecard）

- **Listing 综合健康分**：`{SCORE} / 100`
- **风险等级**：`{RISK_LEVEL}` （极度危险 / 高危受限 / 中度风险 / 健康良好）
- **核心扣分项清单**：
  - 扣分项 1: [具体原因与扣分值]
  - 扣分项 2: [具体原因与扣分值]
- **数据清洗说明（若有）**：[说明爬虫/ERP管道符 `|` 的解耦情况，明确区分爬虫拼接符号与卖家真实输入]
- **整改预期收益**：修复后预估可回升至 `{PROJECTED_SCORE} / 100`，解除隐性降权风险，打通 Rufus/COSMO 事实引用，显著提升移动端 CTR 与 CVR。

---

## 2. 商品基本信息与移动端首屏模拟

- **产品原标题**：{Product Title}
- **品牌名称**：{Brand}
- **父体 / 变体结构**：Parent ASIN `{PARENT_ASIN}`，共 `{COUNT}` 个子变体（{Theme: Color / Size}）
- **适用品类 Overlay**：`{Category Overlay}`（说明选该品类的依据）
- **政策底线校验（Seller Central）**：{拉取成功 / 快照生效}；是否存在保修违规、EPA 杀菌词、FDA 违规医疗词、注册商标侵权词或未认证环保词。

---

## 3. 点击率（CTR）与转化率（CVR）双轮驱动诊断

### 3.1 点击率（CTR）驱动诊断：移动端 65 字符首屏呈现模拟
在手机端与移动 App 搜索结果卡片中，受屏幕宽度与 CSS 折叠限制，买家通常只能看到标题前 60–70 字符：
- **现网前 65 字符呈现**：`{Clean_Title[:65]}...`
- **CTR 缺陷诊断**：[诊断品牌是否露出？核心品类词是否前置？差异化参数（容量/功率/片数）是否在折叠前被买家看清？]
- **CTR 优化重组**：`{Optimized_Title[:65]}...`（实现：品牌一目了然 + 品类精准认知 + 核心卖点瞬间捕获买家视线）
- **主图视觉诊断**：纯白底（RGB 255, 255, 255）、产品占画面 ≥ 85%、无违规徽章/促销文字，保障主图高对比度与聚光度。

### 3.2 转化率（CVR）驱动诊断：详情页首屏决策与 Rufus 截流
- **3秒移动端速读转化（Item Highlights）**：针对移动端黄金眼动区，提供 ≤125 字符的逗号短语，快速传递核心不可替代参数，遏制买家跳失。
- **五点结构化决策（2024年8月15日新规合规）**：采用 `[特性标签]: [利益点]` 句式，句末无句号，无违禁符号，按“人群定位 → 核心性能 → 便捷操作 → 丰富场景 → 明确配件与保养”层层击穿买家顾虑。
- **阻断退货与差评（消灭 INAD）**：统一全页面尺寸、容量、功率与实测数据，清晰标注 `included_components`，消灭“货不对板”争议。

---

## 4. 1–10 项体检诊断汇总表

| # | 体检项 | 状态 | 严重度 | 关键证据与冲突点 | 修复优先级 |
|---|---|---|---|---|---|
| 1 | Size / Weight / Dimensions 多处不一致 | 通过 / 不通过 | 高 | 属性 5x10x5 vs 主图 4.7x4.7x6.77 | P1 |
| 2 | Variation theme 与变体文案一致性 | 通过 / 不通过 | 高 | 主题正确但子体文案分裂 | P2 |
| 3 | Browse node 多选或错选 | 通过 / 不通过 / DATA_MISSING | 中高 | 挂在次级非核心节点 | P1 |
| 4 | 图片 ALT 空白、错语言、空泛或超限 | 通过 / 不通过 | 低 | A+ 图 ALT 全空白或超 100 字符 | P2 |
| 5 | Search Terms 埋竞品品牌/ASIN/超限 | 通过 / 不通过 / DATA_MISSING | 高 | ST 含 ASIN 或超过 250 字节 | P1 |
| 6 | 描述/图片数字与实物不符 | 通过 / 不通过 | 中高 | 五点 12 cups vs 倒粉图 3 cups | P2 |
| 7 | 30 天 list price 改价超过 5 次 | 通过 / 不通过 / DATA_MISSING | 中高 | 秒杀 V 型不计，真实改价 0 次 | - |
| 8 | 跨变体图片串色 / 规格图错配 | 通过 / 不通过 | 高 | White 子体第 2 张挂了 Black 实图 | P1 |
| 9 | 夸大词 / 政策违规词 / 2024新规符号 | 通过 / 不通过 | 高 | 标题含 2-Year Warranty、五点含 ™ 符号 | P1 |
| 10| A+ 对比表 / FAQ 与当前子体不一致 | 通过 / 不通过 | 中高 | 对比表勾选可拆碗与实物打架 | P2 |

---

## 5. 核心 Diff 前后对比（高光纠偏）

| 字段 | 诊断前（现网风险点） | 诊断后（纠偏与 CTR/CVR 优化） | 算法与商业增益 |
|---|---|---|---|
| **标题** | SHARDOR Super Silent Coffee Grinder, 2-Year Warranty, Black... | SHARDOR Electric Coffee Grinder, 70g Capacity, Fast Stainless Steel Blade, Compact for Bean Spice, Black | 前置品牌与核心容量提升 CTR，清除保修词，安全索引区吃满长尾流量 |
| **Item Highlights** | [空白未填写] | 70g capacity, Stainless steel blade, One-touch grind, Compact design | 填满移动端首屏黄金位（≤125 字符），提升移动端 CVR |
| **五点 1** | 【SUPER SILENT】Quieter than others... | Compact Grinder for Home: Tailored for coffee enthusiasts seeking quick fresh grounds every morning; quiet motor reduces daily disturbance | 清除 Emoji 与夸大词，符合 2024 新规末尾无句号，映射受众人群 |
| **五点 5** | 2-Year Warranty Guaranteed with free replacement. | Complete Kit & Care: Includes 1 electric coffee grinder, 1 cleaning brush, and 1 user manual; hand wipe stainless bowl only, do not immerse motor in water | 清除违禁保修词，列清配件与保养边界，阻断退货差评 |
| **属性** | item_dimensions: 5x10x5, material: Metal | item_dimensions: 4.7"L x 4.7"W x 6.77"H, material: 304 Stainless Steel | 纠正错误尺寸，统一类目筛选器与 Rufus 事实源 |
| **ST** | burr mill B0FG6TJJGN best grinder | electric spice herb seed chopping blade compact kitchen seasoning | 剔除竞品 ASIN 与机制错词，充实长尾同义词 (<250 字节) |

---

## 6. Rufus 事实就绪度评分与模拟问答压力测试

### 6.1 Rufus 事实就绪度评分卡（Rufus Fact Readiness: {FACT_SCORE} / 100）

| 事实评价维度 | 满分 | 诊断前得分 | 优化后得分 | 关键赋能动作与事实闭环证据 |
|---|---|---|---|---|
| **显式规格事实覆盖度** | 25 分 | 10 分 | 25 分 | 统一物理容量（70g）、功率（200W）、材质（304不锈钢），填满后台属性 |
| **负向边界与退货防御度** | 25 分 | 5 分 | 25 分 | 明确干磨限制、机身不可水洗边界，阻断误用差评与退货 |
| **场景与兼容性映射度** | 25 分 | 10 分 | 25 分 | 明确 `intended_use`（咖啡豆/干香料）、`target_audience`（家庭咖啡爱好者） |
| **问答截流与差异化优势** | 25 分 | 5 分 | 23 分 | 提供 63dB 低噪实测、食品级材质认证，支持 AI 主动向买家背书推荐 |
| **合计就绪度总分** | 100 分 | **30 分（信息盲区）** | **98 分（AI优先推荐）** | 打通 Rufus 事实链条，形成闭环回答能力 |

### 6.2 Rufus 模拟问答压力测试（5 组 QA 审计）

| 模拟买家提问 | 修改前 PDP 表现 | 修改后 PDP 表现 | Rufus 引用依据 |
|---|---|---|---|
| **Q1: Who is this designed for?** | 未提及，可能被竞品截流 | 明确面向家庭日常咖啡爱好者 | 五点 Bullet 1 |
| **Q2: What is the exact capacity?** | 12 cups 与 70g 矛盾，回答模糊 | 明确 70g 咖啡豆，约 3 杯手冲量 | 属性 capacity + 五点 Bullet 2 |
| **Q3: What comes in the box?** | 倒粉图标注 GIVE AWAY 误导 | 明确标配机器、清洁刷、说明书 | 属性 included_components |
| **Q4: Can this grind wet food?** | 未说明使用边界，易坏产生退货 | 明确仅限干性咖啡豆/坚果研磨 | 五点 Bullet 5 边界申明 |
| **Q5: Is it dishwasher safe?** | FAQ 承诺机洗，五点未提 | 明确机身不可机洗，仅可毛刷干擦 | 五点 Bullet 5 & A+ FAQ |

---

## 7. 按 ASIN 落地工单与纯净代码块

*(每个改法均满足：思考在代码块外，块前标题只用字段名，代码块内只有纯英文原文)*

### 思考（标题策略）
前 65 字符严密锁定【品牌 + 核心词 + 核心规格】，解决移动端搜索截断痛点，拉升 CTR；后续扩展至 140 字符安全区间，补充高意向材质与场景同义词，确保 A9/COSMO 自然搜索流量召回。

### 标题（Blue）
```
SHARDOR Electric Coffee Grinder, 70g Capacity, Stainless Steel Blade for Beans and Spices, Compact Design, Blue
```

### 思考（Item Highlights）
控制在 125 字符以内，以短语平铺核心硬指标，作为移动端第一眼转化钩子。

### Item highlights（全变体共用）
```
70g bean capacity, Fast stainless steel blade, One-touch push button, Compact kitchen footprint
```

### 思考（五点描述）
严格遵循 2024 年 8 月 15 日官方新规：单条均控制在 240 字符以内，末尾无句号，无 ™/®/Emoji 等违禁符号，清晰解答受众、规格、操作、场景与装箱保养。

### 五点（全变体共用）
```
Target Audience: Tailored for coffee lovers and home baristas who want quick, consistent grinds for drip coffee, French press, and espresso
Precise 70g Capacity: Grinds up to 70 grams of fresh coffee beans yielding 3 to 4 flavorful cups in seconds; durable 304 stainless steel chamber ensures even texture
One-Touch Operation: Push-down lid activates stainless steel dual blades instantly; transparent cover allows effortless control over coarse or fine powder
Multi-Purpose Kitchen Tool: Easily pulverizes dry spices, herbs, nuts, and seeds; compact body fits neatly in small apartment cabinets or countertop corners
Package & Maintenance: Includes 1 electric grinder, 1 dual-head cleaning brush, and 1 user manual; dry wipe only and never rinse the motor base under tap
```

### 思考（通用属性纠偏）
依据官方属性一致性要求，修正错误长宽高并补全 Included Components，确保 COSMO 能够读取真实配件关系。

### 属性（全变体共用）
```
item_dimensions: 4.7"L x 4.7"W x 6.77"H
material: ABS Plastic, 304 Stainless Steel
style: Compact
included_components: Coffee Grinder, Cleaning Brush, User Manual
intended_use: Coffee Beans, Spices, Dry Herbs
```

### 思考（Search Terms）
清除前台已有的品牌与 ASIN，补充前台未收录的磨碎与食材同义词，严格控制在 250 字节以内。

### Search Terms
```
electric spice herb seed chopping blade compact kitchen seasoning
```

### 图库 ALT（Blue）
```
MAIN: SHARDOR blue electric coffee grinder front view with stainless steel blade on white background
IMG2: SHARDOR blue coffee grinder showing one touch button operation with ground coffee in bowl
```

### 思考（A+ Content 规划及 A+ ALT）
遵循亚马逊卖家中心 A+ Content Manager 官方硬性规范：每张图片的 ALT（Image Keywords）严格不得超过 100 字符。

### A+ ALT（父体共用，Seller Central 官方限制每张 ≤ 100 字符）
```
A+1: SHARDOR coffee grinder compact size diagram showing 6.77 inch height on marble countertop
A+2: SHARDOR coffee grinder 70 gram bowl with roasted coffee beans and measuring spoon
```

---

## 8. 亚马逊标准平铺表格（Flat Table / TSV 批量导入格式）

针对多变体批量修改，可直接整段复制以下 TSV 内容，粘贴导入官方批量上传模板（Inventory Loader / Category Flat File）。

> [!IMPORTANT]
> `update_delete` 必须显式填入 `PartialUpdate`！严禁留空或填 `Update`，否则未提供的空白属性将被亚马逊系统全量清空覆盖！

```tsv
feed_product_type	item_sku	update_delete	external_product_id	external_product_id_type	item_name	brand_name	parent_child	parent_sku	relationship_type	variation_theme	color_name	item_highlights1	bullet_point1	bullet_point2	bullet_point3	bullet_point4	bullet_point5	generic_keywords	item_dimensions	material	included_components
kitchen	PARENT-SKU-01	PartialUpdate			SHARDOR Electric Coffee Grinder 70g Capacity	SHARDOR	Parent			ColorName		70g capacity, One-touch grind	Target Audience: Tailored for coffee lovers and home baristas who want quick fresh grounds	Precise 70g Capacity: Grinds up to 70 grams of fresh coffee beans yielding 3 to 4 cups	One-Touch Operation: Push-down lid activates stainless steel dual blades instantly	Multi-Purpose Kitchen Tool: Easily pulverizes dry spices, herbs, nuts, and seeds	Package & Maintenance: Includes 1 electric grinder, 1 cleaning brush, and 1 user manual	electric spice herb seed chopping blade	4.7"L x 4.7"W x 6.77"H	304 Stainless Steel	Coffee Grinder, Cleaning Brush, User Manual
kitchen	SKU-BLUE-01	PartialUpdate	B0XXXXXXXX	ASIN	SHARDOR Electric Coffee Grinder, 70g Capacity, Stainless Steel Blade, Blue	SHARDOR	Child	PARENT-SKU-01	Variation	ColorName	Blue	70g capacity, One-touch grind	Target Audience: Tailored for coffee lovers and home baristas who want quick fresh grounds	Precise 70g Capacity: Grinds up to 70 grams of fresh coffee beans yielding 3 to 4 cups	One-Touch Operation: Push-down lid activates stainless steel dual blades instantly	Multi-Purpose Kitchen Tool: Easily pulverizes dry spices, herbs, nuts, and seeds	Package & Maintenance: Includes 1 electric grinder, 1 cleaning brush, and 1 user manual	electric spice herb seed chopping blade	4.7"L x 4.7"W x 6.77"H	304 Stainless Steel	Coffee Grinder, Cleaning Brush, User Manual
kitchen	SKU-BLACK-01	PartialUpdate	B0YYYYYYYY	ASIN	SHARDOR Electric Coffee Grinder, 70g Capacity, Stainless Steel Blade, Black	SHARDOR	Child	PARENT-SKU-01	Variation	ColorName	Black	70g capacity, One-touch grind	Target Audience: Tailored for coffee lovers and home baristas who want quick fresh grounds	Precise 70g Capacity: Grinds up to 70 grams of fresh coffee beans yielding 3 to 4 cups	One-Touch Operation: Push-down lid activates stainless steel dual blades instantly	Multi-Purpose Kitchen Tool: Easily pulverizes dry spices, herbs, nuts, and seeds	Package & Maintenance: Includes 1 electric grinder, 1 cleaning brush, and 1 user manual	electric spice herb seed chopping blade	4.7"L x 4.7"W x 6.77"H	304 Stainless Steel	Coffee Grinder, Cleaning Brush, User Manual
```

---

## 9. 团队协同落地：基于角色的 3 天执行看板（Role-Based Execution Kanban）

| 时间进度 | 运营岗（Operations） | 文案/SEO岗（Copywriting） | 视觉美工岗（Visual Design） |
|---|---|---|---|
| **Day 1: 安全底座与防退货** | 导出后台库存模板；核对并填满 Attributes 规格字段；提交 `update_delete = PartialUpdate` 刷新，消除前后端数据冲突。 | 整理全子体统一规格口径；提取各子体独立 `color_name` / `size_name`；剔除 Search Terms 中的 ASIN 与竞品词。 | 排查主图是否满足纯白底（RGB 255, 255, 255）与产品占比 ≥ 85%；下架所有含 warranty、guarantee 的宣传徽章图。 |
| **Day 2: CTR/CVR 增长上线** | 登录卖家中心 A+ 管理器与商品编辑页面；分批更新标题、Item highlights、五点描述；更新后台通用关键词（ST < 250 字节）。 | 按照移动端前 65 字符黄金区公式校准全子体标题；核对五点 2024 新规（无句号/无禁用符号）；提交每张 ≤ 100 字符的 A+ ALT。 | 解决跨变体图片串色与错配，核验每个子体图库第 1-7 张实图与色卡一一对应；完成信息图上的文字 OCR 纠偏（消灭拼写与数字错误）。 |
| **Day 3: 监控与事实闭环** | 检查后台是否报错；验证前台搜索展现与移动端折叠呈现；在手机端测试 Rufus 问答，核验 5 组模拟问题是否能精准回答。 | 追踪各核心关键词的自然搜索排名与展示量（Impression）；对比改前改后 CTR 转化数据波动。 | 备份全套合规图库源文件；根据前台展现效果做进一步高对比度与移动端视网膜屏细节微调。 |
```
