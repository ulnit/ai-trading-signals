#!/usr/bin/env python3
"""AI Trading Signals — Chinese market intelligence. Sina Finance data. Pi-powered."""
import re, json, time, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

WORK_DIR = Path(__file__).parent.parent
REPORTS_DIR = WORK_DIR / "reports"
SINA = "https://hq.sinajs.cn/list="

INDICES = {"上证指数":"sh000001","深证成指":"sz399001","创业板指":"sz399006","科创50":"sh000688","沪深300":"sh000300"}
STOCKS = {"贵州茅台":"sh600519","宁德时代":"sz300750","比亚迪":"sz002594","中芯国际":"sh688981","寒武纪":"sh688256","海光信息":"sh688041","科大讯飞":"sz002230","浪潮信息":"sz000977","中科曙光":"sh603019"}
SECTORS = {"AI人工智能":"sh512930","半导体":"sh512480","新能源":"sh516160","医药":"sh512010","消费电子":"sh159732","机器人":"sh562500","科创50":"sh588000","沪深300":"sh510300"}

def fetch(codes):
    url = SINA + ",".join(codes)
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://finance.sina.com.cn"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.read().decode("gbk", errors="ignore")
    except:
        return ""

def parse(line):
    m = re.search(r'"([^"]*)"', line)
    if not m: return None
    v = m.group(1).split(",")
    if len(v) < 4: return None
    return {"name":v[0].strip(),"open":float(v[1] or 0),"prev":float(v[2] or 0),"price":float(v[3] or 0),"high":float(v[4] or 0) if len(v)>4 else 0,"low":float(v[5] or 0) if len(v)>5 else 0}

def get_data(code_map):
    raw = fetch(list(code_map.values()))
    result = []
    for line in raw.split("\n"):
        if "hq_str" not in line: continue
        p = parse(line)
        if not p or p["price"] == 0: continue
        cm = re.search(r'hq_str_(\w+)', line)
        code = cm.group(1) if cm else ""
        name = next((k for k,v in code_map.items() if v==code), p["name"])
        chg = ((p["price"]-p["prev"])/p["prev"]*100) if p["prev"] else 0
        result.append({"name":name,"code":code,"price":p["price"],"change_pct":round(chg,2),"open":p["open"],"high":p["high"],"low":p["low"]})
    return result

def analyze():
    indices = get_data(INDICES)
    sectors = sorted(get_data(SECTORS), key=lambda x: x["change_pct"], reverse=True)
    stocks = sorted(get_data(STOCKS), key=lambda x: x["change_pct"], reverse=True)
    
    up = sum(1 for i in indices if i["change_pct"]>0)
    sentiment = "Bullish 🟢" if up>=4 else "Bearish 🔴" if up<=1 else "Neutral 🟡"
    
    insights = []
    sh = next((i for i in indices if "上证" in i["name"]), None)
    if sh: insights.append(f"上证 {sh['price']:.2f} ({sh['change_pct']:+.2f}%)")
    sz = next((i for i in indices if "深证" in i["name"]), None)
    if sz: insights.append(f"深证 {sz['price']:.2f} ({sz['change_pct']:+.2f}%)")
    
    if sectors:
        insights.append(f"🔥 最强: {sectors[0]['name']} ({sectors[0]['change_pct']:+.2f}%)")
        insights.append(f"❄️ 最弱: {sectors[-1]['name']} ({sectors[-1]['change_pct']:+.2f}%)")
        if sectors[0]['change_pct'] > 0 and sectors[-1]['change_pct'] < 0:
            insights.append(f"📊 轮动: 资金从{sectors[-1]['name']}流向{sectors[0]['name']}")
    
    up_stocks = [s for s in stocks if s["change_pct"]>0]
    down_stocks = [s for s in stocks if s["change_pct"]<0]
    if up_stocks: insights.append(f"⚡ 领涨: {up_stocks[0]['name']} {up_stocks[0]['change_pct']:+.2f}%")
    if down_stocks: insights.append(f"📉 领跌: {down_stocks[-1]['name']} {down_stocks[-1]['change_pct']:+.2f}%")
    
    signals = []
    if sentiment == "Bullish 🟢" and sectors:
        signals.append({"type":"买入","level":"★★★","target":sectors[0]['name'],"reason":f"市场向好，{sectors[0]['name']}板块领涨","confidence":75})
    elif sentiment == "Bearish 🔴":
        signals.append({"type":"观望","level":"★★★","target":"现金/逆回购","reason":"市场普跌，建议观望","confidence":80})
    else:
        signals.append({"type":"持有","level":"★★","target":"沪深300","reason":"市场震荡，控制仓位","confidence":60})
    
    if len(sectors) >= 3:
        signals.append({"type":"轮动","level":"★★","target":sectors[1]['name'],"reason":"关注次强板块轮动","confidence":55})
    
    signals.append({"type":"⚠️ 风险提示","level":"★","target":"投资有风险","reason":"AI信号仅供参考，不构成投资建议","confidence":100})
    
    return {"timestamp":datetime.now().isoformat(),"sentiment":sentiment,"indices":indices,"sectors":sectors[:8],"stocks":stocks[:10],"insights":insights,"signals":signals}

