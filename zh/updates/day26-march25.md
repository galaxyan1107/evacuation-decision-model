# 第26天更新 — 2026年3月25日

> 🌐 [English](../../updates/day26-march25.md) | **中文**

**状态：不稳定** | **突破：2/5** | **λ中位数 = 2.171**

---

## 新数据

| 指标 | 第25天 | 第26天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | 5 | **0** | **356** |
| 弹道导弹拦截 | 5 | 0 | 335 |
| 无人机探测 | 17 | ~9 | ~1921 |
| 无人机拦截 | 14 | 7 | ~1787 |
| 巡航导弹 | 0 | 0 | 8 |
| 弹道导弹拦截率（累计） | — | — | 94.1% |
| 无人机库存剩余 | — | — | 4.0%（79/2000） |

**关键事件：**
- FIRST DAY WITHOUT BALLISTIC MISSILES — 0 BMs detected since conflict began Feb 28 (@modgovae via Gulf News)
- Only 9 drones engaged; cumulative 357 BMs, 15 cruise, 1,815 drones (@modgovae)
- Trump claims US and Iran 'in negotiations now'; Iran denies: 'no talks or negotiations for 25 days'
- Iran formally requires crew/cargo manifests and IRGC approval for Hormuz transit; 6 vessels transited openly
- Oil crashes: WTI -5.1% to $87.63; Brent -5% to $99.30 on Trump diplomacy claims
- Air India resumes ad-hoc Dubai-Delhi flights (26 flights); Emirates limited schedule continues
- Iran says 'non-hostile' ships can pass Hormuz safely; formalizing selective blockade regime
- Iran won't accept ceasefire offer per state media (FARS); Trump's 15-point peace plan received by Iran (AP)

---

## Lambda重新计算

```
λ = 1.0
  + λ_发射装置         = -0.544
  + λ_无人机          = +0.192
  + λ_拦截           = +0.000
  + λ_霍尔木兹         = +0.630
  + λ_代理人          = +0.500
  + λ_武器           = +0.400
  + λ_弹道反弹         = +0.000
  + λ_海军威慑         = -0.128
  ────────────────────────────
  λ 中位数       = 2.171（50K蒙特卡罗）
```

| 指标 | 数值 |
|------|------|
| λ 中位数 | **2.171** |
| λ 第95百分位 | **2.884** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.6%** |
| P(λ > 2.0) | **68.3%** |
| 判定 | **不稳定** |
| 突破数 | **2/5** |

---

## 图表

![模型vs实际](../../charts/model_vs_actual_day26.png)

![Lambda演变](../../charts/lambda_evolution_day26.png)

---

## 建议

**立即撤离。** 系统处于级联区域。

---

## 数据来源

| 来源 | 类型 |
|------|------|
| @modgovae (X.com) | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM (50K MC) |
| 生成时间 | 2026-03-25 23:09 |
