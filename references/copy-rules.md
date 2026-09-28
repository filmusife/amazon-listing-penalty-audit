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
feed_product_type	item_sku	external_product_id	external_product_id_type	item_name	item_highlights1	bullet_point1	bullet_point2	bullet_point3	bullet_point4	bullet_point5	generic_keywords	standard_price	main_image_url
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

---

## 标题（Title）

- **公式**：`品牌 + 品类 + 1–2 个已验证核心规格 + 变体特征词`（颜色/尺寸/口味放最后）。
- **长度与弹性**：
  - 新上架或重写：默认推荐 ≤ 75 字符（含空格），规避移动端折叠和搜索抑制；
  - 复杂 3C / 汽配 / 工业类目：若需体现必要年款或接口，可放宽至 100–120 字符，但核心信息前 70 字符必须闭环。
- **溢出卖点分流**：
  - 优先放入 **Item highlights**（≤125 字符，逗号分隔短语，不是句子）；
  - *兜底策略*：若该商品所属类目后台**无 Item highlights 属性**，严禁让卖家无处粘贴，应将溢出卖点有序编入五点前 2 条的前置短语中。
- **英雄子体原则**：
  - 若英雄子体标题 **已经合规** 且有稳定小类排名，不要为了“更美观”去改它的标题。该 ASIN 不要输出标题代码块，只在思考区写“不动”和原因。
  - 英雄标题一旦违规（含 warranty、夸大词、超长抑制、商标侵权），必须强制重写，排名好也不能留。
- **其他子体**：套用统一标题模板，仅替换末尾变体词。

---

## 五点（Bullet Points）

- 全部子体 **一字不差**，共用五点里严禁写死某个特定颜色/尺寸。
- 5 条卖点，首字母大写，写成短语，**句末不加标点符号**，禁止整条 ALL CAPS。
- **结构化映射（对齐 COSMO 与 Rufus 问答）**：
  - Bullet 1: *是什么 / 给谁用*（产品定位、目标受众）
  - Bullet 2: *核心可量化规格*（克数、尺寸、功率、成分）
  - Bullet 3: *关键功能 / 解决的痛点*（操作机制、核心效能）
  - Bullet 4: *使用场景 / 场合*（厨房、户外、日常办公）
  - Bullet 5: *箱内清单与使用边界*（明确标配配件，说明不可用于某物，降低退货）
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
| `capacity` | 虚高营销杯数 | 可称重/测量的物理体积或重量口径 |
| `item_weight` | 留空、抄容量 | 真实称重后填入 |
| `warranty_description` | 写入标题/五点 | 仅填入此专用字段 |

属性优先于 Search Terms。同一父体除变体维度外全部复制。

---

## 图库 ALT（Gallery Images）

- 匹配站点语言。美国站英文约 120–180 字符。
- 句式：`{品牌} {变体词} {看得见的产品} with {材质或关键零件} for {图中场景}`
- 必须按每个 ASIN 的实际槽位实图编写：`MAIN:`、`IMG2:`、`IMG3:`……
- 描述当前画面，不堆砌无意义关键词，不写 warranty、best 或竞品词。

---

## A+ ALT（必出）

每个已分析的 A+ 图都必须有一句 ALT：
- 按模块从上到下、图从左到右编号：`A+1:`、`A+2:`、`A+3:`……
- 句式与图库 ALT 一致，描述可见事实。
- 父体共用 A+ 输出一块 `### A+ ALT（父体共用）`。

---

## Search Terms（ST）

- 美国站 < 250 字节，空格分隔，全小写，不重复。用脚本核验字节。
- **收录**：前台未出现的真实同义词、次要场景、材质长尾。
- **剔除**：自身品牌、竞品品牌、ASIN、标题/五点已有词、夸大词、warranty。
- 代码块只有那一行干净的小写词，字节数标在思考区。
