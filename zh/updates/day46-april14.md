# 第46天更新 — 2026年4月14日

> 🌐 [English](../../updates/day46-april14.md) | **中文**

**状态：不稳定** | **突破：2/5** | **λ中位数 = 1.101**

---

## 新数据

| 指标 | 第45天 | 第46天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 0 | **0** | **536** |
| 弹道导弹拦截 | 0 | 0 | 506 |
| 无人机探测 | 0 | ~0 | ~2362 |
| 无人机拦截 | 0 | 0 | ~2172 |
| 巡航导弹 | 0 | 0 | 19 |
| 弹道导弹拦截率（累计） | — | — | 94.4% |
| 无人机库存剩余 | — | — | -18.1%（-362/2000） |

**关键事件：**
- Ceasefire Day 6: Sixth consecutive zero-attack day; no BMs, drones, or cruise missiles — ceasefire holds despite US naval blockade of Iranian ports
- US BLOCKADE DAY 2: Naval blockade of Iranian ports continues; 14 total ships have transited Hormuz since blockade began (~11 today vs ~3 Monday). US allows non-Iranian port traffic through strait
- SECOND ROUND TALKS DISCUSSED: Pakistan working to set up second round of US-Iran peace talks in Islamabad after first round (21-hour marathon Apr 11-12) collapsed. Both sides reportedly open to resuming negotiations
- Iran considering pausing Hormuz shipping to avoid testing US blockade and derailing potential talks (Bloomberg). Shows restraint despite rhetoric
- CHINA CONDEMNS BLOCKADE: Beijing calls US naval blockade of Hormuz "dangerous and irresponsible act" that will further inflame tensions (CNBC)
- Sanctioned tankers testing blockade: US-sanctioned tanker attempts Hormuz transit, testing enforcement resolve (Bloomberg)
- OIL DROPS ~6%: WTI falls to ~7/bbl (from 03 Monday), Brent ~7.89 — both drop ~5-6% as markets price in potential second round of talks. Biggest single-day drop since ceasefire began
- DXB ~80% capacity: Emirates operating ~145-150 departures/day to ~125 destinations (~70% of normal). EASA conflict zone bulletin extended to Apr 24. Foreign carrier one-rotation cap starts Apr 20
- Polymarket: Ceasefire extension by Apr 21 market at 71%. General ceasefire sentiment drops to ~42% as blockade creates uncertainty
- Trump says ceasefire "holding well" but "I don't care" whether Iran returns to negotiating table. Contradictory signals from White House
- Hezbollah-Israel escalation continues separately from Iran ceasefire; Israel asserts ceasefire does not cover Lebanon
- VLCC rates surge to ~90K/day as war-risk premiums remain extreme; major P&I clubs suspend war risk cover for Gulf transits
- Cumulative (official): 537 BMs, 26 cruise missiles, 2,256 drones; ~13 dead, ~230 injured (unchanged — sixth consecutive zero-casualty day)

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.236
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.000
  + λ_武器           = +0.000
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.240
  ────────────────────────────
  λ 中位数       = 1.101（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **1.101** |
| λ 第95百分位 | **1.515** |
| P(λ > 1.0) | **67.3%** |
| P(λ > 1.5) | **5.2%** |
| P(λ > 2.0) | **2.4%** |
| 判定 | **不稳定** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day46.png)

![Lambda演变](../../charts/lambda_evolution_day46.png)

---

## 建议

**撤离。** 系统已跨越级联阈值。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-04-14 23:06 |
