# Amazon Listing 隐性减分体检与 CTR/CVR 增长审计

以亚马逊最新 Seller Central 规则为底线，对任意品类 Listing（默认美国站）做 7 个隐性减分项加 3 个扩展项体检，深度对齐 **A9/A10 检索召回、COSMO 意图常识图谱与 Rufus 生成式购物助手**，输出以提升 **点击率（CTR）与转化率（CVR）** 为核心的落地诊断报告与全套合规文案。

全品类通用，品类差异通过专属 overlay 解析。区分促销秒杀与真实改价，纠偏合规后强化事实发现层，告别盲目堆砌关键词。

## 核心特性

- **0–100 风险量化评分**：基于官方红线分级量化风险（健康良好 / 中度风险 / 高危受限 / 极度危险）。
- **爬虫管道符智能清洗**：自动解耦爬虫/ERP/`<title>` 标签拼接的管道符 ` | `，杜绝误判卖家违规与虚假“系统腰斩”。
- **移动端 65 字符首屏呈现模拟**：诊断并重构标题黄金展示区（品牌 + 核心品类 + 核心规格），大幅拉升移动端 **点击率（CTR）**。
- **2024 年 8 月 15 日五点新规排查**：严格筛查末尾句号、ALL CAPS、特殊符号/货币/Emoji（`™ ® © … † ‡ ± ~ € £ ¥ ✓ ❌ ★ 【】` 等），防止被亚马逊 AI 强制重写。
- **官方硬性限制防线**：
  - 标题硬上限：≤ 200 字符（超限触发搜索抑制）。
  - Item Highlights：≤ 125 字符（移动端首屏 3 秒转化核心）。
  - 五点描述：推荐 3–5 条，单条 ≤ 255 字符，总长 ≤ 1,000 字符。
  - A+ 图片 ALT：严格 ≤ 100 字符（A+ Content Manager 系统硬上限）。
  - Search Terms：严格 < 250 字节（UTF-8 编码，非字符数）。
- **高危下架红线排查**：EPA/FIFRA 未申报杀菌农药宣称、第三方注册商标通用化侵权陷阱（Velcro、Thermos、PopSockets 等）、未认证环保宣称（eco-friendly 等）。
- **双轨交付（Dual Delivery）**：同时输出单字段纯英文独立代码块（Seller Central 网页端直接粘贴）与整套全变体 **标准平铺表格（Flat Table / TSV 格式）**（直接导入官方库存批量上传模板）。
- **Rufus 5 组模拟问答压力测试**：闭环检验人群定位、核心规格、装箱清单、使用场景与维护边界，杜绝买家向 AI 提问时被竞品截流。

## 安装

把本仓库克隆到你的 skills 目录（如 Codex / Antigravity）：

```bash
git clone https://github.com/filmusife/amazon-listing-penalty-audit.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/amazon-listing-penalty-audit"
```

已存在同名目录时，直接拉取或用本仓库内容覆盖即可。

## 调用

在对话中输入 ASIN 并附带以下任一触发词即可：

- `/listing-audit`
- `$amazon-listing-penalty-audit`
- `/penalty-audit`
- 隐性减分 / 静默降权体检

示例：

```text
/listing-audit 检查美国站 ASIN B0XXXXXXXX 的隐性减分，优化 CTR 与 CVR，覆盖全部变体。
```

## 10 项体检矩阵

1. **Size / Weight / Dimensions 不一致与逻辑错乱**
2. **变体主题与标题双层架构（前 65 字符 CTR 黄金区 + 120–180 字符长尾索引区）**
3. **Browse node 多选或错选**
4. **图片 ALT 空白、错语言、空泛或超限（A+ ALT 严格 ≤ 100 字符）**
5. **Search Terms 埋竞品品牌/ASIN/超 250 字节**
6. **描述 / 图片数字与实物不符（消灭 INAD 货不对板退货）**
7. **30 天 list price 改价超过 5 次（秒杀/券 V 型不计）**
8. **跨变体图片串色 / 规格图错配**
9. **夸大词 / 政策违禁词 / 2024新规符号排查（含保修、EPA、商标侵权）**
10. **A+ 对比表 / FAQ / 视频与当前子体不一致**

## 目录结构

- `SKILL.md`：核心流程、官方铁律与双轮驱动增长指引
- `scripts/scan_listing.py`：确定性扫描脚本（支持 `--self-test` 自动化验证）
- `references/amazon-policy.md`：亚马逊卖家中心现行政策红线与展示机制
- `references/copy-rules.md`：CTR/CVR 文案优化与双轨交付标准规范
- `references/report-template.md`：完整体检诊断报告结构模板
- `references/rufus-cosmo.md`：COSMO 意图图谱与 Rufus 5 组问答测试规范
- `references/seven-items.md`：1–7 核心减分项判定标准
- `references/extra-items.md`：8–10 扩展项判定标准
- `references/evidence-collection.md`：证据收集与数据解耦清洗规范
- `references/category-overlays.md`：细分类目专属覆盖层
