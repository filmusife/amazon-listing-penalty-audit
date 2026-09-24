# Rufus / COSMO 发现层

写标题、五点、属性、A+、ALT、Search Terms 时读。政策底线和 1–10 项判定仍以 amazon-policy / seven-items / extra-items 为准。本文件只改「合规之后怎么写，才对发现层有用」。

Amazon **没有公布** Rufus / Alexa for Shopping 的完整排名公式。第三方博客里的「必须覆盖 8/15 条 COSMO 关系」「Q&A 提升 3.2 倍」一律当启发式，不要写成铁律，也不要为了凑关系编造前台没有证据的场景。

2026-05 起，面向买家的助手品牌从 Rufus 并入 **Alexa for Shopping**。检索思路没换：读结构化属性和可引用事实，而不是关键词密度。下文仍可用 Rufus 指这层对话检索。

## 三层，按这个顺序想

1. **政策底线。** 违规词、超长标题、图上徽章先清掉。不能为了「堆检索词」把 warranty / best / 促销语留在 PDP。
2. **一致 / INAD。** 尺寸、变体、节点、ALT、ST、数字、价格、串色、夸大词、A+ 与子体一致。自相矛盾会少展示、多退货，再反向压权重。
3. **发现栈（合规且一致之后）：**
   - **Lexical retrieval（A9/A10）：** 标题、五点、ST 里把核心同义词各出现一次，让商品能进候选集。不要同一词连写、管道符堆砌、把标题整段抄进 ST。
   - **COSMO：** 常识知识图谱关系。关心的是 who / where / when / 解决什么问题 / 场合 / 和什么一起用，而不只是标题里有没有那个词。优先填 intended_use、	arget_audience、occasion、item type 等 discovery 属性。
   - **Rufus / Alexa for Shopping：** 要能被引用。数字和分类问题优先走属性栏；每条五点回答一个买家会问的问题；A+ 正文、对比表单元格、图上 overlay、ALT 都是检索源。空属性 = 助手无法回答 = 更容易推荐别人。

思考区必须标明这次改动服务哪一层：政策 / COSMO 关系 / Rufus 可引用事实 / Lexical 同义词。禁止写「堆 A9 词」。

## 写字段时怎么用

**标题。** 品牌 + 品类 + 1–2 个已验证规格；75 字符还装得下再加受众或使用场景。不要关键词汤。变体词放最后。

**Item highlights。** 标题装不下的材料、场景、配件。逗号短语。适合放 COSMO 的 where / who，但不要重复标题。

**五点。** 一条一个买家问题，不要管道符堆词。建议顺序（有证据才写，缺的留空不要编）：
1. 是什么 / 给谁用（Used_For_Audience + Is_A）
2. 可测量规格（Capable_Of / 属性可引用）
3. 关键功能或解决问题（Used_For_Func / Used_To）
4. 使用场景或场合（Used_In_Loc / Used_For_Event）
5. 箱内配件或使用边界（Used_With + 降低 INAD）

句式仍遵守 Seller Central：首字母大写、句末不加句号。可以是能读懂的短语，不要营销口号。

**属性。** 比再改一遍 Search Terms 更优先。填满该类目能填的 discovery 字段：item type、intended use、target audience、occasion、material、capacity/size、included components、care、compatibility。数字必须和图、A+、五点同一口径。空字段不要用营销词凑。

**A+。** 当知识库，不当海报。文字模块、对比表、FAQ、图上 overlay、ALT 都必须对 **当前子体** 为真。overlay 上的数字会被 OCR；和属性打架等于给助手两套答案。

**Search Terms。** 只补前台没有的同义词，外加少量意图短语（场景、受众、任务）。不放品牌、ASIN、best、warranty，不把标题再抄一遍。

**图。** 助手会读 overlay 文字。特征图写规格/配件/边界，不要写 premium / warranty 徽章。ALT 描述可见内容，帮助图搜，也给对话层一个短句源。

**保修。** 不进任何 Rufus 面向字段。Warranty 专用属性另填。

**Q&A。** 现网 PDP 若已无独立 Q&A 模块，不要把「去种 Q&A」当成必须改法。能引用的事实写进五点、属性、A+ 即可。

## COSMO 关系（有证据才映射）

论文（Yu et al., SIGMOD 2024）定义了 15 类常识关系。体检时用下面这张短表核对覆盖，**不要为凑满 15 条发明场景**。前台、属性、图上能支撑的才写进文案。

| 买家能问的 | 关系（启发式） | 写到哪 |
|---|---|---|
| 这是什么 | Is_A / Used_As | 标题品类、item type |
| 给谁用 | Used_For_Audience / Used_By | 属性 target audience；五点第 1 条 |
| 干什么 / 解决什么 | Used_For_Func / Used_To / Capable_Of | 属性 intended use；五点功能条 |
| 在哪 / 何时用 | Used_In_Loc / Used_For_Event | Item highlights 或五点场景条 |
| 和什么一起 / 箱内有什么 | Used_With | Included Components；五点配件条 |
| 用在什么上 / 兼容 | Used_On | 属性 compatibility；五点边界 |
| 不适合谁 / 限制 | （降低 INAD，不是硬凑关系） | 五点最后一条或图上限制 |

报告里用四问做覆盖检查即可：谁用、在哪用、箱内有什么、使用边界。答不上来的标缺口，不要编。

## 明确不要做

- 不要把旧 A9 密度（同一词在标题五点 ST 连写三遍）当成优化。
- 不要把 15 条关系写进标题。
- 不要要求用户去「种 Q&A」或伪造评论。
- 不要把第三方转化倍数写进对用户的承诺。
- 发现层优化不能压过政策：75 字符、无 warranty、无竞品品牌，仍然先满足。