def md_report(r):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = f"""# 📊 AI 交易信号日报

**{now}** | 情绪: {r['sentiment']} | 数据: 新浪财经

---

## 📈 主要指数

| 指数 | 点位 | 涨跌幅 |
|------|------|--------|
"""
    for i in r["indices"]:
        md += f"| {i['name']} | {i['price']:.2f} | {i['change_pct']:+.2f}% |\n"
    
    md += "\n## 🔥 板块热度\n\n| 板块 | 涨跌幅 | 强度 |\n|------|--------|------|\n"
    for s in r["sectors"]:
        bar = "█" * min(int(abs(s['change_pct'])*3), 15)
        md += f"| {s['name']} | {s['change_pct']:+.2f}% | {bar} |\n"
    
    md += "\n## ⚡ 重点个股\n\n| 股票 | 现价 | 涨跌幅 |\n|------|------|--------|\n"
    for s in r["stocks"]:
        md += f"| {s['name']} | {s['price']:.2f} | {s['change_pct']:+.2f}% |\n"
    
    md += "\n## 🤖 AI 分析\n\n"
    for ins in r["insights"]:
        md += f"- {ins}\n"
    
    md += "\n## 🎯 信号\n\n| 类型 | 等级 | 标的 | 理由 | 置信度 |\n|------|------|------|------|--------|\n"
    for sig in r["signals"]:
        md += f"| {sig['type']} | {sig['level']} | {sig['target']} | {sig['reason']} | {sig['confidence']}% |\n"
    
    md += f"""

---

## 📌 订阅

| 版本 | 价格 |
|------|------|
| 🆓 免费版 | FREE |
| ⭐ Pro | [$29/月](https://paypal.me/ulnit/29) |
| 🚀 VIP | [$99/月](https://paypal.me/ulnit/99) |

> ⚠️ 免责声明: AI信号仅供研究参考，不构成投资建议。投资有风险，入市需谨慎。
>
> *Powered by AI Trading Signals — Pi 24/7*
"""
    return md

if __name__ == "__main__":
    print("🤖 AI Trading Signals")
    print("=" * 50)
    print("📡 采集数据...")
    report = analyze()
    
    n_idx = len(report["indices"])
    n_sec = len(report["sectors"])
    n_stk = len(report["stocks"])
    print(f"✅ 指数:{n_idx} 板块:{n_sec} 个股:{n_stk}")
    print(f"📊 情绪: {report['sentiment']}")
    for ins in report["insights"][:6]:
        print(f"  • {ins}")
    
    md = md_report(report)
    ds = datetime.now().strftime("%Y%m%d")
    json_path = REPORTS_DIR / f"report_{ds}.json"
    md_path = REPORTS_DIR / f"report_{ds}.md"
    
    with open(json_path, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    with open(md_path, "w") as f:
        f.write(md)
    
    print(f"\n💾 {json_path}")
    print(f"💾 {md_path}")
    print(f"\n🎯 信号: {len(report['signals'])}个")
    for sig in report["signals"][:2]:
        print(f"  [{sig['type']}] {sig['target']} — {sig['reason'][:40]}")
