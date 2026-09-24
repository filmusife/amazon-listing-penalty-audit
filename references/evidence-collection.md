# 证据怎么收

缺数据就标 `DATA_MISSING`。不要用猜测填重量、功率、实验室指标、后台节点列表、后台 ST。

分两档。没有 Keepa/后台时，用 `frontend-min` 把能判死的项判完，不要假装审了 Search Terms 或调价日志。

## 第 0 步：官方规则 + 品类

打开 [amazon-policy.md](amazon-policy.md) 列出的 Seller Central 页面。把现行条款记进报告的政策闸门。拉失败：用快照继续，并标 `POLICY_FETCH_FAILED`。

根据叶子类目和主图，只读 [category-overlays.md](category-overlays.md) 匹配的一节。

## frontend-min（必须做完）

对用户给的 ASIN 和它的 **全部子 ASIN**：

1. 标题、五点、可见属性、面包屑、BSR、型号、评分
2. `dimensionToAsinMap` / `variationValues` / parentAsin / 变体主题
3. 每张主图/图库 hiRes：下载后看图，不要只读文件名
4. **全部 A+ 模块图**（对比表、规格图、场景图、图标）：下载后看图
5. A+ 规格、FAQ、对比表数字、笔误、品牌视频是否绑死单一子体
6. 图上出现的数字和徽章：尺寸/尺码、容量、功率、认证、warranty / guarantee
7. 各子体图库是否串色/串码、规格图是否挂错子体
8. 标题/五点/A+/ALT 里的夸大词、比较词、品类错词、warranty、促销语
9. 标题字符数（美国站含空格是否超过 75）

前台包足够打：#1 #2 #4 #6 #8 #9 #10，以及 #3 的主路径、#5 的前台污染。

## backend-full（有则做，没有就标缺失）

1. Search Terms 原文
2. 后台 Browse node 完整列表
3. Package dimensions / 真实重量
4. Keepa 或 Seller Central 调价日志（必须区分 List Price / Buy Box / Lightning Deal / coupon）
5. 实验室噪音、铭牌功率、检测报告
6. Warranty 文档字段是否已填

这些字段读不到时：给出 **整段替换稿** 或 **待填空白**，思考区写清用户要在后台核对什么。不要把前台没看到的 ST 判成“已通过”。

## 数据源优先级

1. 卖家精灵 / Sorftime / Keepa 等已配置 MCP（若当前环境可用）
2. Amazon 前台 HTML + 实图
3. 用户提供的后台截图、实测、退货报告

不要为了第 4 项去抓 `amazon.com/product-reviews/` 全站评论。只有当图文数字冲突需要旁证时，才看详情页已有的 Customers say / 可见差评标题。

## Keepa 第 7 项怎么读

同时打开这些图层，不要只看一条 Amazon 价：

- List Price（卖家标价）
- Amazon / Buy Box
- Marketplace New
- Lightning Deal / 7-day deal / Best Deal 标记
- Coupon 标记

促销：List Price 不动而 Buy Box 下跌；或下跌后 1–7 天回到原位的 V 型；或带秒杀/券标记。这些 **不计** 改价次数。

真实改价：List Price 台阶式移动并在新价停留 >7 天；或无促销标记时 Amazon 价与 List Price 同步换平台。

看不清 List Price 和 Lightning 标记时标 `DATA_MISSING`，不要用 Buy Box 锯齿直接判不通过。

## 看图时必抓的冲突

- 尺寸/尺码标注 vs 属性栏 vs A+
- 容量/件数/功率/成分 vs 五点
- 配件图 vs Included Components
- GIVE AWAY / Gift 字样
- warranty / guarantee / certified / prime 徽章
- 变体图顺序是否与英雄子体相同（不要假设相同）
- 子体图库是否用了另一变体的实物
- A+ 每一张图的画面（给 ALT 用，不只是核对数字）

具体盯哪些单位，读当前品类 overlay。

## 变体不要偷懒

只审用户给的那一个 ASIN 不够。至少打开父体下每个颜色/尺码/口味的标题、属性、五点、图片槽位、A+。非英雄子体经常还停在旧文案。

提取标题/五点/ALT/ST 后，用 [../scripts/scan_listing.py](../scripts/scan_listing.py) 做确定性扫描，再写第 4/5/9 项结论。
