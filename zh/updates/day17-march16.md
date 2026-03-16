# 第17天更新 — 2026年3月16日

> 🌐 [English](../../updates/day17-march16.md) | **中文**

**状态：不稳定** | **突破：4/5** | **λ中位数 = 2.152**

---

## 新数据

| 指标 | 第16天 | 第17天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 4 | **7** | **303** |
| 弹道导弹拦截 | 4 | 6 | 282 |
| 无人机探测 | 6 | ~25 | ~1733 |
| 无人机拦截 | 5 | 21 | ~1630 |
| 巡航导弹 | 0 | 0 | 8 |
| 弹道导弹拦截率（累计） | — | — | 93.1% |
| 无人机库存剩余 | — | — | 13.4%（267/2000） |

**关键事件：**
- @modgovae: 6 BMs intercepted, 21 drones intercepted (Times of Israel); 1 missile fell on civilian car
- Drone attack sparks fire near DXB fuel tank; flights temporarily suspended then gradual resumption
- Abu Dhabi: missile hits civilian car in Al Bahyan area — 1 Palestinian killed (cumulative 7 dead)
- Fujairah: fire in industrial oil facility from drone attack, no injuries
- Iran FM Araghchi: Hormuz 'open but closed to our enemies'
- Iran destroys Italian MQ-9A Predator UAV at Ali Al Salem Air Base, Kuwait (The Week)
- Brent $104.73 (+1.6%); oil up >40% since Feb 28

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.173
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.128
  ────────────────────────────
  λ 中位数       = 2.152（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.152** |
| λ 第95百分位 | **2.865** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.3%** |
| P(λ > 2.0) | **66.5%** |
| 判定 | **不稳定** |
| 突破数 | **4/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day17.png)

![Lambda演变](../../charts/lambda_evolution_day17.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-03-16 23:29 |
