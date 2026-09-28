# Rufus / COSMO 发现层与事实对齐

写标题、五点、属性、A+、ALT、Search Terms 时读。政策底线和 1–10 项判定仍以 amazon-policy / seven-items / extra-items 为准。本文件指导「合规之后怎么写，才对 AI 对话检索与图谱有用」。

Amazon **没有公布** Rufus / Alexa for Shopping 的完整权重公式。第三方博客里的「必须覆盖 8/15 条 COSMO 关系」「Q&A 提升 3.2 倍」一律当启发式，不要写成铁律，更不要为了凑关系编造前台没有证据的虚假场景。

面向买家的购物助手（Rufus / Alexa for Shopping）核心检索机制：**读取结构化属性和可引用权威事实，而不是计算关键词堆砌密度**。

---

## 优化思考的三层递进模型

1. **第一层：政策合规底线（Floor）**：违规词、超长标题、图上徽章、EPA/商标侵权词先清掉。不能为了「SEO 检索」把违禁词留在 PDP。
2. **第二层：事实一致性与降低 INAD（Consistency）**：尺寸、变体、节点、ALT、ST、数字、价格、串色、夸大词、A+ 与子体完全一致。自相矛盾会导致多退货、少展示，再反向压制自然位。
3. **第三层：AI 发现栈（Discovery Stack）**：
   - **Lexical retrieval（A9/A10 候选集召回）**：标题、五点、ST 把核心同义词自然出现一次，进入搜索候选集。不连写、不堆砌、不抄标题进 ST。
   - **COSMO（买家意图常识图谱）**：关心 who / where / when / 解决什么问题 / 场合 / 和什么搭配用。优先填满 `intended_use`、`target_audience`、`occasion`、`item_type` 等 discovery 属性。
   - **Rufus / Alexa for Shopping（可引用事实闭环）**：提供可直接引用的权威事实。数字和分类走属性栏；五点回答买家核心疑问；A+ 正文与对比表提供深度说明；ALT 提供多模态图像检索源。**空属性 = 助手无法回答 = 买家问答时推荐竞品**。

---

## 各字段在发现层的写法

- **标题**：`品牌 + 品类 + 1–2 个已验证核心规格 + 变体词`。75 字符（推荐）或类目安全长度内完成，拒绝关键词堆砌。变体词固定放末尾。
- **Item highlights**：标题装不下的材料、场景、配件短语（≤125 字符，逗号短语）。若类目模板无此字段，前置合并入五点。
- **五点（Bullet Points）**：一条一个买家核心问题，提供权威事实：
  1. *是什么 / 给谁用* (`Used_For_Audience` + `Is_A`)
  2. *可测量规格事实* (`Capable_Of` / 属性直接引用)
  3. *核心功能与解决的痛点* (`Used_For_Func` / `Used_To`)
  4. *使用场景或场合* (`Used_In_Loc` / `Used_For_Event`)
  5. *箱内配件与使用边界* (`Used_With` + 降低 INAD 退货)
- **属性（Attributes）**：**优先级高于改写 Search Terms**。填满该类目的 discovery 字段：`item_type`、`intended_use`、`target_audience`、`occasion`、`material`、`capacity/size`、`included_components`、`care_instructions`、`compatibility`。数字必须全 Listing 统一口径。
- **A+ 页面**：当成产品知识库，而不是纯海报。正文、对比表、FAQ、图上文字（会被 OCR 识别）、ALT 必须全部为真。
- **Search Terms**：只补前台未出现的真实同义词与长尾意图词，严禁品牌、ASIN、重复词。

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
