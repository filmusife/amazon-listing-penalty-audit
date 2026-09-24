# Amazon Listing 隐性减分体检

Codex skill：以最新 Seller Central 规则为底线，按 7 个静默减分项加 3 个扩展项体检亚马逊 Listing。默认美国站，**全品类通用**。品类差异用 overlay，不套某个历史 ASIN。区分秒杀/优惠券与 list price 改价。纠偏之后按 COSMO 关系与 Rufus/Alexa for Shopping 可引用事实优化发现权重，而不是堆 A9 关键词。

输出标题、Item highlights、五点、属性、图库 ALT、A+ ALT、Search Terms。代码块内只有能进后台的原文；块前标题只用字段名，不写“可复制”。每条改法在块外用思考说明官方依据，以及服务政策 / COSMO / Rufus 哪一层。

不是从零写新 Listing，也不是选品或评论分析。

## 安装

把本仓库放到 Codex skills 目录：

```bash
git clone https://github.com/filmusife/amazon-listing-penalty-audit.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/amazon-listing-penalty-audit"
```

已存在同名目录时，用本仓库内容覆盖该 skill 文件夹即可。重启或新开 Codex 会话后生效。

## 调用

在 Codex 里给 ASIN，并提到以下任一触发即可：

- `$amazon-listing-penalty-audit`
- `/listing-audit`
- `/penalty-audit`
- 隐性减分 / 静默降权体检

示例：

```text
Use $amazon-listing-penalty-audit 检查美国站 ASIN B0XXXXXXX 的隐性减分，覆盖全部变体。
```

## 体检项

1. 尺寸 / 重量 / 属性多处不一致
2. 变体主题与真实差异错配
3. Browse node 多选或错选
4. 图片 ALT 空白、错语言或空泛（含全部 A+ 图）
5. Search Terms 埋竞品品牌或 ASIN
6. 描述 / 图片数字与实物不符
7. 30 天 list price 改价超过 5 次（秒杀/券造成的 V 型不计）
8. 跨变体图片串色 / 规格图错配
9. 夸大词 / 比较词 / 政策违禁词（含 warranty/guarantee）
10. A+ 对比表 / FAQ / 视频与当前子体不一致

完整判定标准和报告结构在 `SKILL.md` 与 `references/`。政策底线见 `references/amazon-policy.md`。品类差异见 `references/category-overlays.md`。确定性扫描用 `scripts/scan_listing.py`。
