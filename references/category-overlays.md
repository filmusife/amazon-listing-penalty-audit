# 品类 overlay

只读与当前商品匹配的 **一节**。匹配不上就用 `generic`。禁止把本节例子里的单位、机制词、禁词当成全球真理。

用法：第 1/6/8/9/10 项遇到“哪些数字必须一致、哪些词不能乱写”时来这里。通用判定仍以 seven-items / extra-items / amazon-policy 为准。

## generic

- 必须一致：可见尺寸、重量（若已宣称）、件数、材质/成分、箱内配件
- 变体陷阱：图库串色/串码；信息图把单一规格写成全系
- 宣称陷阱：best / #1 / warranty / 无证据 100% / 未证实认证
- ST 陷阱：竞品品牌、ASIN、标题已有词、本品没有的品类词

## kitchen-small-appliances

匹配：磨豆机、搅拌机、空气炸锅、电热水壶、厨师机、早餐机等厨房小电器。

- 必须一致：容量（g / ml / cup 只能留一套口径）、功率 W、电压、外形尺寸、噪音 dB（若宣称）、碗/壶是否可拆
- 变体陷阱：颜色生活方式图混用；杯数/碗数图挂错子体
- 宣称陷阱：dishwasher safe、commercial、ultra quiet、wet grinding；刀片机写 burr / conical / espresso-grade
- ST 陷阱：补同义词（mill / chopper）可以，不能补实物没有的研磨机制

## apparel-shoes

匹配：服装、鞋靴、内衣、配饰穿戴。

- 必须一致：尺码名 vs 尺码表 vs 产品细节 vs 图上标注；成分百分比；产地（若宣称）
- 变体陷阱：Size 主题却用错码服装图；尺码表图数字属于另一件；颜色名和实图色差且未说明
- 宣称陷阱：slimming / medical compression / 治疗功效；UPF、organic 无检测；虚高弹性或“显瘦几厘米”
- ST 陷阱：竞品服装品牌、已在标题的 size/color 词；不要把鞋的机制词写进服装 ST

## beauty-personal-care

匹配：护肤、彩妆、身体护理、口腔护理（非药品）。

- 必须一致：净含量、成分（INCI 若已写）、使用对象、是否香精/防晒值
- 变体陷阱：香型/色号图挂错；成分图把单一配方写成全系
- 宣称陷阱：treat / cure / heal、药妆、FDA approved（通常不成立）、hypoallergenic / organic / anti-bacterial 无依据
- ST 陷阱：药品名、竞品品牌、病症词

## supplements-grocery

匹配：膳食补充剂、维生素、包装食品、咖啡豆/茶叶（食品本身）。

- 必须一致：净重、份数、营养表、过敏原、口味变体
- 变体陷阱：口味图串味；营养表挂到另一口味
- 宣称陷阱：疾病声称、FDA 未评估语句缺失、减肥保证、无依据 organic / non-GMO
- ST 陷阱：药品名、病症、竞品品牌；咖啡豆不要写成 espresso machine 配件除非真是

## consumer-electronics

匹配：耳机、充电器、线材、摄像头、智能配件、小 3C。

- 必须一致：兼容型号、接口、电压/电流、电池容量、无线协议、外形尺寸
- 变体陷阱：兼容清单图挂错型号；颜色图混用；配件包内容与 Included Components 不符
- 宣称陷阱：无线距离虚标、防水等级无测试、MFi/Qi 无授权、fast charge 与实测电流不符
- ST 陷阱：竞品型号词（除非确是兼容描述且政策允许的通用型号，不要写品牌名）

## home-furniture

匹配：家具、收纳、床品、灯具、家居软装。

- 必须一致：长宽高、承重、材质、组装件数、床品尺寸名（Twin/Queen）vs 实测
- 变体陷阱：尺寸款用了另一尺寸的场景图；沙发色号串色
- 宣称陷阱：承重虚标、防水/防火无依据、实木 vs 贴面写错
- ST 陷阱：竞品家具品牌、已在标题的尺寸名

## toys-baby

匹配：玩具、婴幼儿用品、安全座椅配件（非医疗）。

- 必须一致：适用年龄、尺寸、材质、安全认证（若宣称）
- 变体陷阱：年龄款包装图挂错；配件件数与当前 SKU 不符
- 宣称陷阱：ASTM/CPSC 未证实、牙齿矫正/医疗、choking 相关保证语、无依据 organic
- ST 陷阱：竞品玩具品牌、医疗词、超龄/欠龄关键词

## sports-outdoors

匹配：健身器材、瑜伽用品、户外装备、骑行配件。

- 必须一致：承重、尺寸、材质、适用场景、件数
- 变体陷阱：阻力级别/尺寸图挂错；颜色垫面图混用
- 宣称陷阱：减肥保证、专业训练效果、防水等级无测试
- ST 陷阱：竞品运动品牌、医疗康复词（除非有依据且政策允许）

## automotive-parts-accessories

匹配：汽车配件、绞盘绳/拖车绳、车载应急装备、车灯、脚垫、改装外饰。

- 必须一致：适配车型年份与底盘（Vehicle Fitment / Amazon PartFinder 口径）、破断强力与安全工作负荷（MBS vs WLL 必须清晰区分，严禁混淆）、线径/长度、材质（如 UHMWPE 超高分子量聚乙烯 / 锻造合金钢）、电压与流明（车灯）
- 变体陷阱：不同承重级别或线径用了同一张破断强力示意图；适用车型清单图挂错子体
- 宣称陷阱：未获第三方检测报告宣称 DOT / SAE / CE 认证；indestructible / unbreakable 等绝对化不坏承诺；直接把 OEM 品牌写成主语（如 "Jeep Winch" 侵权，必须写 "Winch Rope Compatible with Jeep"）
- ST 陷阱：竞品汽配品牌名、裸写 OEM 汽车品牌名（如 ford jeep 直接塞入 ST）、与本品无关的车型发动机代号

## pet-supplies

匹配：宠物用品、智能喂食器、牵引绳、宠物窝垫、玩具、梳理洗护。

- 必须一致：适用犬种体型与体重区间（Pet Weight / Sizing Guide）、喂食容量（L / Cups / g）、材质（食品级不锈钢 / BPA-Free 塑料 / 耐磨牛津布）、清洗保养方式
- 变体陷阱：不同尺码子体共用一张未标具体尺寸的场景图；颜色款实图与色名串色
- 宣称陷阱：indestructible / 100% chew-proof（极度容易因买家大狗咬坏触发 INAD 退货与差评）；flea & tick repellent / 杀跳蚤杀虫（未经 EPA 登记直接触发杀菌农药停售）；cure anxiety / heal skin（医疗治愈疾病声称触发 FDA 违规）；vet recommended（无兽医权威背书证据）
- ST 陷阱：处方兽药名、竞品宠物品牌、EPA 违规杀虫词

如何选择：看叶子类目和主图，不看卖家自称。一件“瑜伽垫”不要因为 A+ 写了 kitchen 就去读 kitchen 节。
