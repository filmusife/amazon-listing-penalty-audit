# 证据怎么收

缺数据就标 `DATA_MISSING`。不要用猜测填重量、功率、实验室噪音、后台节点列表、后台 ST。

## 最低证据包

对用户给的 ASIN 和它的 **全部子 ASIN**：

1. 标题、五点、属性栏（Color/Material/Style/Dimensions）、面包屑、BSR、型号、评分
2. `dimensionToAsinMap` / `variationValues` / parentAsin / 变体主题
3. 每张主图 hiRes：下载后用多模态看图，不要只读文件名
4. A+ 规格、FAQ、对比表数字和笔误
5. Keepa 90 天价格图（改价次数）
6. 图上出现的数字：尺寸标注、杯数、dB、配件赠品字样

## 数据源优先级

1. 卖家精灵 / Sorftime / Keepa 等已配置 MCP（若当前环境可用）
2. Amazon 前台 HTML + 实图
3. 用户提供的后台截图、实测、退货报告

不要为了第 4 项去抓 `amazon.com/product-reviews/` 全站评论；本 skill 不是评论分析。只有当图文数字冲突需要旁证时，才看详情页已有的 Customers say / 可见差评标题。

## 前台看不到、必须交给用户或标缺失

- Search Terms 原文
- 后台 Browse node 完整列表
- Package dimensions / 真实重量（除非图上有）
- 30 天 Seller Central 调价日志（Keepa 只是近似）
- 实验室噪音、铭牌功率

对这些字段：给出 **整段替换稿** 或 **待填空白**，并写清用户要在后台核对什么。

## 看图时必抓的冲突

- 尺寸标注 vs 属性栏 vs A+
- 杯数 vs 克数 vs 五点
- dB 数字 vs 五点
- 可拆碗 vs 一体碗 vs 对比表勾选
- GIVE AWAY / Gift 字样
- 变体图顺序是否与英雄色相同（常见：White 把尺寸图放在第 2 张）

## 变体不要偷懒

只审用户给的那一个 ASIN 不够。至少打开父体下每个颜色/尺码的标题、属性、五点、图片槽位。橙/银/白经常还停在旧文案。
