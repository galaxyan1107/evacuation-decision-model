# 第25天更新 — 2026年3月24日

> 🌐 [English](../../updates/day25-march24.md) | **中文**

**状态：不稳定** | **突破：2/5** | **λ中位数 = 2.170**

---

## 新数据

| 指标 | 第24天 | 第25天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 7 | **5** | **356** |
| 弹道导弹拦截 | 7 | 5 | 335 |
| 无人机探测 | 16 | ~17 | ~1912 |
| 无人机拦截 | 14 | 14 | ~1780 |
| 巡航导弹 | 0 | 0 | 8 |
| 弹道导弹拦截率（累计） | — | — | 94.1% |
| 无人机库存剩余 | — | — | 4.4%（88/2000） |

**关键事件：**
- @modgovae: 5 BMs intercepted, 17 drones detected (~14 intercepted); cumulative ~357 BMs, 15 cruise, ~1,806 drones
- Trump 5-day delay on Iran power plant strikes enters Day 2; Pakistan/Turkey/Egypt/Oman mediating
- Iranian source acknowledges US 'outreach' to CNN; possible Vance-Iran meeting in Pakistan this week
- Oil rebounds: WTI $92.39 (+4.8%), Brent $102.47 — markets skeptical of de-escalation durability
- Indian national suffers minor injuries from interception debris in al-Shawamekh, Abu Dhabi
- Polymarket ceasefire-by-Mar-31 surges to ~20% amid suspected insider trading (10 new accounts wagered $160K)
- Selective Hormuz transits continue expanding; ~24 vessels/day; Japan, China, India, Pakistan permitted

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.191
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.128
  ────────────────────────────
  λ 中位数       = 2.170（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.170** |
| λ 第95百分位 | **2.883** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.6%** |
| P(λ > 2.0) | **68.3%** |
| 判定 | **不稳定** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day25.png)

![Lambda演变](../../charts/lambda_evolution_day25.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-03-25 01:31 |
