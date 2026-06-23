# Douyin & ByteDance CN Shadowrocket Rules

适用于中国区字节跳动服务的分流规则，覆盖：

- 抖音、抖音火山版、抖音支付、汽水音乐
- 即梦 AI（`jimeng.jianying.com`）
- 豆包、扣子 Coze 中国区
- 火山引擎、火山云及相关 CDN/API
- 飞书中国区、飞书文档、飞书会议和开放平台
- 字节跳动中国区共享登录、图片、视频、对象存储和网络基础设施

规则基于
[`v2fly/domain-list-community`](https://github.com/v2fly/domain-list-community)
的 `bytedance`、`douyin`、`doubao`、`volcengine`、`feishu` 分类生成，并每周自动更新。

## Shadowrocket

将规则放在 `GEOIP` 和 `FINAL` 前：

```ini
RULE-SET,https://raw.githubusercontent.com/DDcat2025/douyin-bytedance-shadowrocket-rules/main/rule/Shadowrocket/ByteDanceCN/ByteDanceCN.list,DIRECT
```

也可以使用 Domain Set：

```ini
DOMAIN-SET,https://raw.githubusercontent.com/DDcat2025/douyin-bytedance-shadowrocket-rules/main/rule/Shadowrocket/ByteDanceCN/ByteDanceCN_Domain.list,DIRECT
```

二者选择一个即可，不要重复引用。如果你的网络需要代理访问这些服务，将 `DIRECT`
替换为相应策略组名称。

## Mihomo / Clash Meta

```yaml
rule-providers:
  bytedance-cn:
    type: http
    behavior: classical
    url: https://raw.githubusercontent.com/DDcat2025/douyin-bytedance-shadowrocket-rules/main/rule/Mihomo/ByteDanceCN/ByteDanceCN.yaml
    path: ./ruleset/bytedance-cn.yaml
    interval: 86400

rules:
  - RULE-SET,bytedance-cn,DIRECT
```

## 文件

- `ByteDanceCN.list`：Shadowrocket `RULE-SET` 格式。
- `ByteDanceCN_Domain.list`：Shadowrocket `DOMAIN-SET` 格式。
- `ByteDanceCN.yaml`：Mihomo classical rule-provider 格式。
- `data/bytedance-cn-domains.txt`：每行一个域名的纯文本列表。

## 范围说明

本规则包含飞书中国区，但没有合并 TikTok、Lark Global 和 Trae 海外分类，因为
这些服务的线路策略可能与中国区抖音不同。即梦 AI 使用的剪映、字节 CDN 和静态
资源域名已包含。
