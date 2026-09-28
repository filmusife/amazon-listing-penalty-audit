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

相关页按需打开：图片总要求 `1881`、属性/关键词 `F2C2L6RCFZGWBXC`、一般上架限制 `201707070`、A+ Content guide。登录墙打不开时不要假装已经核对现行页。

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

## 标题策略（分级管控与品类弹性）

- **长度分级**：
  - **核心移动端安全区（≤ 75 字符含空格）**：亚马逊官方针对新类目和移动端展示鼓励的长度。若字符超出可能在移动端截断或被系统自动压制。新上架或因违规被动重写的标题，首选 ≤75 字符。
  - **类目弹性安全区（76–120 字符）**：对于复杂 3C、汽配（含适用年款）、工业配件等必须携带规格与兼容性的类目，若类目竞品普遍在 100 字符且未受压制，可采用该区间，但核心信息（品牌+品类+关键规格）必须在前 70 字符完整表达。
  - **高危溢出区（> 150 字符）**：极易触发截断或抑制，必须精简重写。
- **溢出卖点分流**：
  - 首选进入 **Item highlights**：≤125 字符，逗号短语，不写句子。
  - *兜底策略*：若该商品所属类目后台**无 Item highlights 属性**，严禁让卖家无处粘贴，应将溢出卖点有序编入五点前 2 条的前置短语中。
- **禁止字符**：`! $ ? _ { } ^ ¬ ¦`。`~ # < > *` 只能当型号或计量，不能当装饰。
- **英雄子体保护**：已有长标题若仍正常展示、小类排名稳定、且 **没有政策违规**：英雄子体可暂不改动标题，避免打乱既有权重。一旦含违规词（warranty、guarantee、夸大词、商标侵权），必须立即重写，排名好也不能留。

---

## 五点（Bullet Points）

- 至少 3 条独特卖点，建议 5 条；常见单条约 10–255 字符（以类目模板为准）。
- 首字母大写；写成短语，**句末不加句号**；不要整条 ALL CAPS；不用 【】★ emoji ™ ®。
- 禁止：Guarantee information；EPA 未备案杀菌词；无依据的 bamboo/soy/organic 宣称；ASIN；N/A TBD；公司网址电话；同一事实在多条重复。
- 主观比较词（best、#1、better than、quieter than、guaranteed）没有外包装或权威第三方依据严禁写入。
  - *例外白名单*：说明使用方式的操作短语如 `for best results`、`best before`，属于合规指导语，不属于违规夸大。

---

## 图片 / A+

任何产品图都禁止 warranty、guarantee、促销、虚假认证徽章，以及 mimic Amazon 的图形。禁止字符串包括但不限于：`warranty`、`guarantee`、`best`、`amazon`、`prime`、`fda`、`certified`、`coupon`、`free`、`sale`。

主图：纯白底（RGB 255, 255, 255）、产品占画面 85% 以上、无文字徽章。特征图可以有尺寸/功能标注，但标注数字必须和属性/五点一致，且不能变成促销章。

---

## Search Terms（搜索词）

- 美国站 `generic_keywords` **小于 250 字节**。达到或超出 250 字节将导致整段词条完全不被亚马逊建立索引。
- 只放前台未出现的同义词、缩写、次要使用场景、材质长尾词。
- 严禁放置：自身品牌、竞品品牌、任何 ASIN、best/cheapest、on sale、重复前台已有词汇。

---

## 权重怎么用这些规则

合规不是终点，而是地基。政策清掉违规词之后，用腾出的位置写 **可验证、可筛选、能被 Rufus 引用、能降低 INAD 退货** 的信息：规格、材质、箱内配件、真实功能、使用场景和受众。发现层奖励的是完整属性和一致事实，不是堆保证口号，也不是把同一个关键词连写三遍。
