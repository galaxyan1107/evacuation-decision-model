# 第28天更新 — 2026年3月27日

> 🌐 [English](../../updates/day28-march27.md) | **中文**

**状态：不稳定** | **突破：2/5** | **λ中位数 = 2.118**

---

## 新数据

| 指标 | 第27天 | 第28天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 15 | **6** | **377** |
| 弹道导弹拦截 | 15 | 6 | 356 |
| 无人机探测 | 11 | ~9 | ~1941 |
| 无人机拦截 | 9 | 7 | ~1803 |
| 巡航导弹 | 0 | 0 | 8 |
| 弹道导弹拦截率（累计） | — | — | 94.4% |
| 无人机库存剩余 | — | — | 2.9%（59/2000） |

**关键事件：**
- @modgovae: 6 BMs intercepted, 9 drones detected; cumulative 378 BMs, 15 cruise, 1,835 drones
- 3 Chinese ships (incl. COSCO vessels) turned away from Hormuz — IRGC declares strait 'shut', contradicting Trump claims
- Trump delays attacks on Iranian energy sector by 10 days (to April 6), cites 'very well' talks
- Iran calls US proposal 'one-sided and unfair'; Pakistan relaying messages between Washington and Tehran
- Brent tops $110 again ($111.06) on Chinese ship Hormuz incident; WTI $97.01
- 3 US carrier strike groups converging: Lincoln (Arabian Sea), Ford (Red Sea), Bush (crossing Atlantic)
- Saudi/UAE/Iraq pipeline alternatives discussed as oil escape routes from Hormuz dependency
- Cumulative: 11 dead, ~171 injured

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.194
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.184
  ────────────────────────────
  λ 中位数       = 2.118（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.118** |
| λ 第95百分位 | **2.830** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.6%** |
| P(λ > 2.0) | **62.6%** |
| 判定 | **不稳定** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day28.png)

![Lambda演变](../../charts/lambda_evolution_day28.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-03-27 23:09 |
