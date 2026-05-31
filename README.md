# 📊 AI Trading Signals — 中国AI交易信号

**每日 A 股市场情报，AI 驱动。新浪财经数据。Pi 24/7 自动生成。**

> *"AI交易大赛结果出炉：只有中国AI赚钱，跟GPT-5反着买" — 36kr*

## 工作原理

```
新浪财经 API (免费实时数据)
    ↓
Python 采集引擎 (5大指数 + 8大板块 + 9只重点个股)
    ↓
AI 分析引擎 (市场情绪 + 板块轮动 + 动量信号)
    ↓
每日报告 (Markdown + JSON)
    ↓
订阅分发 ($29-99/月)
```

## 覆盖范围

### 📈 5 大指数
上证指数 · 深证成指 · 创业板指 · 科创50 · 沪深300

### 🔥 8 大热门板块
AI人工智能 · 半导体 · 新能源 · 医药 · 消费电子 · 机器人 · 科创50 · 沪深300

### ⚡ 9 只重点个股
贵州茅台 · 宁德时代 · 比亚迪 · 中芯国际 · 寒武纪 · 海光信息 · 科大讯飞 · 浪潮信息 · 中科曙光

## 今日信号示例

```
📊 情绪: Bearish 🔴
📈 上证 4068.57 (-0.73%) | 深证 15575.13 (-1.81%)
🔥 最强: 医药 (+2.38%)
❄️ 最弱: 半导体 (-5.84%)
📊 轮动: 资金从半导体流向医药

🎯 信号:
  [观望] ★★★ 现金/逆回购 — 市场普跌，建议观望
  [轮动] ★★ 沪深300 — 关注次强板块轮动
```

## 定价

| 版本 | 内容 | 价格 |
|------|------|------|
| 🆓 免费版 | 每日市场概览 + 1个信号 | FREE |
| ⭐ Pro版 | 全信号 + 板块轮动 + 个股推荐 | [$29/月](https://paypal.me/ulnit/29) |
| 🚀 VIP版 | Pro + 实时预警 + 1对1咨询 | [$99/月](https://paypal.me/ulnit/99) |

## 技术栈 (零成本运营)

- **数据**: 新浪财经 JS API (免费, 无需 API Key)
- **引擎**: Python 标准库 only
- **分发**: GitHub Pages + Markdown
- **支付**: PayPal.me
- **硬件**: Raspberry Pi ($35)

## 市场验证

- 36kr 头条：「只有中国AI赚钱」
- API 转售市场营收暴涨 1134%
- WAIC 2025 热点：「怎么用 AI 赚钱」

## 快速开始

```bash
git clone https://github.com/ulnit/ai-trading-signals
cd ai-trading-signals
python3 src/engine.py

# 输出: reports/report_YYYYMMDD.md + reports/report_YYYYMMDD.json
```

## 订阅

👉 [Pro $29/月](https://paypal.me/ulnit/29)  
👉 [VIP $99/月](https://paypal.me/ulnit/99)

---

> ⚠️ 免责声明: AI交易信号仅供研究参考，不构成投资建议。投资有风险，入市需谨慎。
>
> *Powered by AI · Running on Raspberry Pi · 24/7 Automated*