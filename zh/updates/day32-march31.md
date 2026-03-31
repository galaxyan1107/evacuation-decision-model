# 第32天更新 — 2026年3月31日

> 🌐 [English](../../updates/day32-march31.md) | **中文**

**状态：不稳定** | **突破：2/5** | **λ中位数 = 2.116**

---

## 新数据

| 指标 | 第31天 | 第32天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 11 | **8** | **432** |
| 弹道导弹拦截 | 11 | 8 | 411 |
| 无人机探测 | 27 | ~36 | ~2083 |
| 无人机拦截 | 25 | 32 | ~1930 |
| 巡航导弹 | 0 | 4 | 12 |
| 弹道导弹拦截率（累计） | — | — | 95.1% |
| 无人机库存剩余 | — | — | -4.2%（-83/2000） |

**关键事件：**
- @modgovae: 8 BMs intercepted, 4 cruise missiles, 36 drones detected (~32 intercepted); cumulative 433 BMs, 19 cruise, 1,977 drones
- CRUISE MISSILES RETURN: First cruise missiles since early March — 4 launched, marking significant escalation in weapon diversity
- Kuwaiti VLCC Al Salmi (2M bbl loaded) struck by Iranian drone at Dubai Port anchorage — fire extinguished, 24 crew safe, no oil spill
- 4 Asian nationals injured in southern Dubai from interception debris falling on residential houses
- 3 UN peacekeeping troops killed (per Al Jazeera liveblog)
- Trump escalates Iran threats; Polymarket ceasefire-by-Mar-31 expires at ~1% (resolving NO)
- Oil: WTI $102.24, Brent ~$106.56; Brent completes steepest monthly rise on record (~55% in March)
- Houthis continue Bab al-Mandeb threats but pledge to keep strait open 'for now'
- DXB operating limited flights ~55% capacity; BA suspended through May 31; Air France through Mar 31
- Hormuz selective transits continue; ~4 vessels; Iran toll booth system active
- Cumulative: 12 dead, ~182 injured

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.208
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.200
  ────────────────────────────
  λ 中位数       = 2.116（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.116** |
| λ 第95百分位 | **2.828** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.5%** |
| P(λ > 2.0) | **62.4%** |
| 判定 | **不稳定** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day32.png)

![Lambda演变](../../charts/lambda_evolution_day32.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-03-31 23:07 |
