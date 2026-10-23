# 美国站 Listing 政策底线与合规红线

写任何标题、五点、Item highlights、图片 ALT、A+、Search Terms 之前先读本文件，并打开下面的 Seller Central 页面。

本文件是核对过的 **US** 政策快照，**不是永久真理，也不是全球站点真理**。拉到的现行帮助页覆盖这里的条款。拉失败则沿用本快照，并在报告标 `POLICY_FETCH_FAILED`。

非美国站：先开该站点 Seller Central 对应帮助页。当地规则覆盖本快照。拉不到则继续用本快照体检，并标 `MARKETPLACE_UNVERIFIED`。不要把 US 的 75 字符标题建议默认套到所有站点。

## 每次必开的页面（US）

- 标题：[Product title requirements](https://sellercentral.amazon.com/help/hub/reference/external/GYTR6SYGFA5E3EQC?locale=en-US)
- 五点：[Product bullet point requirements](https://sellercentral.amazon.com/help/hub/reference/external/GX5L8BF8GLMML6CX?locale=en-US)
- 误导/违禁宣称：[Misleading and prohibited claims](https://sellercentral.amazon.com/help/hub/reference/external/G202024200?locale=en-US)
- 图片徽章：[Prohibited badging](https://sellercentral.amazon.com/help/hub/reference/external/GQ2VU6MXD8H6VGSU?locale=en-US)
- 详情页总规则：[Product detail page rules](https://sellercentral.amazon.com/help/hub/reference/external/G200390640?locale=en-US)
- 搜索词：[Search terms / generic keywords](https://sellercentral.amazon.com/help/hub/reference/external/GNYWHX2TP7C8GXHK?locale=en-US)
- 农药与杀菌设备：[Pesticides and pesticide devices](https://sellercentral.amazon.com/help/hub/reference/external/202115120)
- A+ 页面指南与规格：[A+ Content specifications and best practices](https://sellercentral.amazon.com/help/hub/reference/external/G202102950)

相关页按需打开：图片总要求 `1881`、属性/关键词 `F2C2L6RCFZGWBXC`、一般上架限制 `201707070`。登录墙打不开时不要假装已经核对现行页。

---

## 亚马逊官方各模块字段规范与硬性限制汇总表

| 模块 / 字段 | 亚马逊官方硬性系统限制 | 推荐最佳实践 / 安全区间 | 违规严重后果与算法影响 |
|---|---|---|---|
| **标题（Title）** | **≤ 200 字符**（含空格）<br>严禁符号 `! $ ? _ { } ^ ¬ ¦` | **前 60–80 字符黄金区（CTR核心）**：`品牌 + 核心品类词 + 核心参数/型号`<br>**全长 120–180 字符安全索引区**：承载长尾词，留足 20 字符余量防超限 | 超过 200 字符触发**搜索抑制（Search Suppressed）**；若前 65 字符漏填品牌/品类，移动端搜索卡片严重折叠导致 **点击率（CTR）暴跌** |
| **五点（Bullet Points）**<br>*(2024年8月15日新规)* | 建议 3–5 条，单条 ≤ 255 字符，总长建议 ≤ 1,000 字符；**严禁任何特殊符号/Emoji**（`™ ® © … † ‡ ± ~ € £ ¥ ✓ ❌`）；**末尾严禁加句号** | **单条 150–240 字符**，采用 `[加粗/大写特性标签]: [利益点与事实阐述]` 结构；句末不加句号，短语间用分号 `;` 分隔 | 违规触发**亚马逊生成式 AI（Rufus/Listing AI）强制重写或隐性降权**；手机端长文本折叠导致 **转化率（CVR）下滑** |
| **Item Highlights** | **≤ 125 字符**（含空格） | **80–120 字符**，逗号分隔的 3–4 个高密度规格/材质/场景短语 | 超过字符限制后台直接报错拦截；填满可显著抢占移动端首屏转化视线，提升 **CVR** |
| **Search Terms（ST）** | **严格 < 250 字节**（以 UTF-8 字节计算，非字符数） | **180–245 字节**，纯英文小写空格分隔，填满前台未覆盖的长尾同义词 | 达到或超过 250 字节整段词条**被 A9 引擎完全放弃建立索引**；重复前台词浪费宝贵权重预算 |
| **A+ 图片 ALT** | **严格 ≤ 100 字符**（A+ Content Manager 系统硬上限） | **50–95 字符**，精准、自然描述画面中的产品主体、核心零件与使用动作 | 超过 100 字符后台**报错拦截，无法保存或提交审核**；优质 ALT 支撑 Rufus 多模态图文问答召回 |
| **图库主图（MAIN）** | 纯白底（RGB 255, 255, 255），产品占画面 ≥ 85% | 极简高质感实物图，严禁任何文字/徽章/边框/附赠配件 | 违规触发主图被系统自动屏蔽移除或静默降权，直接摧毁 **CTR** |
| **属性（Attributes）** | 真实准确填入对应物理度量衡，严禁自相矛盾 | 全面填满类目专属 discovery 字段（`intended_use`、`target_audience`、`capacity` 等） | 属性缺失或冲突导致类目筛选器被过滤，买家退货率（INAD）激增，Rufus 无法回答直接截流推荐竞品 |

---

## 高危红线 1：保修 / 保证放哪

**严禁**写进标题、五点、Product Description、图库、A+、ALT、Search Terms。

Seller Central 五点的 Prohibited content 明确禁止 **Guarantee information**，示例包括 Full refund、If not satisfied send it back、Unconditional guarantee with no limit。标题也禁止 `100% quality guaranteed` 这类促销保证。图片禁止 warranty / guarantee 徽章和对应英文词。

保修只进 **Warranty 文档 / warranty 专用属性**。思考区可以告诉用户去哪个后台字段填；粘贴块里不要出现 warranty、guarantee、money-back、2-year manufacturer's warranty。

---

## 高危红线 2：EPA / FIFRA 农药与杀菌设备下架雷区

亚马逊美国站使用算法严查 **EPA 农药/杀菌宣称**。 Listing（包括标题、五点、A+、图片文字、后台属性）只要包含以下词汇且未在后台合规提供 EPA 注册号/机构号，将直接面临**整条下架（Ineligible / 5461 抑制）**：

- `antimicrobial` / `anti-microbial`
- `antibacterial` / `anti-bacterial`
- `mold-resistant` / `mildew-resistant`
- `disinfectant` / `disinfecting`
- `fungicidal` / `germicidal`
- `insect-repellent` / `repels pests/bugs/mosquitoes`
- `sterilizer` / `sterilization`（医疗/杀菌器械）

**合规改法**：若商品并非 EPA 注册杀菌产品，一律清除上述词汇。改用物理事实表达，例如用 `easy to clean` 替代 `antibacterial`，用 `moisture-resistant` 替代 `mold-resistant`。

---

## 高危红线 3：注册商标（IP）通用化侵权陷阱

前台文案与 Search Terms 严禁包含误当普通名词的第三方注册商标。亚马逊品牌保护系统（Brand Registry Bot）会自动扫描并触发侵权警告：

| 常见误用词（侵权风险） | 必须改用的官方通用名词 |
|---|---|
| `Velcro` | `hook and loop` / `fastener straps` |
| `Thermos` | `insulated tumbler` / `vacuum bottle` |
| `PopSockets` / `Popsocket` | `collapsible phone grip` / `expanding stand` |
| `Post-it` | `sticky notes` / `self-adhesive notes` |
| `Gore-Tex` | `waterproof breathable fabric/membrane` |
| `Band-Aid` | `adhesive bandage` |
| `Rollerblade` | `inline skates` |
| `Frisbee` | `flying disc` |
| `ChapStick` | `lip balm` |
| `Crock-Pot` | `slow cooker` |
| `Ziploc` | `zipper storage bags` / `resealable bags` |
| `Q-tips` | `cotton swabs` |

---

## 高危红线 4：未认证环保宣称（Green Claims）

亚马逊自 2023–2024 年对环境声明执行严格监管。严禁在标题、五点、A+ 或图片上使用未获官方认证（如 Climate Pledge Friendly 认证资质）的主观环保词：
- 严禁词汇：`eco-friendly`、`environmentally friendly`、`green product`。
- 合规表达：使用具体的物理行为描述，如 `reusable permanent filter eliminates paper waste`（可重复使用的永久滤网减少纸质浪费），不得使用概括性定性环保词。

---

## 标题策略（CTR 黄金展示区与长尾索引布局）

- **长度与展示分层机制**：
  - **官方硬性抑制上限（≤ 200 字符含空格）**：字符数 > 200 会直接触发亚马逊搜索抑制（Search Suppressed），彻底消失在搜索端。
  - **移动端 65 字符首屏黄金展示区（CTR 核心命脉）**：手机端与移动 App 搜索结果卡片采用响应式 CSS（`line-clamp`）只展示标题的前 60–70 字符（后接 `...`）。
    - **算法事实澄清**：移动端折叠是前端 UI 排版，**不是后台系统截断，更不是算法惩罚**！标题后半段的词在 A9/COSMO 索引库中完全生效。
    - **点击率（CTR）驱动原则**：买家在移动端扫视只有 1–2 秒。标题前 65 字符必须严格遵循：`[品牌] + [核心品类词] + [核心规格/型号] + [最大卖点]`。若将品牌或产品词置于 70 字符之后，手机端买家无法识别产品，直接滑过，导致 **CTR 暴跌**。
  - **高权重安全索引区（80–180 字符）**：利用 80–180 字符区间有序容纳核心同义词、兼容机型、材质和次要功能，既充分榨取 A9/COSMO 自然搜索流量，又留有 20 字符安全余量，避免因子变体词变长触发 200 字符硬性抑制。**严禁为机械追求“≤75字符”而粗暴删减卖家的长尾关键词！**
- **禁止字符**：官方明文禁用 `! $ ? _ { } ^ ¬ ¦`。严禁中文全角标点（如全角逗号 `，`）与任何装饰性符号。
- **关于数据抓取中的“管道符 `|`”与排查准则**：
  - 许多数据抓取工具、ERP 系统（如领星）或网页 `<title>` 标签，会自动将【标题】与【Item Highlights】或【品牌/类目】通过管道符 ` | ` 拼接。
  - **体检铁律**：必须先清洗分流数据！**严禁将爬虫拼接的管道符误判为卖家在后台违规，更严禁臆断“亚马逊系统因管道符将标题腰斩”**！若卖家后台确实录入了 `|`，建议温和提示其改用英文逗号 `,` 或连字符 `-`，使语意更通顺。
- **英雄子体保护**：已有长标题若没有政策违规（无 warranty、无夸大词、无商标侵权），且在小类稳定排名出单，切忌随意大改标题结构，避免打乱既有权重；仅在含绝对违规词或超 200 字符时强制重写。

---

## 五点（Bullet Points，严格对齐 2024 年 8 月 15 日新规）

亚马逊在 2024 年 8 月 15 日起对商品五点描述全面引入生成式 AI（Generative AI）审查，不合规的五点将面临**系统自动重写、强制截断或隐性降权**：

- **条数与长度**：建议 3–5 条，单条推荐控制在 **150–240 字符**（系统上限 255 字符），5 条总长控制在 **1,000 字符以内**。
- **格式规范（提升阅读率与 CVR）**：
  - 推荐采用 `[加粗/首字母大写特性标签]: [利益点与可引用事实阐述]` 结构（如 `Food-Grade Materials: Crafted from BPA-free Tritan...`）。
  - **末尾严禁加句号**：官方风格指南明文规定“Do not end with punctuation”（以短语片段呈现，末尾不加 `.`）。短语间用分号 `;` 分隔。
- **2024 官方严打违禁清单（绝对红线）**：
  - **严禁特殊符号与商标**：`™`、`®`、`©`、`…`、`†`、`‡`、`±`、`~`。
  - **严禁货币符号与表情图标**：`$`、`€`、`£`、`¥` 以及各类 Emoji、对勾、星星 (`✓`、`❌`、`★`、`●`、`【】`)。
  - **严禁售后与保证**：`Full refund`、`money-back`、`replacement guarantee`、`warranty` 等（保修仅限后台专用 Warranty 属性）。
  - **严禁未认证宣称**：`eco-friendly`、`anti-microbial`、`bamboo` 等无资质定性宣称。
  - **严禁整段 ALL CAPS**：除开头的特性标签（2–4 个词）可大写外，禁止全句全大写。

---

## 图片 / A+ 深度规则

任何产品图都禁止 warranty、guarantee、促销、虚假认证徽章，以及 mimic Amazon 的图形。禁止字符串包括但不限于：`warranty`、`guarantee`、`best`、`amazon`、`prime`、`fda`、`certified`、`coupon`、`free`、`sale`。

### 主图（MAIN）
纯白底（RGB 255, 255, 255）、产品占画面 85% 以上、无文字徽章。特征图可以有尺寸/功能标注，但标注数字必须和属性/五点一致，且不能变成促销章。

### A+ Content 图片 ALT（Image Keywords，硬性 ≤ 100 字符）
亚马逊卖家后台 A+ Content Manager 在上传图片时，强制要求填写 Image Keywords（ALT 文本）。**系统硬性上限严格限制为 ≤ 100 字符（含空格）**。超出此字符数后台直接弹窗报错拦截，无法保存。
- 编写规范：控制在 50–95 字符之间，自然描述画面可见事实，严禁堆词，严禁违规侵权词。

---

## Search Terms（搜索词）

- 美国站 `generic_keywords` **严格小于 250 字节（< 250 Bytes，UTF-8 编码）**。达到或超出 250 字节将导致整段词条完全不被亚马逊建立索引。
- 只放前台未出现的同义词、缩写、次要使用场景、材质长尾词。
- 严禁放置：自身品牌、竞品品牌、任何 ASIN、best/cheapest、on sale、重复前台已有词汇。

---

## 权重怎么用这些规则

合规不是终点，而是地基。政策清掉违规词之后，用腾出的位置写 **可验证、可筛选、能被 Rufus 引用、能降低 INAD 退货** 的信息：规格、材质、箱内配件、真实功能、使用场景和受众。发现层奖励的是完整属性和一致事实，不是堆保证口号，也不是把同一个关键词连写三遍。
