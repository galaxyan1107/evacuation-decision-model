# 第43天更新 — 2026年4月11日

> 🌐 [English](../../updates/day43-april11.md) | **中文**

**状态：亚稳态** | **突破：2/5** | **λ中位数 = 0.463**

---

## 新数据

| 指标 | 第42天 | 第43天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 0 | **0** | **536** |
| 弹道导弹拦截 | 0 | 0 | 506 |
| 无人机探测 | 0 | ~0 | ~2362 |
| 无人机拦截 | 0 | 0 | ~2172 |
| 巡航导弹 | 0 | 0 | 19 |
| 弹道导弹拦截率（累计） | — | — | 94.4% |
| 无人机库存剩余 | — | — | -18.1%（-362/2000） |

**关键事件：**
- Ceasefire Day 3: Third consecutive zero-attack day; no BMs, drones, or cruise missiles detected by @modgovae
- HISTORIC ISLAMABAD TALKS BEGIN: First direct US-Iran talks since 1979 Islamic Revolution. VP JD Vance + Steve Witkoff + Jared Kushner lead US delegation; FM Abbas Araghchi + Speaker Mohammad Bagher Ghalibaf lead Iranian delegation of 70+. Talks began after 5-hour delay (CNN, Al Jazeera, ABC News, Washington Times)
- PROGRESS SIGNALS: Sources report 'some progress on basic conditions including Lebanon ceasefire'; reports of potential 'movement on unfreezing of Iranian assets' (Al Jazeera live blog, Times of Israel)
- IRAN RED LINES: Iran state TV outlines red lines — control of Strait of Hormuz, Lebanon truce included in ceasefire, no US military presence in region (Times of Israel)
- US NAVY CROSSES HORMUZ: US warships cross Strait of Hormuz for first time since war began — east-to-west transit into Gulf and back (Bloomberg, Axios). Iran calls it a 'ceasefire violation' and threatens response. Aimed at building confidence for commercial shipping
- HORMUZ STILL BOTTLENECKED: ~10 vessels transited Saturday (up from 7 Thu); Iran still restricting passage, charging $1M+ tolls; 600+ vessels still stranded including 300+ tankers (NBC News, Al Jazeera)
- EASA EXTENDS AIRSPACE BAN: EASA extended Conflict Zone Information Bulletin (CZIB 2026-03-R6) to April 24 — European carriers (BA, Lufthansa, Air France, KLM) remain grounded on Gulf routes; next review April 24 (Wego, TravelPirates)
- DXB ~78% capacity: Emirates + flydubai operating 220+ daily flights; recovery continues but EASA extension blocks European carriers; Emirates at ~70% of pre-conflict capacity (IBTimes, Time Out Dubai)
- OIL SOFTENS ON TALKS OPTIMISM: WTI ~$95.50 (down from $98.70 Day 42); Brent ~$96.66; markets pricing increased probability of lasting ceasefire as talks begin (Trading Economics, Fortune)
- Polymarket: ceasefire extension to Apr 21 at ~78% (up from 75% Day 42); permanent peace deal by Jun-30 at ~42%; conflict ends by Dec-31 at ~94%
- Cumulative (official): 537 BMs, 26 cruise missiles, 2,256 drones; ~13 dead, ~230 injured (unchanged — third consecutive zero-casualty day)
- Trump warns of 'reset' if talks fail; Iran's Ghalibaf: 'We are here to find peace but not at any cost' (News24Online, The Week India)

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.236
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.000
  + λ_代理人          = +0.000
  + λ_武器           = +0.000
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.240
  ────────────────────────────
  λ 中位数       = 0.463（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **0.463** |
| λ 第95百分位 | **1.010** |
| P(λ > 1.0) | **5.1%** |
| P(λ > 1.5) | **2.0%** |
| P(λ > 2.0) | **0.3%** |
| 判定 | **亚稳态** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day43.png)

![Lambda演变](../../charts/lambda_evolution_day43.png)

---

## 建议

**监测。** 系统在正常参数范围内。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-04-11 23:06 |
