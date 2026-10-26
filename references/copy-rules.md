# 文案规则与双轨交付规范

写改法时读。先过官方政策，再补发现层。不要为了堆 A9 词牺牲合规。写字段时同时读 [rufus-cosmo.md](rufus-cosmo.md)。品类机制词、单位、禁写功效只取 [category-overlays.md](category-overlays.md) 匹配节。

---

## 交付规范：双轨交付（Dual Delivery）

用户在修改亚马逊 Listing 时有两种常见场景：单个子体微调 vs 多变体大批量更新。因此体检必须提供 **双轨交付**：

1. **单字段独立英文粘贴块**：用于运营在 Seller Central 网页端快速单项修改；
2. **亚马逊标准平铺表格（Flat Table / TSV 格式）**：用于多变体商品，整行整列直接复制导入卖家下载的官方库存文件（Category Flat File / Inventory Loader），支持一键批量上传（Add Products via Upload）。

### 1. 单字段代码块规范
- 块前标题 **只用字段名**：`### 标题（Navy, Size M）`、`### Item highlights（Navy）`、`### 五点（全变体共用）`、`### 属性（全变体共用）`、`### 图库 ALT（White）`、`### A+ ALT（父体共用）`、`### Search Terms`。
- **严禁**在标题或代码块内写“可复制”“可粘贴”“paste-ready”。
- 代码块内 **只有纯英文原文**，零中文、零括号注释、零操作说明。
- 代码块正上方用 **思考** 说明：依据哪条 Seller Central 政策；为什么这样改；服务哪一层（政策 / COSMO 关系 / Rufus 可引用事实 / Lexical 同义词）。

### 2. 标准平铺表格规范（Flat Table / TSV）
在报告末尾或多变体修复中，生成标准 TSV（制表符分隔）代码块，至少包含以下列：
```tsv
feed_product_type	item_sku	external_product_id	external_product_id_type	item_name	item_highlights1	bullet_point1	bullet_point2	bullet_point3	bullet_point4	bullet_point5	generic_keywords	item_dimensions	capacity	item_weight	color_name	material_type
```
变体较多（≥3 个）时，平铺表格能极大减轻卖家手工复制的负担。

---

## 政策闸门与红线排查（写之前必过）

对照 [amazon-policy.md](amazon-policy.md)。出现任一项先改文案，再谈优化：

1. **保修信息**：warranty / guarantee / money-back / 100% quality guaranteed（必须彻底移除，只填入后台专用 Warranty 属性）。
2. **夸大比较**：best / #1 / 无外包装证据的绝对词 / 点名竞品（除 `for best results` 操作指导语外，一律删除）。
3. **农药杀菌（EPA）**：anti-microbial / antibacterial / mold-resistant / disinfectant（非 EPA 注册一律清除，改用物理特性描述）。
4. **注册商标（IP）**：把 Velcro 改为 `hook and loop`；Thermos 改为 `insulated tumbler`；PopSockets 改为 `collapsible phone grip`；Gore-Tex 改为 `waterproof breathable fabric` 等。
5. **违规符号**：标题禁用 `! $ ? _ { } ^ ¬ ¦`，五点禁用 【】★ emoji ™ ®，句末不加句号。
6. **未认证环保宣称**：禁止使用 `eco-friendly`、`environmentally friendly`，避免触发环境声明政策限制。

---

## 标题（Title，硬上限 200 字符，CTR 黄金区 + 长尾索引双层架构）

- **CTR 驱动的黄金结构（双层架构）**：
  - **第一层：移动端 60–80 字符黄金区（CTR 命脉）**：
    - **公式**：`[Brand] + [Core Product Keyword] + [Key Spec / Primary Metric] + [Top Differentiator]`
    - **CTR 逻辑**：移动端搜索卡片因为屏幕限制会在 ~65 字符处折叠。买家必须在折叠前看清“谁家做的、具体是什么、核心多大/多强”。若品牌或品类词后置，点击率（CTR）将断崖式下跌。
  - **第二层：高权重长尾索引区（80–180 字符）**：
    - **内容**：收录核心长尾同义词、主要材质、兼容机型、适用场景与末尾变体词（颜色/尺寸放最后）。
    - **算法逻辑**：A9 与 COSMO 语义引擎依然会完整建立这部分词条的搜索索引。控制在 120–180 字符既吃满搜索长尾曝光，又远离 200 字符搜索抑制红线。
  - **切忌**：严禁机械式地把所有 Listing 标题强行砍成 ≤75 字符！这会导致 Listing 丢掉后半段关键搜索词，重创自然流量。
