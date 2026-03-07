# 每日更新管线

> 🌐 [English](../../pipeline/README.md) | **中文**

自动化每日流程，使用阿联酋国防部（@modgovae）等来源的新数据更新撤离决策模型。

---

## 快速开始

```bash
# 处理daily_data.json中的最新天数据
python pipeline/daily_update.py

# 通过命令行添加新一天并处理
python pipeline/daily_update.py --add \
    --day 9 --date 2026-03-08 \
    --bm 12 --bm-int 11 --bm-sea 1 \
    --drones 118 --drones-int 112 --drones-fell 6 \
    --deaths 0 --injuries 14 \
    --airport 60 --oil 99 --vlcc 430000 \
    --hormuz-status closed \
    --carriers 3 --carriers-eff 2.5 \
    --events "12枚弹道导弹|阿联酋航空65%网络" \
    --notes "第9天更新"

# 交互式添加新一天
python pipeline/daily_update.py --add
```

---

## 管线步骤

脚本按顺序执行6个步骤：

| 步骤 | 操作 | 输出 |
|------|------|------|
| 1 | **蒙特卡罗模拟**（50K次） | λ中位数、P(λ>1)、判定、突破数 |
| 2 | **对比图表**（6面板） | `charts/model_vs_actual_day{N}.png` |
| 3 | **Lambda演变图** | `charts/lambda_evolution_day{N}.png` |
| 4 | **英文更新页** | `updates/day{N}-{month}{day}.md` |
| 5 | **中文更新页** | `zh/updates/day{N}-{month}{day}.md` |
| 6 | **SUMMARY.md** 导航更新 | 新页面链接 |

---

## 数据文件

所有历史数据存储在 `pipeline/daily_data.json`。

### 每日数据采集来源

| 字段 | 来源 | 说明 |
|------|------|------|
| 弹道导弹/无人机数据 | @modgovae (X.com) | 阿联酋国防部每日公报 |
| 伤亡数据 | WAM/路透社 | 阿联酋通讯社 |
| 机场运力 | Gulf News | 航空新闻 |
| 油价/VLCC | 彭博社 | 财经数据 |
| 海峡状态 | 海事追踪 | Seatrade Maritime等 |
| 停火概率 | Polymarket | 预测市场 |
| 航母部署 | USNI News | 海军追踪 |

---

## 模型参数

### Lambda分量

```
λ = 1.0（基准）
  + λ_发射装置     = f(TEL消耗率)      稳定效应（-）
  + λ_无人机       = f(库存剩余)        不稳定（+）
  + λ_拦截         = f(累计拦截率)      不稳定（+）
  + λ_霍尔木兹     = f(海峡状态)        不稳定（+）
  + λ_代理人       = f(代理人激活)      不稳定（+）
  + λ_武器         = f(新升级)          不稳定（+）
  + λ_弹道反弹     = f(弹道导弹趋势)    不稳定（+）
  + λ_海军威慑     = f(航母数量)        稳定效应（-）
```

### 级联阈值

| 指标 | 阈值 | 突破条件 |
|------|------|---------|
| 发射装置消耗 | > 85% | 突破 |
| 无人机库存 | < 30% | 突破 |
| 拦截率（累计） | < 90% | 突破 |
| 每日伤亡 | > 10 | 突破 |
| 新武器/目标 | 任何 | 突破 |

**判定规则：** ≥3突破 = 不稳定，≥1 = 亚稳态，0 = 稳定

---

## 运行日志

每次管线运行的记录保存在 `pipeline/run_log.json`，包含时间戳、天数、λ中位数、判定和突破数。
