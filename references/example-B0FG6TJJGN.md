# 判定校准案例（厨房小家电，非通用规则）

只在两种情况阅读：

1. 需要看「思考在代码块外、块内纯粘贴」的完整写法
2. 当前商品是厨房小家电，且出现尺寸图 vs 属性栏、图文两套营销数、秒杀 V 型这类同类问题

案例 ASIN `B0FG6TJJGN` 只用来校正判定，不是模板。里面的 70g、碗数、burr、Super Silent、四色磨豆机，**禁止**套到服装、3C、个护、食品等其他品类。输出时仍要：思考在代码块外，块前标题只用字段名。

## 第 1 项：不要信看起来更整的属性

| 位置 | 数字 |
|---|---|
| 属性栏 / A+ 规格 | 5"L x 10"W x 5"H 或 5"L x 5"W x 10"H |
| 主图尺寸标注 | **6.77 in 高 × 4.7 in 宽** |

正确动作：以尺寸图 / 卡尺为准，统一 `4.7"L x 4.7"W x 6.77"H`。`5x10x5` 是把高度填进了宽度。筛选器读属性，A+ 读规格，两套数会同时伤害转化和精筛。

同时出现的脏字段：Style=`NICE`；Black 材质只写 Stainless Steel，Orange 才写了 ABS+Stainless Steel（壳体其实是塑料）。配件后台写 `1 BOWL`，但 FAQ/对比表是一体不可拆碗。

**思考：** 统一成主图可测量尺寸，并填对 Material / Included Components，让全部颜色都能进同一组筛选，减少 INAD。

```
item_dimensions: 4.7"L x 4.7"W x 6.77"H
material: ABS, Stainless Steel
style: Compact
included_components: Coffee Grinder, Cleaning Brush, User Manual
```

不要在块内写“以主图为准”。Warranty 不要出现在这张属性表的营销字段里；若用户有保修，思考区让他去 Warranty 专用字段填。

## 第 2 项：主题对，文案裂开

主题 Color 是对的，不要拆组。Black/Orange 已是新标题，Silver/White 仍是旧 Super Silent 标题；Orange 五点还在写 sleek black design。

英雄 Black 标题如果已经合规且小类排名稳定：**不要输出 Black 标题代码块**，思考区写“不动”。

若英雄标题本身含 Super Silent / warranty / 超长且已被截断，则必须重写成 ≤75 字符，并给 Item highlights。排名好也不能留违规词。

## 第 4 项：变体图序不同 + A+ 也要 ALT

Black 第 2 张是安全锁，White 第 2 张是尺寸图。图库 ALT 必须按槽位实图写。

A+ 每张规格图、对比表、场景图都要编号输出：

### A+ ALT（父体共用）

**思考：** A+ 图已在页面上，空 ALT 等于放弃图片检索；按模块顺序描述可见内容，不复述夸大词。

```
A+1: SHARDOR electric coffee grinder size diagram showing 6.77 inch height and 4.7 inch width on white background
A+2: SHARDOR coffee grinder 70 gram capacity graphic with whole beans beside the bowl
```

不要只给 MAIN / 特征图。不要在 ALT 句尾加 `in our listing graphic` 或“改图后改成 63 dB”。

## 第 6 项：图文两套营销数

- 五点 12 cups vs 倒粉图 3 cups → 删 12 cups，跟 70g 和 3 servings
- 五点 63 dB vs 噪音图 60 dB → 无第三方报告时用更保守的 63，并改图
- 倒粉图 GIVE AWAY → 标配配件改 Included 或去掉

换图任务写在思考区。五点代码块里直接写保守口径，不要夹注“改图后”。

## 第 7 项：秒杀不是改价

若 Keepa 近 30 天 Amazon 价在 $24.99 与 $26.99 之间出现 V 型，但 List Price 一直是 $26.99，或跌价窗口带 Lightning Deal / coupon 标记：判 **通过**，不是频繁改价。

只有 List Price 自己台阶式来回跳且停留超过 7 天，才计次。看不清图层则 `DATA_MISSING`。本单当时若只是促销锯齿，不要写“锁一个基础价、停秒杀、改用 coupon”。

## 第 9 项：warranty 不能进五点

错误五点：`2-YEAR MANUFACTURER'S WARRANTY` 或 `Satisfaction guaranteed`。

Seller Central 五点禁止 Guarantee information；标题禁止 100% quality guaranteed；图片禁止 warranty 徽章。保修只进 Warranty 字段。

正确：五点写容量、安全锁、一体碗、适用场景、箱内配件。思考区说明“保修从 PDP 拿走是为了不被抑制；腾出的位置用来写可筛选、可验证的事实，对自然权重更有用”。

## 第 5 / 8 / 10 项

ST 前台看不到就整段替换，补标题没有的同义词，禁止写实物没有的机制（本例刀片机禁止 burr）。代码块只有小写词，字节数写思考区。

White 若用了 Black 机身生活方式图 → 第 8 项不通过，换图说明写思考区。

旧标题 Super Silent、quieter than、刀片机写 burr → 第 9 项不通过；违规子体标题代码块直接给干净标题，需要时附 Item highlights。

A+ 对比表若勾了可拆碗、FAQ 却写一体碗 → 第 10 项不通过；代码块给修正后的单元格和 FAQ 答句。

## 其他品类怎么迁移这个案例（不要抄数字）

- **服装：** 第 1 项看尺码表 vs 产品细节 vs 图上标注，不要看“看起来更整的 S/M/L”。第 8 项看 Size 图是否用了另一码衣服。
- **3C：** 第 6 项看兼容型号/电压/电流是否和图、A+、五点同一套。第 10 项看 FAQ 有没有把单一配件写成全系标配。
- **个护/保健：** 第 9 项优先打疾病声称、FDA、抗菌/有机，而不是噪音词。