- **关于数据抓取中的“管道符 `|`”**：
  - 若输入数据含有 ` | `，通常为爬虫/ERP/`<title>` 标签拼接了标题与卖点高亮，**必须自动清洗剥离，严禁将抓取分隔符误判为卖家违规或臆造“系统腰斩扣分”**。在后台新提交文本中，推荐使用英文半角逗号 `,` 或连字符 `-`。
- **格式规范**：Title Case（实词首字母大写，介词连词小写）；严禁全句 ALL CAPS；严禁全角符号（如中文逗号 `，`）与任何装饰符号。
- **溢出卖点分流（协同 Item Highlights）**：
  - 核心参数与卖点短语优先录入 **Item highlights**（≤125 字符，逗号分隔短语）；
  - *兜底策略*：若该商品类目后台无 Item highlights 属性，将溢出卖点有序编入五点描述前 2 条中。
- **英雄子体原则**：
  - 若英雄子体标题 **已经合规** 且有稳定小类排名，不要为了“更美观”去改它的标题。该 ASIN 不要输出标题代码块，只在思考区写“不动”和原因。
  - 英雄标题一旦违规（含 warranty、夸大词、超 200 字符抑制、商标侵权），必须强制重写，排名好也不能留。
- **其他子体**：套用统一标题模板，仅替换末尾变体词。

---

## Item Highlights（商品核心亮点，官方限制 ≤ 125 字符，移动端 CVR 引擎）

- **字符限制**：**严格 ≤ 125 字符（含空格）**。
- **格式**：短语形式，逗号分隔，不写完整长句，例如：`10oz Glass Pitcher, 5-in-1 Auto Presets, BPA-Free Tritan, One-Touch Self Clean`。
- **转化率（CVR）价值**：位于移动端 PDP 详情页首屏黄金眼动区，买家扫视 3 秒即可确认是否符合购买预期，极大降低跳失率。

---

## 五点（Bullet Points，推荐 5 条，严格对齐 2024 年 8 月 15 日新规）

- **字符限制**：推荐 3–5 条，单条建议控制在 **150–240 字符**（系统上限 255 字符），5 条总长建议不超过 **1,000 字符**（过长会在移动端折叠，降低买家阅读率）。
- **标点与格式**：
  - 采用 `[加粗/大写特性标签]: [利益点与事实阐述]`（如 `One-Touch Operation: Features 6 intuitive presets...`）；
  - **末尾严禁加句号**（对齐亚马逊风格指南 "Do not end with punctuation"）；
  - 禁止整条 ALL CAPS；
  - **严禁 2024 官方违禁符号**：`™ ® © … † ‡ ± ~ € £ ¥ ✓ ❌ ★ ● 【】` 以及各类 Emoji。
- **全部子体一致**：共用五点里严禁写死某个特定颜色/尺寸。
- **结构化映射（双轮驱动 CVR 提升与 Rufus 问答截流）**：
  - Bullet 1: *【定位与人群】*（明确产品定位，告诉买家“这是为你准备的”，提升意图契合度）
  - Bullet 2: *【核心规格与性能】*（容量、材质、功率等实测数据，消除尺寸/性能疑虑，防退货）
  - Bullet 3: *【便捷操作与核心痛点】*（操作简便度、自动程序、省时省力，强化购买冲动）
  - Bullet 4: *【使用场景与生活契合】*（厨房、差旅、办公等生动场景，映射 COSMO 关系）
  - Bullet 5: *【装箱清单与维护边界】*（明确列出 `included_components` 与保养清洗边界，杜绝买家误用差评与退货）
- 粘贴块只有 5 行纯英文正文，不要带有 `Bullet 1:` 这样的中文前缀。

---

## 属性（Attributes）

常见脏字段与修法（值要按实物）：

| 字段 | 严禁填入 | 正确填法 |
|---|---|---|
| `style` | NICE、随意形容词 | 与实物相符的真实 style（Modern, Classic, Compact） |
| `material` | 只写金属但壳体是塑料；混纺只写棉 | 真实主要材质（ABS Plastic, 304 Stainless Steel） |
| `size` | Large（与尺寸筛选冲突） | 真实容量或标准尺码名 |
| `included_components` | 件数不对、把固定部件写成配件 | 整机 + 真实可拆配件清单 |
| `capacity` | 把重量当容量（如 3.3 磅）或虚高杯数 | 真实液体体积或物理容量（40 fl oz, 8 Cups, 1.2L） |
| `item_weight` | 留空、抄容量 | 真实称重净重（如 3.3 pounds） |
| `item_dimensions` | 长宽高倒置（如高度填为 5.28"） | 真实长宽高物理测量（11.93"L x 5.28"W x 11.46"H） |
| `warranty_description` | 写入标题/五点 | 仅填入此专用字段 |

