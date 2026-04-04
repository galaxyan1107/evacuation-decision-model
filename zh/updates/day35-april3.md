# 第35天更新 — 2026年4月3日

> 🌐 [English](../../updates/day35-april3.md) | **中文**

**状态：不稳定** | **突破：5/5** | **λ中位数 = 2.127**

---

## 新数据

| 指标 | 第34天 | 第35天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 19 | **18** | **474** |
| 弹道导弹拦截 | 17 | 16 | 449 |
| 无人机探测 | 26 | ~47 | ~2191 |
| 无人机拦截 | 22 | 40 | ~2022 |
| 巡航导弹 | 0 | 4 | 16 |
| 弹道导弹拦截率（累计） | — | — | 94.7% |
| 无人机库存剩余 | — | — | -9.6%（-191/2000） |

**关键事件：**
- @modgovae: 18 BMs engaged (~16 intercepted, 1 fell sea, 1 fell land), 4 cruise missiles, 47 drones detected (~40 intercepted, ~7 fell UAE); cumulative 475 BMs, 23 cruise, 2,085 drones
- CRUISE MISSILES RETURN AGAIN: 4 cruise missiles fired — second consecutive salvo after Day 32's 4; cumulative now 23
- HABSHAN GAS COMPLEX FIRE: Falling debris from successful interception ignites fire at Abu Dhabi Habshan gas facility; operations suspended; no injuries reported
- 12 injured in Ajban area from falling interception debris — 7 Nepalese, 5 Indian nationals
- Iran expands Hormuz selective passage — Philippine-flagged vessels and Filipino seafarers now permitted after talks
- 12 vessels transit Hormuz (up from ~4/day in late March) — Iran toll booth system continues
- WTI surpasses Brent in rare inversion: WTI ~$111.54, Brent ~$109.03; WTI surges 12%+ on Iran escalation fears
- UK 30+ nation Hormuz summit continues; 3 ships attempt new Oman coast route to bypass Iranian waters
- Iran rejects US 15-point ceasefire proposal transmitted via Pakistan; issues counter-demands
- Polymarket ceasefire-by-Apr-30 at ~22% (down from ~25% Day 34) — markets increasingly skeptical
- DXB operating at ~53% capacity; most European/North American carriers remain suspended
- Total projectiles today: 69 (18 BM + 4 CM + 47 drones) — highest since early conflict days
- Cumulative: ~13 dead, ~206 injured

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.219
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.200
  ────────────────────────────
  λ 中位数       = 2.127（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.127** |
| λ 第95百分位 | **2.841** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.7%** |
| P(λ > 2.0) | **63.6%** |
| 判定 | **不稳定** |
| 突破数 | **5/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day35.png)

![Lambda演变](../../charts/lambda_evolution_day35.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-04-03 19:03 |
