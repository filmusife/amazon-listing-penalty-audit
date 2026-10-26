# Rufus / COSMO 发现层与事实对齐

写标题、五点、属性、A+、ALT、Search Terms 时读。政策底线和 1–10 项判定仍以 amazon-policy / seven-items / extra-items 为准。本文件指导「合规之后怎么写，才对 AI 对话检索、常识图谱以及 CTR/CVR 提升有用」。

Amazon 面向买家的购物助手（Rufus / Alexa for Shopping）核心检索机制：**读取结构化属性和可引用权威事实，而非计算关键词堆砌密度**。

---

## 优化思考的三层递进模型

1. **第一层：政策合规底线（Floor）**：违规词、超长标题（>200字符）、图上徽章、EPA/商标侵权词先清掉。不能为了「SEO 检索」把违禁词留在 PDP。
2. **第二层：事实一致性与降低 INAD（Consistency）**：尺寸、变体、节点、ALT、ST、数字、价格、串色、夸大词、A+ 与子体完全一致。自相矛盾会导致多退货、少展示，再反向压制自然位。
3. **第三层：AI 发现栈与转化引擎（Discovery & Conversion Stack）**：
   - **Lexical retrieval（A9/A10 候选集召回）**：标题（60-80 字符黄金区 + 80-180 字符长尾区）、五点、ST 把核心同义词自然出现一次，进入搜索候选集。不连写、不堆砌、不抄标题进 ST。
   - **COSMO（买家意图常识图谱）**：关心 who / where / when / 解决什么问题 / 场合 / 和什么搭配用。优先填满 `intended_use`、`target_audience`、`occasion`、`item_type` 等 discovery 属性。
   - **Rufus / Alexa for Shopping（可引用事实闭环与 CVR 转化）**：提供可直接引用的权威事实。数字和分类走属性栏；五点回答买家核心疑问；A+ 正文与对比表提供深度说明；ALT 提供多模态图像检索源。**空属性 = 助手无法回答 = 买家问答时推荐竞品**。

---

## 各字段在发现层与转化层的写法

- **标题（CTR 命脉 + 搜索召回）**：
  - **前 60–80 字符**：`[品牌] + [核心品类词] + [核心规格/参数] + [关键卖点]`。在移动端搜索折叠前完成心智闭环，锁定 **点击率（CTR）**。
  - **80–180 字符**：容纳高权重长尾搜索词与末尾变体词，满足 A9/COSMO 自然搜索召回。
- **Item highlights（移动端 CVR 核心）**：标题装不下的材料、场景、配件短语（≤125 字符，逗号短语）。买家 3 秒速读确认购买意图。若类目模板无此字段，前置合并入五点。
- **五点（Bullet Points，对齐 2024 年 8 月 15 日新规）**：一条一个买家核心问题，提供权威事实（末尾不加句号，无违禁符号）：
  1. *是什么 / 给谁用* (`Used_For_Audience` + `Is_A`)
  2. *可测量规格事实* (`Capable_Of` / 属性直接引用，消除退货风险)
  3. *核心功能与解决的痛点* (`Used_For_Func` / `Used_To`，激发购买欲望)
  4. *使用场景或场合* (`Used_In_Loc` / `Used_For_Event`，COSMO 意图对齐)
  5. *箱内配件与使用边界* (`Used_With` + 降低 INAD 退货，明确边界)
- **属性（Attributes）**：**优先级高于改写 Search Terms**。填满该类目的 discovery 字段：`item_type`、`intended_use`、`target_audience`、`occasion`、`material`、`capacity/size`、`included_components`、`care_instructions`、`compatibility`。数字必须全 Listing 统一口径。
- **A+ 页面**：当成产品知识库，而不是纯海报。正文、对比表、FAQ、图上文字（会被 OCR 识别）、ALT 必须全部为真。
- **Search Terms**：严格 < 250 字节，只补前台未出现的真实同义词与长尾意图词，严禁品牌、ASIN、重复词。

---

## COSMO 常识图谱核对表（有依据才映射）

| 买家意图问题 | COSMO 图谱关系 | 建议填写字段 |
|---|---|---|
| 这是什么 | `Is_A` / `Used_As` | 标题品类词、`item_type_keyword` |
| 给谁用 | `Used_For_Audience` / `Used_By` | 属性 `target_audience`；五点第 1 条 |
| 解决什么痛点 | `Used_For_Func` / `Used_To` / `Capable_Of` | 属性 `intended_use`；五点功能条 |
| 在哪 / 何时用 | `Used_In_Loc` / `Used_For_Event` | Item highlights 或五点场景条 |
| 包含什么配件 | `Used_With` | 属性 `included_components`；五点配件条 |
| 适用什么设备 | `Used_On` | 属性 `compatibility`；五点边界条 |
| 不能用在什么上 | *使用边界（降低退货）* | 五点最后一条或 A+ FAQ 说明 |

---

## Rufus 模拟问答压力测试（5 组 QA 审计规范）

在完成 Listing 优化后，必须进行 **【Rufus 模拟问答压力测试】**，检验优化后的事实能否支撑 AI 助手的问答闭环：

1. **Q1（适用人群/对象）**：*“Who is this product designed for?”*
   - *检验点*：能否直接引用五点 1 或属性 `target_audience` 给出精准受众，而不含糊其辞。
2. **Q2（核心规格/容量）**：*“What is the exact capacity / size / power?”*
   - *检验点*：能否引用单一准确的数字事实，且不出现图文冲突的两套数字。
3. **Q3（配件清单）**：*“What items are included in the box?”*
   - *检验点*：能否准确列举 `included_components`，避免买家以为有赠品而产生差评。