属性优先于 Search Terms。同一父体除变体维度外全部复制。

---

## 图库 ALT（Gallery Images，主副图图文描述）

- 匹配站点语言。美国站英文建议控制在 **80–150 字符**。
- 句式：`{品牌} {变体词} {看得见的产品} with {材质或关键零件} for {图中场景}`
- 必须按每个 ASIN 的实际槽位实图编写：`MAIN:`、`PT01:`、`PT02:`……
- 描述当前画面真实特征，不堆砌无意义关键词，不写 warranty、best 或竞品词。

---

## A+ 图片 ALT（Image Keywords，卖家后台官方硬性限制 ≤ 100 字符）

在亚马逊卖家中心 A+ Content Manager 中，上传图片必须填写的 Image Keywords（ALT 文本）**严格受后台系统字符限制：不得超过 100 个字符（≤ 100 characters，含空格）**。一旦超过 100 字符，后台系统将直接报错拦截，导致无法保存或提交审核！

- **字符上限**：**严格 ≤ 100 字符（建议 50–95 字符最佳安全区间）**。
- **编写原则**：
  - 用一句精简流畅的自然英文描述可见画面主体、核心零件与使用动作；
  - 严禁为了堆砌 A9 关键词而写超 100 字符；
  - 严禁包含注册商标侵权词（如 Velcro）、保修词（warranty）或未认证环保词（eco-friendly）；
  - 必须按页面模块从上到下、图从左到右编号：`A+1:`、`A+2:`、`A+3:`……
  - 父体共用 A+ 输出一块 `### A+ ALT（父体共用）`。

---

## Search Terms（ST，官方硬性限制 < 250 字节）

- **字节上限**：美国站 `generic_keywords` **严格小于 250 字节（< 250 Bytes，以 UTF-8 字节计算，不是字符数）**。达到或超过 250 字节，亚马逊系统将直接放弃对整个字段建立索引！
- **格式规范**：空格分隔，全部小写，无需逗号或分号。
- **收录**：前台标题、五点、属性中未出现的真实同义词、次要场景词、原料/材质长尾词。
- **剔除**：自身品牌、竞品品牌、ASIN、标题/五点已有词、夸大词、warranty。
- 代码块只有那一行干净的小写词，字节数标在思考区。用脚本严格核验字节。


---

## 批量上传表格（Flat Table TSV）与 PartialUpdate 安全准则

为便于运营团队直接在卖家中心（Seller Central -> Catalog -> Add Products via Upload）进行批量刷新，交付报告必须提供符合官方模板规范的 TSV（Tab-Separated Values）纯文本平铺表格。

### 1. `update_delete = PartialUpdate` 铁律（防数据被清空）
- **核心风险**：在亚马逊 Inventory Loader 或 Category Specific Flat File 中，`update_delete` 字段若为空或误填为 `Update`，亚马逊系统将把当前表格中留空的所有字段（如未上传的副图 URL、历史属性、合规认证信息等）**判定为删除并直接全量清空覆盖**！
- **强制规范**：**所有用于优化刷新的 Flat Table 表格，`update_delete` 列必须 100% 显式填写 `PartialUpdate`**。这确保系统仅更新表格中填写的标题、五点、属性、ST 等目标字段，其余后台已有资产不受任何影响。

### 2. 变体父子层级结构（Parent-Child Variation Structure）
对于多变体 Listing，平铺表格必须完整呈现父体行与子体行：
- **父体行（Parent Row）**：
  - `parent_child`: `Parent`
  - `parent_sku`: [留空]
  - `relationship_type`: [留空]
  - `variation_theme`: 如 `ColorName`、`SizeName` 或 `ColorName-SizeName`
  - 父体不填具体价格、条形码与尺寸规格，但可带共用的父体标题与五点。
- **子体行（Child Rows）**：
  - `parent_child`: `Child`
  - `parent_sku`: 填入父体 SKU
  - `relationship_type`: `Variation`
  - `variation_theme`: 与父体保持完全一致
  - 填入对应子体的专用变体属性（如 `color_name`、`size_name`）、条码、独立标题与图片。

### 3. 表格代码块格式
在报告中以 ```tsv 代码块提供，首行为标准表头，后续每行以 Tab 键（`\t`）分隔字段，运营可一键复制并粘贴至 Excel 或另存为 UTF-8 文本文件直接上传。
