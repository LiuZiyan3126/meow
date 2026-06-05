# MEOW — 金融高频订单簿分钟级收益率预测

基于 ResidualMLP 神经网络的 P-quant 金融时序预测项目。利用约 300 只 A 股分钟级高频订单簿数据，预测 12 分钟后的中间价变化率。

西北工业大学计算机学院《模式识别与机器学习》期末大作业。

## 快速开始

```bash
# 1. 安装依赖
pip install torch scikit-learn pandas tables numpy

# 2. 准备数据：将 archive/ 目录（含 .h5 文件）放到项目根目录

# 3. 运行（自动训练 6-11 月 + 评估 12 月）
python meow.py
```

如果已训练并保存过模型权重，再次运行时会自动加载 `model_weights.pt` 和 `scaler.pkl`，跳过训练直接评估。

## 项目结构

```
meow.py                    # 入口调度器 (MeowEngine)
src/                       # 源码模块
├── __init__.py
├── nn_model.py            # ResidualMLP 网络结构定义
├── mdl.py                 # 模型训练/推理包装器 (MeowModel)
├── feat.py                # 特征工程生成器 (MeowFeatureGenerator)
├── dl.py                  # HDF5 数据加载器 (MeowDataLoader)
├── eval.py                # 评估器 (MeowEvaluator)
├── tradingcalendar.py     # 交易日历
└── log.py                 # 日志工具
scripts/                   # 独立脚本
├── 1.py                   # 可视化脚本（预测 vs 真实散点图）
└── make_ppt.py            # PPT 生成脚本
doc/                       # 文档与报告
resources/                 # 资源文件（交易日历）
archive/                   # HDF5 数据目录
```

## 方法概览

### 特征工程（62 特征，7 大类）

| 类别 | 特征数 | 说明 |
|------|--------|------|
| A. 订单簿不平衡 | 8 | 多档位数量/金额加权不平衡、深度集中度 |
| B. 价差与微观结构 | 8 | 各报价价差、价差斜率、Kyle 微观价格 |
| C. 成交流特征 | 10 | 量/笔数/金额三维成交不平衡、VWAP 价差 |
| D. 委托/撤单动态 | 10 | 新增/撤单不平衡、净挂单流 |
| E. 滚动时序统计 | 16 | 关键特征的 rolling mean/std（5/12/24 窗口） |
| F. 截面特征 | 5 | 相对截面均值的偏离、滞后收益率 |
| G. 交互特征 | 4 | trade_imb×spread、ob_imb0×midpx_ret1 等 |

### 模型架构

**ResidualMLP** — 带残差连接的多层感知机：

```
Input(62) → Linear(128) → BN → GELU → Dropout(0.2)
  → Block1: 128→256, GELU, Dropout(0.3)
  → Block2: 256→256, GELU, Dropout(0.3)  [+残差连接]
  → Block3: 256→128, GELU, Dropout(0.3)  [+残差投影]
  → Block4: 128→64,  GELU, Dropout(0.2)
  → Head:  64→1
```

总参数量约 165K，支持 GPU/CPU 自动检测。

### 训练策略

- **标签缩放**：训练时 y×100（解决 fret12 量级过小导致的梯度消失），推理时 ÷100
- **时序切分**：最后 15% 训练数据作为验证集，杜绝金融时序数据泄露
- **优化器**：AdamW (lr=1e-3, weight_decay=1e-4) + ReduceLROnPlateau
- **早停**：patience=25，恢复最佳 checkpoint
- **分批推理**：batch_size=8192，torch.no_grad() 下执行，防止 OOM

## 评估结果

| 指标 | 基线 (Ridge 6特征) | 本方案 (ResidualMLP 62特征) |
|------|--------------------|------------------------------|
| Pearson 相关系数 | 0.025 | **0.0643** (2.6× 提升) |
| R² | < 0 | 0.0041 |
| MSE | — | 5.5×10⁻⁵ |

Pearson 达到课程预期 5-10% 区间，相较线性基线提升约 2.6 倍。

## 硬件要求

- **GPU 训练**：RTX 4060 (8GB) 可完整训练约 700 万样本
- **CPU 推理**：任意含 8GB+ RAM 的机器即可运行推理和评估
- 训练时间约 30-45 分钟（单卡 RTX 4060），推理约 1-2 分钟

## 文档

- [doc/DESIGN.md](doc/DESIGN.md) — 详细设计文档（特征公式、模型架构、创新点）
- [doc/CONTRIBUTION.md](doc/CONTRIBUTION.md) — 小组成员分工
- [doc/实验报告.md](doc/实验报告.md) — 课程实验报告
- [doc/升级方案.md](doc/升级方案.md) — 项目升级优化方案
- [doc/模型选型与对比分析.md](doc/模型选型与对比分析.md) — 可用模型排名与分析
