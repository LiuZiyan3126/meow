"""Generate MEOW project presentation PPT."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

DARK_BG = RGBColor(0x0D, 0x0D, 0x1A)
CARD_BG = RGBColor(0x22, 0x22, 0x3A)
ACCENT = RGBColor(0x00, 0x9E, 0xFF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xCC, 0xCC, 0xCC)
GREEN = RGBColor(0x00, 0xE6, 0x96)
ORANGE = RGBColor(0xFF, 0xA5, 0x00)
GRAY = RGBColor(0x88, 0x88, 0x99)
RED = RGBColor(0xFF, 0x55, 0x55)
YELLOW = RGBColor(0xFF, 0xD7, 0x00)
BAR_BG = RGBColor(0x12, 0x12, 0x28)


def bg(slide, color=DARK_BG):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color


def tb(slide, left, top, width, height, text, font_size=18,
       color=WHITE, bold=False, align=PP_ALIGN.LEFT, font_name="Microsoft YaHei"):
    box = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.alignment = align
    return tf


def ml(slide, left, top, width, height, lines,
       font_size=16, color=WHITE, line_sp=1.3, font_name="Microsoft YaHei"):
    box = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, (text, fs, clr, bld) in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = text
        p.font.size = Pt(fs if fs else font_size)
        p.font.color.rgb = clr if clr else color
        p.font.bold = bld if bld is not None else False
        p.font.name = font_name
        p.space_after = Pt(font_size * (line_sp - 1))
    return tf


def title_bar(slide, title, subtitle=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0),
        prs.slide_width, Inches(1.1))
    shape.fill.solid()
    shape.fill.fore_color.rgb = BAR_BG
    shape.line.fill.background()
    tb(slide, 0.8, 0.15, 11.5, 0.8, title, font_size=34, bold=True)
    if subtitle:
        tb(slide, 0.8, 0.75, 11.5, 0.4, subtitle, font_size=16, color=LIGHT)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.1),
        Inches(2.0), Inches(0.04))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT
    line.line.fill.background()


def card(slide, left, top, width, height):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = CARD_BG
    shape.line.fill.background()
    return shape


def section_title(slide, number, title, subtitle=None):
    bg(slide)
    tb(slide, 1.2, 1.5, 2, 2, f"{number:02d}", font_size=96,
       color=ACCENT, bold=True)
    tb(slide, 1.2, 3.8, 11, 1, title, font_size=44, bold=True)
    if subtitle:
        tb(slide, 1.2, 5.0, 11, 0.8, subtitle, font_size=20, color=LIGHT)
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.8),
        Inches(2.5), Inches(0.05))
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT
    line.line.fill.background()


def pn(slide, num):
    tb(slide, 12.2, 7.05, 0.9, 0.35, str(num),
       font_size=11, color=GRAY, align=PP_ALIGN.RIGHT)


# ============================================================
# SLIDE 1: 封面
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
tb(slide, 1.2, 1.5, 11, 1.2, "MEOW", font_size=80, bold=True, color=ACCENT)
tb(slide, 1.2, 2.8, 11, 0.8, "金融高频订单簿分钟级收益率预测",
   font_size=40, bold=True)
tb(slide, 1.2, 3.8, 11, 0.5,
   "基于 ResidualMLP 神经网络的 P-quant 金融时序预测",
   font_size=20, color=LIGHT)
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(4.6),
    Inches(3.0), Inches(0.05))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT
line.line.fill.background()
tb(slide, 1.2, 5.0, 11, 0.4,
   "西北工业大学计算机学院  /  《模式识别与机器学习》期末大作业",
   font_size=17, color=LIGHT)
tb(slide, 1.2, 5.5, 11, 0.4,
   "汇报人：欧阳熠  |  组员：刘子彦、顾思豪、欧阳熠",
   font_size=17, color=GRAY)
tb(slide, 1.2, 6.5, 11, 0.4,
   "Pearson 0.0643  /  2.6x 基线提升  /  7 大类 62 特征  /  ResidualMLP",
   font_size=14, color=GRAY)

# ============================================================
# SLIDE 2: 项目概述
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "项目概述")
pn(slide, 2)

card(slide, 0.8, 1.5, 5.6, 2.3)
tb(slide, 1.1, 1.65, 5, 0.4, "任务定义", font_size=20, bold=True, color=ACCENT)
ml(slide, 1.1, 2.15, 5, 1.4, [
    ("利用约 300 只 A 股分钟级高频订单簿数据，"
     "预测 12 分钟后的中间价变化率 fret12", 15, WHITE, False),
    ("", 8, WHITE, False),
    ("fret12 = (P12 - P0) / P0", 18, ACCENT, True),
    ("", 8, WHITE, False),
    ("训练集: 2023.06-11（~123 个交易日，~700 万条）", 14, LIGHT, False),
    ("评估集: 2023.12（~21 个交易日，~150 万条）", 14, LIGHT, False),
])

card(slide, 6.9, 1.5, 5.6, 2.3)
tb(slide, 7.2, 1.65, 5, 0.4, "核心成果", font_size=20, bold=True, color=GREEN)
ml(slide, 7.2, 2.15, 5, 1.4, [
    ("", 10, WHITE, False),
    ("Pearson 相关系数", 16, LIGHT, False),
    ("0.025  ->  0.0643  (+157%)", 22, GREEN, True),
    ("", 6, WHITE, False),
    ("达到课程预期 5-10% 区间", 16, WHITE, False),
    ("2.6 倍基线 Ridge 提升", 16, WHITE, False),
])

card(slide, 0.8, 4.1, 11.7, 3.0)
tb(slide, 1.1, 4.25, 11, 0.4, "系统架构", font_size=20, bold=True, color=ACCENT)
ml(slide, 1.1, 4.75, 11, 2.1, [
    ("meow.py (MeowEngine)                        入口调度器",
     15, WHITE, False),
    ("  +-- dl.py (MeowDataLoader)              从 HDF5 加载数据",
     14, GRAY, False),
    ("  +-- feat.py (MeowFeatureGenerator)      7 大类 62 特征生成",
     14, GRAY, False),
    ("  +-- nn_model.py (ResidualMLP)           神经网络结构定义",
     14, GRAY, False),
    ("  +-- mdl.py (MeowModel)                  训练/标签缩放/分批推理/持久化",
     14, GRAY, False),
    ("  +-- eval.py (MeowEvaluator)             Pearson/R2/MSE + CSV 导出",
     14, GRAY, False),
    ("  +-- tradingcalendar.py (Calendar)       交易日历",
     14, GRAY, False),
])

# ============================================================
# SLIDE 3: 数据分析 EDA
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "一、数据分析", "EDA Findings")
pn(slide, 3)

card(slide, 0.8, 1.5, 5.6, 2.5)
tb(slide, 1.1, 1.65, 5, 0.35, "原始数据概况", font_size=20, bold=True, color=ACCENT)
ml(slide, 1.1, 2.15, 5, 1.6, [
    ("原始数据共 62 个字段，按来源分为四大类：", 15, WHITE, False),
    ("", 4, WHITE, False),
    ("  + 订单簿快照: bid/ask 在 0/4/9/19 档的价格、委托量、金额", 14, LIGHT, False),
    ("  + 主动成交统计: 成交笔数、量、额、最高/最低价、VWAP", 14, LIGHT, False),
    ("  + 委托新增统计: nAdd、addQty、addTurnover 等", 14, LIGHT, False),
    ("  + 撤销委托统计: nCxl、cxlQty、cxlTurnover 等", 14, LIGHT, False),
])

card(slide, 6.9, 1.5, 5.6, 2.5)
tb(slide, 7.2, 1.65, 5, 0.35, "缺失率统计与处理", font_size=20, bold=True, color=ACCENT)
ml(slide, 7.2, 2.15, 5, 1.6, [
    ("+ 订单簿与成交类字段：缺失率接近 0%", 14, WHITE, False),
    ("+ 委托新增/撤单类字段：缺失率 ~1.5-2.2%", 14, WHITE, False),
    ("  （部分分钟无新增或撤单事件，属正常现象）", 13, GRAY, False),
    ("+ 目标变量 fret12：缺失率 0%", 14, WHITE, False),
    ("", 6, WHITE, False),
    ("处理策略：统一 fillna(0)", 14, GREEN, True),
    ("将无事件视为「无活动」状态", 14, WHITE, False),
])

card(slide, 0.8, 4.3, 11.7, 2.8)
tb(slide, 1.1, 4.45, 11, 0.35, "目标变量 fret12 分布特征", font_size=20, bold=True, color=ACCENT)
ml(slide, 1.1, 4.9, 11, 2.0, [
    ("均值 ~0.0006，标准差 ~0.007，范围约 [-0.06, 0.09]", 15, WHITE, False),
    ("典型金融高频收益率分布特征：均值极接近零，窄峰但存在厚尾", 15, WHITE, False),
    ("", 6, WHITE, False),
    ("对模型训练的三大影响：", 15, YELLOW, True),
    ("  1. 目标值量级极小（1e-3 至 1e-4），直接计算 MSE 会导致梯度消失 -> 需要标签缩放", 14, LIGHT, False),
    ("  2. 高噪声特性决定预测值方差远小于真实值方差，R2 天然趋近于零", 14, LIGHT, False),
    ("  3. 特征尺度跨越 4-5 个数量级 -> 必须使用 BatchNorm + StandardScaler 标准化", 14, LIGHT, False),
])

# ============================================================
# SLIDE 4: Section 标题 - 特征工程
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
section_title(slide, 1, "特征挖掘与特征工程",
              "7 大类 62 特征  /  市场微观结构理论驱动  /  Cython 级计算效率")
pn(slide, 4)

# ============================================================
# SLIDE 5: 特征总览
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "一、特征工程 —— 7 大类 62 特征总览", "Feature System Overview")
pn(slide, 5)

cats = [
    ("A. 订单簿不平衡\n8 特征", ACCENT,
     ["ob_imb0 / 0_4 / 5_9 / 10_19",
      "ob_tr_imb0_4 / 5_9 / 10_19",
      "ob_depth_buy",
      "数量+金额双维度",
      "多档位分层覆盖"]),
    ("B. 价差与微观结构\n8 特征", GREEN,
     ["spread_bps0/4/9/19",
      "spread_slope",
      "micro_price (Kyle 1985)",
      "mp_dev / midpx_ret1",
      "价差成本+均衡价格"]),
    ("C. 成交流\n10 特征", ORANGE,
     ["trade_imb (量不平衡)",
      "trade_count_imb (笔数不平衡)",
      "trade_tvr_imb (金额不平衡)",
      "trade_vwap_sprd",
      "trade_intensity 等"]),
    ("D. 委托/撤单动态\n10 特征", YELLOW,
     ["add_imb / cxl_imb",
      "add_count_imb / cxl_count_imb",
      "net_flow (净挂单流)",
      "add_cxl_ratio",
      "挂单意愿与意图变化"]),
]
for col, (title, clr, lines) in enumerate(cats):
    left = 0.5 + col * 3.15
    card(slide, left, 1.5, 2.95, 3.3)
    tb(slide, left + 0.2, 1.6, 2.6, 0.6, title, font_size=16, bold=True, color=clr)
    ml(slide, left + 0.2, 2.3, 2.6, 2.3,
       [(ln, 12, WHITE if ln else WHITE, False) for ln in lines])

cats2 = [
    ("E. 滚动时序统计\n16 特征", RED,
     ["基础 rolling mean/std（11 个）:",
      "trade_imb_ma5/ma12/std12",
      "ob_imb0_ma5/std12",
      "midpx_ret1_ma5/ma12/std12/std24",
      "spread_bps0_ma12, intensity_ma5/12",
      "衍生特征（5 个）:",
      "vol_ratio5/12, spread_chg5,",
      "imb_chg5, ret_ma_accel"]),
    ("F. 截面特征\n5 特征", ACCENT,
     ["cx_ret1 / cx_relret1",
      "cx_trade_imb / cx_ob_imb0",
      "lagret12",
      "",
      "通过 groupby(interval).transform",
      "去均值分离：",
      "市场共同信号 vs 个股异质信号",
      "动量/反转效应检验"]),
    ("G. 交互特征\n4 特征", GREEN,
     ["imb_x_spread",
      " = trade_imb * spread_bps0",
      "obi_x_ret",
      " = ob_imb0 * midpx_ret1",
      "act_x_spread",
      " = trade_intensity * spread_bps0",
      "obi_x_vol",
      " = ob_imb0 * midpx_ret1_std12"]),
]
for col, (title, clr, lines) in enumerate(cats2):
    left = 0.5 + col * 4.2
    card(slide, left, 5.1, 3.95, 2.1)
    tb(slide, left + 0.2, 5.2, 3.6, 0.5, title, font_size=15, bold=True, color=clr)
    ml(slide, left + 0.2, 5.75, 3.6, 1.35,
       [(ln, 11, WHITE if ln else WHITE, False) for ln in lines])

# ============================================================
# SLIDE 6: 特征设计逻辑
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "一、特征工程 —— 设计逻辑详解", "Feature Design Rationale")
pn(slide, 6)

designs = [
    ("订单簿不平衡：数量 vs 金额 vs 多档位分层",
     "数量不平衡 =「有多少股愿意买卖」，金额不平衡 =「有多少资金」--> 区分散户(数量敏感) vs 机构(金额敏感)。"
     "多档位分层：最优档(0)、近端5档(0_4)、中端5档(5_9)、远端10档(10_19) --> 区分「浅层博弈」与「深层布局」。"
     "ob_depth_buy 衡量买方流动性是否过度集中在近端。"),
    ("成交流：量/笔数/金额三维不平衡 + 活跃度",
     "trade_imb =「有多少股」主动买卖，trade_count_imb =「有多少人」，trade_tvr_imb =「有多少钱」。"
     "大单倾向于金额加权捕捉，散户跟风倾向用笔数捕捉。"
     "trade_intensity（活跃度）越高，成交方向信号越可靠。trade_vwap_sprd 衡量买卖成交均价的偏离。"),
    ("委托/撤单：net_flow 捕捉被动交易意图",
     "add（新增委托）反映挂单意愿，cxl（撤销）反映撤单意愿。net_flow = add - cxl 衡量净挂单意愿变化。"
     "买方 net_flow > 0 表示买方限价单净增加 -> 买盘堆积 -> 对价格有支撑作用。"
     "add_cxl_ratio = add/(add+cxl) 衡量挂单持续性。"),
    ("滚动时序统计：窗口选择与衍生特征设计",
     "窗口 5min（短线交易者反应时间）、12min（匹配预测目标周期）、24min（更长期波动率基准）。"
     "vol_ratio = 当前成交量 / 历史均值 -> 成交量异常检测。"
     "ret_ma_accel = 短期动量 - 长期动量 -> 判断动量加速还是减速。spread_chg5/imb_chg5 捕捉近期变化。"),
    ("截面特征：分离市场共同信号与个股异质信号",
     "每个截面上所有股票的收益率 = 市场共同部分 + 个股异质部分。"
     "cx_relret1 = 个股收益 - 截面均值，反映个股相对市场的超额表现。"
     "lagret12 基于过去 12 分钟超额收益，用于检验动量/反转效应。所有截面去均值操作使用 groupby(interval).transform。"),
    ("交互特征：条件依赖关系的显式化",
     "imb_x_spread：宽价差时成交方向信号更可信（流动性差时，主动成交更可能是知情交易）。"
     "obi_x_ret：订单簿方向与近期价格的共振/背离。"
     "obi_x_vol：不同波动率状态下订单簿信号的差异化表达。act_x_spread：高活跃度+宽价差的异常状态捕捉。"),
]
for row, (title, desc) in enumerate(designs):
    top = 1.3 + row * 1.02
    card(slide, 0.5, top, 12.3, 0.95)
    tb(slide, 0.7, top + 0.08, 12, 0.28, title, font_size=15, bold=True, color=ACCENT)
    tb(slide, 0.7, top + 0.38, 12, 0.55, desc, font_size=12, color=LIGHT)

# ============================================================
# SLIDE 7: 效率优化
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "一、特征工程 —— 效率优化",
          "Pandas 原生 Cython 路径替代 Python Lambda")
pn(slide, 7)

card(slide, 0.8, 1.5, 5.6, 2.5)
tb(slide, 1.1, 1.65, 5, 0.35, "常见错误做法 (OOM/极慢)",
   font_size=18, bold=True, color=RED)
ml(slide, 1.1, 2.2, 5, 1.6, [
    ('df.groupby(["symbol","date"])["col"]', 14, LIGHT, False),
    ("  .transform(lambda x: x.rolling(5).mean())", 14, LIGHT, False),
    ("", 8, WHITE, False),
    ("问题：lambda 逐组调用 Python 解释器", 14, RED, False),
    ("-> 700 万行数据 OOM 或数十分钟卡死", 14, RED, False),
])

card(slide, 6.9, 1.5, 5.6, 2.5)
tb(slide, 7.2, 1.65, 5, 0.35, "我们的方案 (~30 秒完成)",
   font_size=18, bold=True, color=GREEN)
ml(slide, 7.2, 2.2, 5, 1.6, [
    ('df.set_index(["symbol","date"])["col"]', 14, LIGHT, False),
    ("  .groupby(level=[0,1])", 14, LIGHT, False),
    ("  .rolling(window=5, min_periods=1)", 14, LIGHT, False),
    ("  .mean()", 14, LIGHT, False),
    ("", 8, WHITE, False),
    ("Cython 级 groupby rolling，无 Python 循环开销", 14, GREEN, True),
    ("-> 效率提升数十倍，内存安全", 14, GREEN, False),
])

card(slide, 0.8, 4.3, 11.7, 2.8)
tb(slide, 1.1, 4.45, 11, 0.35,
   "实现代码 (feat.py: MeowFeatureGenerator._rolling_mean / _rolling_std)",
   font_size=18, bold=True, color=ACCENT)
ml(slide, 1.1, 4.9, 11, 2.0, [
    ("def _rolling_mean(self, df, col, window):", 14, ACCENT, True),
    ("    return (", 14, LIGHT, False),
    ('        df.set_index(["symbol", "date"])[col]', 14, LIGHT, False),
    ("        .groupby(level=[0, 1])", 14, LIGHT, False),
    ("        .rolling(window=window, min_periods=1)", 14, LIGHT, False),
    ("        .mean()", 14, LIGHT, False),
    ("        .reset_index(level=[0, 1], drop=True)", 14, LIGHT, False),
    ("        .values", 14, LIGHT, False),
    ("    )", 14, LIGHT, False),
    ("# _rolling_std() 同理。共 16 个滚动特征全部走此 Cython 路径。", 13, GRAY, False),
    ("# 所有 shift 操作严格限定在 (symbol, date) 组内，杜绝跨日数据泄露。", 13, GRAY, False),
])

# ============================================================
# SLIDE 8: Section 标题 - 模型
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
section_title(slide, 2, "模型定义、选择与创新设计",
              "ResidualMLP  /  GELU+BN+残差+递减Dropout  /  标签缩放  /  时序验证")
pn(slide, 8)

# ============================================================
# SLIDE 9: 模型架构
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "二、模型架构 —— ResidualMLP", "网络结构与各组件设计理由")
pn(slide, 9)

card(slide, 0.8, 1.5, 7.0, 4.2)
tb(slide, 1.1, 1.65, 6.5, 0.35,
   "网络结构（总参数量 ~165K）", font_size=18, bold=True, color=ACCENT)
ml(slide, 1.1, 2.15, 6.5, 3.3, [
    ("Input(62)", 16, ACCENT, True),
    ("  |", 12, GRAY, False),
    ("Linear(62->128)  ->  BN  ->  GELU  ->  Dropout(0.2)", 15, WHITE, False),
    ("  |", 12, GRAY, False),
    ("Block1: 128->256, GELU, Dropout(0.3)         [无残差]", 15, WHITE, False),
    ("  |", 12, GRAY, False),
    ("Block2: 256->256, GELU, Dropout(0.3)         [+恒等残差]", 15, WHITE, False),
    ("  |", 12, GRAY, False),
    ("Block3: 256->128, GELU, Dropout(0.3)         [+投影残差]", 15, WHITE, False),
    ("  |", 12, GRAY, False),
    ("Block4: 128->64,  GELU, Dropout(0.2)         [无残差]", 15, WHITE, False),
    ("  |", 12, GRAY, False),
    ("Head: Linear(64->1)  [无激活函数，回归输出]", 15, ACCENT, True),
])

card(slide, 8.2, 1.5, 4.3, 4.2)
tb(slide, 8.5, 1.65, 3.8, 0.35, "各组件设计理由", font_size=18, bold=True, color=ACCENT)
ml(slide, 8.5, 2.15, 3.8, 3.3, [
    ("GELU 激活函数", 16, GREEN, True),
    ("零点附近平滑过渡，对金融小信号更敏感", 12, LIGHT, False),
    ("避免 ReLU 在负半区的「死神经元」问题", 12, LIGHT, False),
    ("Hendrycks & Gimpel, 2016", 10, GRAY, False),
    ("", 5, WHITE, False),
    ("BatchNorm1d", 16, GREEN, True),
    ("特征尺度差异大（4-5 个数量级）", 12, LIGHT, False),
    ("逐层标准化输入分布，兼有正则化效果", 12, LIGHT, False),
    ("Ioffe & Szegedy, 2015", 10, GRAY, False),
    ("", 5, WHITE, False),
    ("残差连接（仅中间两层）", 16, GREEN, True),
    ("缓解深层网络梯度消失", 12, LIGHT, False),
    ("学习恒等映射的扰动，而非从头学映射", 12, LIGHT, False),
    ("ResNet, He et al., 2016", 10, GRAY, False),
    ("", 5, WHITE, False),
    ("递减 Dropout (0.2->0.3->0.2)", 16, GREEN, True),
    ("中间层特征交互最复杂，最需要正则化", 12, LIGHT, False),
    ("输出前降低 Dropout 保留预测信号精度", 12, LIGHT, False),
])

card(slide, 0.8, 6.0, 11.7, 1.1)
tb(slide, 1.1, 6.1, 11, 0.3,
   "为什么不选用 LSTM / Transformer？", font_size=17, bold=True, color=YELLOW)
ml(slide, 1.1, 6.45, 11, 0.55, [
    ("LSTM/GRU 在极高噪声金融数据上容易过拟合序列模式中的噪声（而非真实信号）。"
     "Transformer 需要海量数据才能发挥优势。", 13, LIGHT, False),
    ("MLP + 残差在高噪声、样本相对有限时更鲁棒；"
     "且通过滚动统计特征已将时序信息注入输入层，无需循环结构显式建模。", 13, LIGHT, False),
])

# ============================================================
# SLIDE 10: 训练策略三大创新
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "二、训练策略三大创新", "Training Strategy Innovations")
pn(slide, 10)

strategies = [
    ("标签缩放\nTarget Scaling",
     GREEN,
     [("fret12 均值约 0.0006", LIGHT),
      ("直接计算 MSE 会导致梯度消失", LIGHT),
      ("", WHITE),
      ("训练: loss = MSE(pred, y x 100)", GREEN),
      ("推理: prediction = model(x) / 100", GREEN),
      ("", WHITE),
      ("梯度放大 100 倍，训练稳定收敛", GREEN)]),
    ("时序验证集切分\nAnti Look-ahead Bias",
     ORANGE,
     [("错误: train_test_split(shuffle=True)", RED),
      ("-> 未来信息泄露 -> 过拟合", RED),
      ("-> 实盘场景完全不可行", RED),
      ("", WHITE),
      ("正确: 按时间排序，最后 15% 日期做验证集", GREEN),
      ("-> 从源头杜绝 look-ahead bias", GREEN),
      ("", WHITE),
      ("金融数据核心原则：", LIGHT),
      ("永远不能用未来预测过去", YELLOW)]),
    ("分批推理 + 模型持久化\nSafe Inference",
     ACCENT,
     [("推理: torch.no_grad() + batch_size=8192", GREEN),
      ("-> 150 万样本不 OOM, 1-2 分钟完成", GREEN),
      ("", WHITE),
      ("持久化: 训练后自动保存", LIGHT),
      ("  model_weights.pt + scaler.pkl", LIGHT),
      ("-> 检测到文件则跳过训练，直接推理", GREEN),
      ("", WHITE),
      ("优化器: AdamW (Loshchilov & Hutter 2019)", LIGHT),
      ("早停: patience=25, 恢复最佳 checkpoint", LIGHT)]),
]
for i, (title, clr, lines) in enumerate(strategies):
    left = 0.8 + i * 4.1
    card(slide, left, 1.5, 3.8, 5.5)
    tb(slide, left + 0.3, 1.65, 3.2, 0.6, title,
       font_size=17, bold=True, color=clr)
    ml(slide, left + 0.3, 2.35, 3.2, 4.5,
       [(text, 14, color, False) for text, color in lines])

# ============================================================
# SLIDE 11: 实验结果
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "三、实验结果与分析", "Evaluation Results & Ablation Study")
pn(slide, 11)

card(slide, 0.8, 1.5, 5.6, 2.5)
tb(slide, 1.1, 1.65, 5, 0.35, "核心指标对比", font_size=18, bold=True, color=ACCENT)
ml(slide, 1.1, 2.1, 5, 1.7, [
    ("", 4, WHITE, False),
    ("Pearson:  0.025  ->  0.0643", 24, GREEN, True),
    ("                +157%  (2.6x 基线)", 16, LIGHT, False),
    ("", 8, WHITE, False),
    ("R2:        < 0   ->   0.0041", 18, WHITE, False),
    ("MSE:       --    ->   5.5e-5", 18, WHITE, False),
    ("", 8, WHITE, False),
    ("达到课程预期 5-10% 区间", 16, GREEN, True),
])

card(slide, 6.9, 1.5, 5.6, 2.5)
tb(slide, 7.2, 1.65, 5, 0.35, "消融实验", font_size=18, bold=True, color=ACCENT)
ml(slide, 7.2, 2.1, 5, 1.7, [
    ("移除特征组              Pearson 下降", 13, GRAY, False),
    ("A. 订单簿不平衡            -0.015  *", 14, WHITE, False),
    ("E. 滚动时序统计            -0.012  *", 14, WHITE, False),
    ("C. 成交流                  -0.008", 14, WHITE, False),
    ("G. 交互特征                -0.005", 14, WHITE, False),
    ("D. 委托/撤单               -0.004", 14, WHITE, False),
    ("B. 价差微观结构              -0.003", 14, WHITE, False),
    ("F. 截面特征                -0.002", 14, WHITE, False),
    ("全部 7 类均有正向贡献", 13, GREEN, True),
])

card(slide, 0.8, 4.3, 11.7, 2.8)
tb(slide, 1.1, 4.45, 11, 0.35, "关键发现", font_size=18, bold=True, color=YELLOW)
ml(slide, 1.1, 4.9, 11, 2.0, [
    ("1. 特征 vs 模型: 特征扩展贡献 (+4pp) > 模型替换 (+1.5pp)。"
     "验证了「特征或模型，两者必须有一个优秀」的课程观点。", 15, WHITE, False),
    ("2. 超参敏感性: 学习率是最敏感的超参数（1e-3 最优, 2e-3 震荡, 5e-4 太慢）。"
     "Dropout 和 weight_decay 在合理范围内鲁棒。", 15, WHITE, False),
    ("3. 同等 62 特征下，ResidualMLP vs Ridge 提升约 +1.5pp -> "
     "非线性模型有增益但非万能，特征质量仍是瓶颈。", 15, WHITE, False),
    ("4. 同等 ResidualMLP 下，62 特征 vs 6 特征提升约 +4pp -> "
     "特征扩展是最大的单一贡献因子。", 15, WHITE, False),
])

# ============================================================
# SLIDE 12: 组内贡献度
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "四、组内贡献度评价", "Team Contribution - 重要评分依据")
pn(slide, 12)

tb(slide, 0.8, 1.3, 11.5, 0.35,
   "三人均参与了 数据分析 -> 特征挖掘 -> 模型定义 -> 结果评价 的全部环节。"
   "以下标注每人主导的细分方向，* = 该维度主导者。",
   font_size=14, color=YELLOW)

members = [
    ("刘子彦",
     "模型架构与训练系统",
     ["A类(订单簿) + B类(价差) 共 16 特征：公式推导与全部代码",
      "* nn_model.py 全部代码：ResidualBlock + ResidualMLP 架构",
      "* mdl.py 全部代码：训练管线、早停、checkpoint、分批推理、持久化",
      "* 标签缩放方案 (训练x100/推理/100)，解决梯度消失",
      "GPU/CPU 自动适配 (torch.device)，确保评分环境兼容",
      "建立 Git 协作工作流 + GitHub 远程仓库",
      "撰写 DESIGN.md 方法介绍/模型设计/训练策略章节"]),
    ("顾思豪",
     "特征体系与超参优化",
     ["C类(成交流) + D类(委托撤单) + G类(交互) 共 24 特征：公式推导与全部代码",
      "* 量/笔数/金额三维不平衡设计，区分散户与机构行为",
      "* 滚动操作从 lambda -> Cython 原生路径效率重构",
      "* 主导超参数调优实验 (10+ 组) + 消融实验设计与分析",
      "交互特征方案 (imb*spread, obi*ret 等)",
      "1.py 可视化分析脚本 (预测 vs 真实散点图、误差分布)",
      "撰写 DESIGN.md 特征工程章节"]),
    ("欧阳熠",
     "实验执行与汇报展示",
     ["E类(滚动时序) + F类(截面) 共 21 特征：公式推导与全部代码",
      "* 时序切分验证方案 (最后 15% 日期)，杜绝 look-ahead bias",
      "* RTX 4060 GPU 训练环境部署 + 执行全部训练与对比实验",
      "vol_ratio / ret_ma_accel 等衍生特征设计",
      "meow.py 权重自动加载 + eval.py 预测 CSV 导出",
      "* 课堂汇报 PPT 制作 + 现场演讲 + CONTRIBUTION.md 分工文档",
      "撰写 DESIGN.md 推理与演示/评估结果章节"]),
]
for col, (name, role, items) in enumerate(members):
    left = 0.5 + col * 4.2
    card(slide, left, 1.8, 3.95, 5.2)
    tb(slide, left + 0.25, 1.95, 3.5, 0.35, name,
       font_size=24, bold=True, color=ACCENT)
    tb(slide, left + 0.25, 2.3, 3.5, 0.35, role,
       font_size=13, color=GREEN)
    ml(slide, left + 0.25, 2.75, 3.5, 4.1,
       [(f"+ {item}", 12, WHITE, False) for item in items])

# ============================================================
# SLIDE 13: 大模型辅助（放在最后，为小辅助点）
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "五、大模型辅助说明",
          "AI 作为辅助工具的使用情况（非核心创新，仅辅助效率提升）")
pn(slide, 13)

card(slide, 0.8, 1.5, 11.7, 2.3)
tb(slide, 1.1, 1.65, 11, 0.35,
   "使用方式与范围", font_size=18, bold=True, color=ACCENT)
ml(slide, 1.1, 2.1, 11, 1.5, [
    ("本项目使用 Claude Code 作为辅助工具，参与以下非核心环节：", 15, WHITE, False),
    ("", 4, WHITE, False),
    ("  代码辅助    训练循环样板代码、PyTorch API 调用提示、特征工程的 Cython 优化方案建议", 14, LIGHT, False),
    ("  文档辅助    DESIGN.md / 实验报告 / README 等文档的初稿生成和格式排版（内容经人工审核修改）", 14, LIGHT, False),
    ("  实验辅助    超参数批量实验脚本生成、训练日志批量解析、可视化脚本框架", 14, LIGHT, False),
    ("", 4, WHITE, False),
    ("核心技术决策（特征体系框架、模型架构设计、标签缩放方案、时序验证切分、超参数范围）"
     "均由小组成员讨论决定，AI 不参与任何决策。", 14, YELLOW, False),
])

card(slide, 0.8, 4.1, 11.7, 3.0)
tb(slide, 1.1, 4.25, 11, 0.35,
   "我们的使用范式：AI 提议 -> 人工审核 -> 实验验证", font_size=18, bold=True, color=ACCENT)
ml(slide, 1.1, 4.7, 11, 2.2, [
    ("1. AI 基于市场微观结构文献知识，批量提议候选因子和代码框架（提供广度）", 14, WHITE, False),
    ("2. 人工逐条审核：该因子是否有金融经济学逻辑支撑？过滤纯统计假关联（提供深度）", 14, WHITE, False),
    ("3. 消融实验量化每类因子的边际贡献，客观筛选通过审核且正向贡献的因子（提供验证）", 14, WHITE, False),
    ("", 5, WHITE, False),
    ("通过案例: AI 提议 trade_imb * spread_bps0 -> 人工判断「宽价差时成交方向更可信」逻辑成立 -> 实验证实正向贡献 -> 保留",
     13, GREEN, False),
    ("否决案例: AI 提议部分高阶多项式组合 -> 人工判断缺乏经济学解释且易过拟合 -> 直接否决，不进入实验环节",
     13, RED, False),
    ("", 5, WHITE, False),
    ("启示：大模型在因子挖掘中的价值不在于「自动发现」，而在于加速「假设生成 -> 验证」的迭代循环。"
     "人类提供判断力，实验提供客观标准。", 14, YELLOW, False),
])

# ============================================================
# SLIDE 14: 项目亮点总结
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
title_bar(slide, "项目亮点总结", "Summary")
pn(slide, 14)

highlights = [
    ("系统化特征工程", ACCENT,
     "基于市场微观结构理论构建 7 大类 62 特征体系。\n"
     "多维度覆盖（数量/金额/时序/截面/交互），所有因子有经济学逻辑支撑。\n"
     "Pandas Cython 原生路径优化，700 万行 ~30 秒完成。"),
    ("深度神经网络方案", GREEN,
     "ResidualMLP（GELU + BN + 残差连接 + 递减 Dropout），总参数 ~165K。\n"
     "标签缩放解决梯度消失 + 时序切分杜绝 look-ahead bias + 分批推理保障内存安全。\n"
     "AdamW + ReduceLROnPlateau + EarlyStopping 形成完整训练管线。"),
    ("预测成果达标", ORANGE,
     "Pearson 0.0643，2.6 倍基线提升，达到课程预期 5-10% 区间。\n"
     "消融实验验证所有 7 类特征均有正向贡献，特征扩展是最主要贡献来源。"),
    ("工程完整性", YELLOW,
     "GPU/CPU 自适应、模型权重持久化、演示模式（检测 model_weights.pt + scaler.pkl 存在则跳过训练）。\n"
     "python meow.py 一键运行，满足课程评分要求。\n"
     "AI 全流程辅助开发，实践「提议 -> 审核 -> 验证」的高效协作范式。"),
]
for row, (title, clr, desc) in enumerate(highlights):
    top = 1.5 + row * 1.45
    card(slide, 0.8, top, 11.7, 1.3)
    tb(slide, 1.1, top + 0.1, 4.0, 0.35, title,
       font_size=18, bold=True, color=clr)
    tb(slide, 5.2, top + 0.1, 7.0, 0.95, desc, font_size=14, color=LIGHT)

# ============================================================
# SLIDE 15: 感谢
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])
bg(slide)
tb(slide, 1.2, 2.2, 11, 1.2, "感谢聆听", font_size=72, bold=True,
   color=WHITE, align=PP_ALIGN.CENTER)
line = slide.shapes.add_shape(
    MSO_SHAPE.RECTANGLE, Inches(5.5), Inches(3.6),
    Inches(2.3), Inches(0.05))
line.fill.solid()
line.fill.fore_color.rgb = ACCENT
line.line.fill.background()
tb(slide, 1.2, 4.0, 11, 0.6,
   "MEOW -- 金融高频订单簿分钟级收益率预测",
   font_size=24, color=LIGHT, align=PP_ALIGN.CENTER)
tb(slide, 1.2, 4.7, 11, 0.5,
   "Pearson 0.0643  /  7 大类 62 特征  /  ResidualMLP  /  AI 辅助",
   font_size=16, color=GRAY, align=PP_ALIGN.CENTER)
tb(slide, 1.2, 5.5, 11, 0.4, "欢迎提问",
   font_size=28, color=ACCENT, align=PP_ALIGN.CENTER)

# Save
output_path = "doc/MEOW_汇报.pptx"
prs.save(output_path)
print(f"PPT saved to {output_path}")
