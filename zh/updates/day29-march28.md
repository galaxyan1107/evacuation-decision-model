# 第29天更新 — 2026年3月28日

> 🌐 [English](../../updates/day29-march28.md) | **中文**

**状态：不稳定** | **突破：2/5** | **λ中位数 = 2.114**

---

## 新数据

| 指标 | 第28天 | 第29天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 6 | **20** | **397** |
| 弹道导弹拦截 | 6 | 20 | 376 |
| 无人机探测 | 9 | ~37 | ~1978 |
| 无人机拦截 | 7 | 33 | ~1836 |
| 巡航导弹 | 0 | 0 | 8 |
| 弹道导弹拦截率（累计） | — | — | 94.7% |
| 无人机库存剩余 | — | — | 1.1%（22/2000） |

**关键事件：**
- @modgovae: 20 BMs intercepted, 37 drones detected (33 intercepted, 4 fell UAE); cumulative 398 BMs, 15 cruise, 1,872 drones
- BM SURGE: 6→20 (+233%) — largest daily count since Day 27 rebound (15); volatile pattern continues (Day 26: 0, Day 27: 15, Day 28: 6, Day 29: 20)
- 1 civilian killed (Asian nationality) + 6 injured (5 Indians + 1 Pakistani) from interception debris at Kezad, Abu Dhabi
- US troops injured in Iran attack on Saudi base — war reaches one-month mark (NPR)
- Oil surges sharply: WTI $99.64 (+5.46%, session high $100.04 breaches $100 intraday); Brent $112.57 (+4.22%)
- Iran Hormuz toll booth system continues; ~2 selective transits; IRGC checks nationality/cargo/crew
- Multiple international carriers still suspended (KLM through May 17, Turkish through end March, Air France through Mar 31)
- DXB operating ~45% capacity; Emirates + flydubai maintaining reduced schedules
- 3rd carrier (USS George H.W. Bush) crossing Atlantic toward theater; 3 CSGs converging
- Polymarket ceasefire-by-Mar-31 declining to ~15% with only 3 days remaining
- Cumulative: 12 dead, ~177 injured

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.198
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.192
  ────────────────────────────
  λ 中位数       = 2.114（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.114** |
| λ 第95百分位 | **2.826** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.5%** |
| P(λ > 2.0) | **62.1%** |
| 判定 | **不稳定** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day29.png)

![Lambda演变](../../charts/lambda_evolution_day29.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-03-28 23:07 |