4. **Q4（兼容性与使用场景）**：*“Can I use this with [X] / in [Location]?”*
   - *检验点*：能否在属性或五点中找到明确的兼容/场景事实。
5. **Q5（使用边界与限制）**：*“Is this dishwasher safe / waterproof / suitable for [Y]?”*
   - *检验点*：能否给出权威明确的否定或肯定回答，防止买家错误使用导致退货。

若某问题 PDP 无事实支撑，在报告中明确标出 `RUFUS_FACT_GAP`，提示卖家在属性或 A+ 中补充事实。


---

## COSMO 15 节点意图常识图谱全映射表

COSMO 意图图谱通过买家真实行为数据训练，构建实体与生活场景的多跳关系。Listing 必须在文案中自然嵌入这些语义三元组，才能被常识图谱有效收录并主动推流：

| # | COSMO 核心图谱关系 | 语义含义 | 最佳落地字段与文案承载规范 |
|---|---|---|---|
| 1 | `Is_A` | 产品本质类别 | 标题首部品类词、`item_type_keyword`（必须精准，严禁泛词） |
| 2 | `Used_For_Audience` | 目标受众人群 | 属性 `target_audience`、五点 Bullet 1 开头 |
| 3 | `Used_By` | 实际使用者/执行者 | 五点受众描述（如 "baristas, home cooks, beginners"） |
| 4 | `Used_For_Func` | 核心功能机制 | 标题卖点、五点 Bullet 2/3（动词短语：grind, blend, steam） |
| 5 | `Used_To` | 买家最终想要达成的目的 | 五点利益点（如 "brew fresh morning espresso, prepare baby puree"） |
| 6 | `Capable_Of` | 机器/材质具备的硬性能力 | 属性参数（如 `capacity: 70g`, `power: 200W`, `noise: 63dB`） |
| 7 | `Used_In_Loc` | 使用的具体物理空间 | 五点场景条、Item highlights（如 "kitchen countertop, RV, dorm"） |
| 8 | `Used_For_Event` | 发生的生活事件/场合 | 属性 `occasion`、五点场景描述（如 "holiday gathering, camping trip"） |
| 9 | `Used_With` | 搭配使用的工具/配件 | 属性 `included_components`、五点 Bullet 5（装箱配件清单） |
| 10| `Used_On` | 作用的对象/食材/媒介 | 属性 `intended_use`、五点范围（如 "coffee beans, spices, dry nuts"） |
| 11| `Made_Of` | 物理材质与工艺 | 属性 `material`、五点材质说明（如 "304 food-grade stainless steel"） |
| 12| `Has_Property` | 关键物理特性 | 属性与 highlights（如 "compact, BPA-free, one-touch, detachable"） |
| 13| `Requires` | 运行所需的前提条件 | 属性与五点（如 "120V outlet, hand wash, pre-soaking"） |
| 14| `Prevents` | 能够预防的不良问题 | 五点痛点阻断（如 "prevents overheating, stops powder spillage"） |
| 15| `Not_Used_For` | 明确的使用边界（防退货） | 五点 Bullet 5 与 A+ FAQ（如 "not for wet grinding, hand wipe only"） |

---

## Rufus 事实就绪度量化评分模型（Rufus Fact Readiness Score, 0–100）

Rufus 等大语言模型购物助手的本质是**“基于可信事实的问答与推荐生成”**。如果 PDP 中只有口号而没有硬核事实，Rufus 在买家提问时将产生信息盲区或直接引用竞品。我们设立 4 个维度（各 25 分）量化评价 Listing 的事实就绪度：

| 评估维度 | 分值 | 检验指标与得分标准 | 典型失分陷阱 |
|---|---|---|---|
| **1. 显式规格事实覆盖度 (Explicit Spec Coverage)** | 25 分 | 核心物理参数（容量、长宽高、材质、功率、电压）在后台 Attributes 与五点中均有明确单一文字口径，图文一致。得 20-25 分。 | 数字仅印在图片上、后台属性全空白、标题五点数字互相打架（得 0-10 分）。 |
| **2. 负向边界与退货防御度 (Negative Scenario Defense)** | 25 分 | 明确标注清洗方式（机洗/手擦）、能否处理湿性食材、适用/不适用场景，前置消灭买家误用差评。得 20-25 分。 | 含糊其辞宣称“全能”，买家买回家发现无法机洗或烧毁电机怒打一星（得 0-10 分）。 |
| **3. 场景与兼容性映射度 (Context & Compatibility)** | 25 分 | 准确填入 `intended_use`、`compatibility`、`target_audience`，形成闭环场景语义。得 20-25 分。 | 宣称“universal / fits all”却无具体型号对照，买家提问“能否用于我的车”时助手无法作答。 |
| **4. 问答截流与差异化优势 (Q&A Interception & Edge)** | 25 分 | 具备明确对比事实（如噪音 dB 数值、BPA-Free 认证材质、可拆卸设计），支持助手向买家推荐本品。得 20-25 分。 | 纯空洞形容词（best, great, amazing），无任何第三方可验证事实支持推荐（得 0-10 分）。 |

- **90–100 分（AI 优先推荐级）**：事实完备闭环，Rufus 拟真问答 5 组全部正面直接作答，推荐权重极高。
- **75–89 分（合格支撑级）**：主要事实具备，个别使用边界待补充。
- **50–74 分（事实欠缺级）**：属性栏大面积空白，主要依靠文本模糊推测，存在被竞品截流风险。
- **0–49 分（信息盲区级）**：充斥夸大词与宣传口号，无结构化事实，AI 问答直接判定为不可靠来源。
