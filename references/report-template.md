# 完整体检报告结构与交付模板

把完整体检报告写入 `outputs/{ASIN}-penalty-audit.md`。聊天对话中输出结论摘要、评分卡、核心 Diff 对比、高优先级代码块及标准平铺表格。

---

## 报告标准 Markdown 模板

```markdown
# {ASIN} ({站点}) Listing 隐性减分体检与 AI 检索诊断报告

## 1. 综合诊断与健康评分卡（0–100 Health Scorecard）

- **Listing 综合健康分**：`{SCORE} / 100`
- **风险等级**：`{RISK_LEVEL}` （极度危险 / 高危受限 / 中度风险 / 健康良好）
- **核心扣分项清单**：
  - 扣分项 1: [具体原因与扣分值]
  - 扣分项 2: [具体原因与扣分值]
- **整改预期收益**：修复后预估可回升至 `{PROJECTED_SCORE} / 100`，解除静默降权风险，打通 Rufus/COSMO 引用通道。

## 2. 商品基本信息与覆盖层
- **产品名称**：{Product Title}
- **父体 / 变体结构**：Parent ASIN `{PARENT_ASIN}`，共 `{COUNT}` 个子变体（{Theme: Color / Size}）
- **适用品类 Overlay**：`{Category Overlay}`（说明选该品类的依据）
- **政策底线校验（Seller Central）**：{拉取成功 / 快照生效}；是否存在保修违规、EPA 杀菌词或商标侵权。

---

## 3. 1–10 项体检诊断汇总表

| # | 体检项 | 状态 | 严重度 | 关键证据与冲突点 | 修复优先级 |
|---|---|---|---|---|---|
| 1 | Size / Weight / Dimensions 多处不一致 | 通过 / 不通过 | 高 | 属性 5x10x5 vs 主图 4.7x4.7x6.77 | P1 |
| 2 | Variation theme 与真实差异错配 | 通过 / 不通过 | 高 | 主题正确但子体文案分裂 | P2 |
| 3 | Browse node 多选或错选 | 通过 / 不通过 / DATA_MISSING | 中高 | 挂在次级非核心节点 | P1 |
| 4 | 图片 ALT 空白、错语言或空泛 | 通过 / 不通过 | 低 | A+ 图 ALT 全空白 | P2 |
| 5 | Search Terms 埋竞品品牌/ASIN/超限 | 通过 / 不通过 / DATA_MISSING | 高 | ST 含 ASIN B0... | P1 |
| 6 | 描述/图片数字与实物不符 | 通过 / 不通过 | 中高 | 五点 12 cups vs 倒粉图 3 cups | P2 |
| 7 | 30 天 list price 改价超过 5 次 | 通过 / 不通过 / DATA_MISSING | 中高 | 秒杀 V 型不计，真实改价 0 次 | - |
| 8 | 跨变体图片串色 / 规格图错配 | 通过 / 不通过 | 高 | White 子体第 2 张挂了 Black 实图 | P1 |
| 9 | 夸大词 / 政策违规词 / EPA / 商标 | 通过 / 不通过 | 高 | 标题含 2-Year Warranty、Velcro | P1 |
| 10| A+ 对比表 / FAQ 与当前子体不一致 | 通过 / 不通过 | 中高 | 对比表勾选可拆碗与实物打架 | P2 |

---

## 4. 核心 Diff 前后对比（高光纠偏）

| 字段 | 诊断前（现网风险点） | 诊断后（纠偏与 AI 事实化） | 解决的核心问题 |
|---|---|---|---|
| **标题** | SHARDOR Super Silent Coffee Grinder, 2-Year Warranty, Black... | SHARDOR Electric Coffee Grinder, 70g Capacity, Black | 清除违禁词，控制字符数，避免降权 |
| **五点 1** | 【SUPER SILENT】Quieter than others... | Compact Electric Grinder with One-Touch Operation for Coffee Beans | 转为主观夸大消除，注入事实与人群 |
| **属性** | item_dimensions: 5x10x5, material: Metal | item_dimensions: 4.7x4.7x6.77 in, material: ABS, Stainless Steel | 纠正错误尺寸，统一筛选器口径 |
| **ST** | burr mill B0FG6TJJGN best grinder | electric spice herb seed chopping blade | 剔除竞品 ASIN 与机制错词，补同义词 |

---

## 5. Rufus 模拟问答压力测试（5 组 QA 审计）

| 模拟买家提问 | 修改前 PDP 表现 | 修改后 PDP 表现 | Rufus 引用依据 |
|---|---|---|---|
| **Q1: Who is this designed for?** | 未提及，可能被竞品截流 | 明确面向家庭日常咖啡爱好者 | 五点 Bullet 1 |
| **Q2: What is the exact capacity?** | 12 cups 与 70g 矛盾，回答模糊 | 明确 70g 咖啡豆，约 3 杯手冲量 | 属性 capacity + 五点 Bullet 2 |
| **Q3: What comes in the box?** | 倒粉图标注 GIVE AWAY 误导 | 明确标配机器、清洁刷、说明书 | 属性 included_components |
| **Q4: Can this grind wet food?** | 未说明使用边界，易坏产生退货 | 明确仅限干性咖啡豆/坚果研磨 | 五点 Bullet 5 边界申明 |
| **Q5: Is it dishwasher safe?** | FAQ 承诺机洗，五点未提 | 明确机身不可机洗，仅可毛刷干擦 | 五点 Bullet 5 & A+ FAQ |

---

## 6. 按 ASIN 落地工单与纯净代码块

*(每个改法均满足：思考在代码块外，块前标题只用字段名，代码块内只有纯英文原文)*

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

### 标题（Blue）
```
SHARDOR Electric Coffee Grinder, 70g Capacity, Blue
```

### 图库 ALT（Blue）
```
MAIN: SHARDOR blue electric coffee grinder front view with stainless steel blade on white background
IMG2: SHARDOR blue coffee grinder showing one touch button operation with ground coffee in bowl
```

### A+ ALT（父体共用）
```
A+1: SHARDOR coffee grinder compact size diagram showing 6.77 inch height on marble countertop
A+2: SHARDOR coffee grinder 70 gram bowl with roasted coffee beans and measuring spoon
```

---

## 7. 亚马逊标准平铺表格（Flat Table / TSV 批量导入格式）

针对多变体批量修改，可直接整段复制以下 TSV 内容，粘贴导入官方批量上传模板（Inventory Loader / Category Flat File）：

```tsv
feed_product_type	item_sku	external_product_id	external_product_id_type	item_name	item_highlights1	bullet_point1	bullet_point2	bullet_point3	bullet_point4	bullet_point5	generic_keywords	item_dimensions
kitchen	SKU-BLUE-01	B0XXXXXXXX	ASIN	SHARDOR Electric Coffee Grinder, 70g, Blue	Compact size, One-touch grind	Compact Electric Grinder with One-Touch Operation for Coffee Beans	70g Capacity Grinds Enough Beans for 3 to 4 Fresh Cups	Stainless Steel Dual Blade Quickly Grinds Coarse to Fine	Compact Lightweight Design Fits Easily in Small Kitchen Cabinets	Includes Grinder and Brush, For Dry Beans Only Hand Wipe Clean	electric spice herb seed chopping blade	4.7"L x 4.7"W x 6.77"H
kitchen	SKU-BLACK-01	B0YYYYYYYY	ASIN	SHARDOR Electric Coffee Grinder, 70g, Black	Compact size, One-touch grind	Compact Electric Grinder with One-Touch Operation for Coffee Beans	70g Capacity Grinds Enough Beans for 3 to 4 Fresh Cups	Stainless Steel Dual Blade Quickly Grinds Coarse to Fine	Compact Lightweight Design Fits Easily in Small Kitchen Cabinets	Includes Grinder and Brush, For Dry Beans Only Hand Wipe Clean	electric spice herb seed chopping blade	4.7"L x 4.7"W x 6.77"H
```

---

## 8. 执行工单与分步实施路线
- **Day 1（安全底座）**：更新后台 Attributes 属性栏与 A+ 规格数字（对权重无震荡，阻断 INAD 退货）；
- **Day 2（文本纠偏）**：批量更新 ST、五点、非英雄子体标题、Item highlights、图库 ALT、A+ ALT；
- **Day 3（视觉物料）**：美工安排替换图库中串色的子体图、下掉主图/附图上的违规保修徽章。
```
