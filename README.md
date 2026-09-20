# Amazon Listing 7项隐性减分体检

Codex skill：按 7 个静默减分项体检亚马逊 Listing（默认美国站），并输出可粘贴到 Seller Central 的字段 / 标题 / 五点 / ALT / Search Terms 改法。

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
Use $amazon-listing-penalty-audit 检查美国站 ASIN B0XXXXXXX 的 7 项隐性减分，覆盖全部变体，给可粘贴改法。
```

## 7 项

1. 尺寸 / 重量 / 属性多处不一致
2. 变体主题与真实差异错配
3. Browse node 多选或错选
4. 图片 ALT 空白或中文
5. Search Terms 埋竞品品牌或 ASIN
6. 描述 / 图片数字与实物不符
7. 30 天改价超过 5 次

完整判定标准和报告结构在 `SKILL.md` 与 `references/`。
