# 第31天更新 — 2026年3月30日

> 🌐 [English](../../updates/day31-march30.md) | **中文**

**状态：不稳定** | **突破：2/5** | **λ中位数 = 2.113**

---

## 新数据

| 指标 | 第30天 | 第31天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 16 | **11** | **424** |
| 弹道导弹拦截 | 16 | 11 | 403 |
| 无人机探测 | 42 | ~27 | ~2047 |
| 无人机拦截 | 37 | 25 | ~1898 |
| 巡航导弹 | 0 | 0 | 8 |
| 弹道导弹拦截率（累计） | — | — | 95.0% |
| 无人机库存剩余 | — | — | -2.4%（-47/2000） |

**关键事件：**
- @modgovae: 11 BMs engaged, 27 UAVs engaged; cumulative 425 BMs, 15 cruise, 1,941 UAVs
- HOUTHIS ENTER WAR: Launch 2nd strike on Israel (cruise missiles + drones); threaten Bab al-Mandeb closure
- Oil surges 3%: WTI $102.85, Brent $115.35 — Brent on pace for steepest monthly rise on record (+55% in March)
- SocGen forecasts $150/bbl possible in April if Houthis block Bab al-Mandeb
- Polymarket ceasefire-by-Mar-31 collapses to ~2% (market expires tomorrow)
- DXB improving: Emirates, British Airways, Lufthansa, Air India, IndiGo all operating at ~60% capacity
- Houthis: 'Closing Bab al-Mandeb is among our options' — dual-strait closure risk emerges
- 0 new deaths; 0 new injuries; cumulative: 12 dead, ~178 injured

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.205
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.200
  ────────────────────────────
  λ 中位数       = 2.113（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.113** |
| λ 第95百分位 | **2.825** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.5%** |
| P(λ > 2.0) | **62.0%** |
| 判定 | **不稳定** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day31.png)

![Lambda演变](../../charts/lambda_evolution_day31.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-03-30 23:07 |
