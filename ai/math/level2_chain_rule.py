# 🏰 部落冲突 · AI 数学第 2 关：攻城机器的齿轮组（链式法则）
#
# 📜 剧情：
#   攻城机器工坊里，机器都是一级一级齿轮串起来的：
#   你转动第一个齿轮（输入 w），它带动第二个，第二个再带动第三个……最后输出 y。
#   工坊主想知道：**把 w 拧动一点点，最后的 y 会变多少？**（也就是 y 对 w 的斜率）
#   上一关的测量仪可以量，但太慢了。这一关你要用链式法则**直接算出来**，
#   再用测量仪验货。
#
# 🎯 任务（按顺序做，每做完一个就能跑一次自测）：
#
#   任务 1｜两级齿轮
#       机器已经给你了（见下面代码）：
#           里层 g(w) = 3w + 2      # 输入 w，输出记作 u
#           外层 f(u) = u²          # 输入 u，输出 y
#           整台机器：y = f(g(w))
#       你要写三个函数：
#           def dg(w)       # 返回：里层 g 在 w 处的斜率（手算出公式，写成代码）
#           def df(u)       # 返回：外层 f 在 u 处的斜率（手算出公式，写成代码）
#           def dy_dw(w)    # 返回：整台机器的输出 y 对 w 的斜率
#                           # 必须用链式法则，通过调用 dg 和 df 来算；不许用测量仪
#
#   任务 2｜三级齿轮
#       机器已经给你了：
#           第一级 p(w) = w³         # 输入 w，输出记作 u
#           第二级 q(u) = 2u + 1     # 输入 u，输出记作 v
#           第三级 r(v) = v²         # 输入 v，输出 y
#           整台机器：y = r(q(p(w)))
#       你要写：
#           def dy3_dw(w)   # 返回：这台三级机器的输出 y 对 w 的斜率（链式法则，不许用测量仪）
#
#   任务 3｜城墙造价预测器（这就是线性回归里的一个数据点）
#       建筑大师想用一个公式预测城墙升级的造价：
#           预测造价 = w × x        # x 是城墙等级，w 是「每一级值多少金币」，是你要调的旋钮
#       有一条真实记录：等级 x 的城墙，实际造价是 y。
#           误差 e   = 预测造价 - 实际造价 = w × x - y
#           损失 L   = e²           # 误差的平方：预测得越离谱，损失越大
#       注意：x 和 y 是记录里**固定的数**（常数），能变的只有 w。
#       你要写：
#           def loss(w, x, y)       # 返回：损失 L
#           def dloss_dw(w, x, y)   # 返回：损失 L 对 w 的斜率（链式法则，不许用测量仪）
#
#   任务 4｜找到最准的 w
#       真实记录是：x = 2（2 级城墙），y = 10（造价 10 金币）
#       ws     = 从 0 到 10（两端都包含）、等间距的 101 个候选 w（numpy 数组）
#       best_w = ws 里，让损失 L 对 w 的斜率最接近 0 的那个 w
#                （斜率必须用任务 3 的 dloss_dw 来算）
#
# 📘 知识卡：notes/calculus.md 卡 8～10
# 🚫 你写的函数里不许调用 slope_central、np.gradient、sympy（测量仪只给自测验货用）

#
# 完成日期：2026-11-10 ✅
#   链的结构第一版就全对：每一层的斜率都在它自己的输入处取值（df(g(w))、dr(q(p(w)))），
#   卡 9 的坑一个没踩；任务 3（线性回归单个数据点的斜率）、任务 4 一次通过
#   Claude 指出的问题：第一版 dg、df 用了测量仪（题目要求手算公式）；dp、dq、dr 没定义
#   用到的已推导知识：D20；新推出 D21、D22（notes/derived.md）

import numpy as np


# ---------- 已经给你的东西（不用改） ----------

def slope_central(f, x, h=1e-5):      # 上一关学到的标准测量仪（中心差分）
    return (f(x + h) - f(x - h)) / (2 * h)

def g(w): return 3 * w + 2            # 任务 1 的里层
def f(u): return u ** 2               # 任务 1 的外层

def p(w): return w ** 3               # 任务 2 的第一级
def q(u): return 2 * u + 1            # 任务 2 的第二级
def r(v): return v ** 2               # 任务 2 的第三级


# ---------- 自己写的版本 ----------

# 任务 1
def dg(w): return 3

def df(u): return 2 * u

def dy_dw(w):
    return dg(w) * df(g(w))


# 任务 2
def dp(w): return 3 * (w ** 2)
def dq(u): return 2
def dr(v): return 2 * v

def dy3_dw(w):
    return dp(w) * dq(p(w)) * dr(q(p(w)))


# 任务 3
def loss(w, x, y):
    return (w * x - y) ** 2

def dloss_dw(w, x, y):
    return 2 * x * (w * x - y)


# 任务 4
ws = np.linspace(0,10,101)
best_w = ws[np.argmin(np.abs(dloss_dw(ws,2,10)))]


# ⬇⬇⬇ 自测（不用改）⬇⬇⬇
test_w = np.array([-2.0, -0.5, 0.0, 1.0, 3.5])     # 用来验货的几个 w

# 任务 1
assert np.allclose(dg(test_w), slope_central(g, test_w), atol=1e-4), "dg 和测量仪量出来的对不上"
assert np.allclose(df(test_w), slope_central(f, test_w), atol=1e-4), "df 和测量仪量出来的对不上"
truth1 = slope_central(lambda w: f(g(w)), test_w)
assert np.allclose(dy_dw(test_w), truth1, atol=1e-4), f"dy_dw 和测量仪对不上：你的 {dy_dw(test_w)}，测量仪 {truth1}"
print("✅ 任务 1 两级齿轮")

# 任务 2
truth2 = slope_central(lambda w: r(q(p(w))), test_w)
assert np.allclose(dy3_dw(test_w), truth2, rtol=1e-5, atol=1e-4), f"dy3_dw 和测量仪对不上：你的 {dy3_dw(test_w)}，测量仪 {truth2}"
print("✅ 任务 2 三级齿轮")

# 任务 3
assert abs(loss(3, 2, 10) - 16) < 1e-12, "loss 写错了：w=3, x=2, y=10 时预测 6，误差 -4，损失应该是 16"
assert abs(loss(5, 2, 10)) < 1e-12, "loss 写错了：预测完全正确时损失应该是 0"
for x0, y0 in [(2, 10), (3, -4), (-1.5, 6)]:
    truth3 = slope_central(lambda w: loss(w, x0, y0), test_w)
    assert np.allclose(dloss_dw(test_w, x0, y0), truth3, atol=1e-4), f"x={x0}, y={y0} 时 dloss_dw 和测量仪对不上：你的 {dloss_dw(test_w, x0, y0)}，测量仪 {truth3}"
print("✅ 任务 3 城墙造价预测器")

# 任务 4
assert isinstance(ws, np.ndarray) and ws.shape == (101,), "ws 要有 101 个点"
assert ws[0] == 0 and ws[-1] == 10, "ws 要从 0 开始、到 10 结束（两端都包含）"
assert np.any(np.isclose(ws, best_w)), "best_w 要是 ws 里的某一个点"
assert abs(dloss_dw(best_w, 2, 10)) <= np.abs(dloss_dw(ws, 2, 10)).min() + 1e-12, "best_w 不是斜率最接近 0 的那个 w"
assert loss(best_w, 2, 10) < 1e-9, "best_w 的损失不是最小"
print("✅ 任务 4 找到最准的 w")
print(f"🎉 数学第 2 关「攻城机器的齿轮组」通关！机器自己发现了：每一级城墙值 {best_w:g} 金币")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================
# 思路一样，区别只有一点：先走一趟前向，把每一级的输出存进变量（u、v），
# 反向那一趟直接用存好的值。上面自己写的版本里 p(w) 被算了 3 次、q(p(w)) 算了 1 次；
# 层数一多，重复计算会爆炸。「前向时把中间值存下来」正是反向传播的做法。

def dy3_dw_std(w):
    # 前向：从里到外算出每一级的输出
    u = p(w)                  # 第一级的输出
    v = q(u)                  # 第二级的输出
    # 反向：从外到里，每一级的斜率在它自己的输入处取值
    dy_dv = 2 * v             # 第三级 r(v) = v²    在 v 处的斜率
    dv_du = 2                 # 第二级 q(u) = 2u+1  在 u 处的斜率
    du_dw = 3 * w ** 2        # 第一级 p(w) = w³    在 w 处的斜率
    return dy_dv * dv_du * du_dw


def dloss_dw_std(w, x, y):
    pred = w * x              # 前向：预测造价
    e = pred - y              # 前向：误差
    dL_de = 2 * e             # 外层 L = e²        在 e 处的斜率
    de_dw = x                 # 里层 e = w·x - y   在 w 处的斜率（x、y 是常数）
    return dL_de * de_dw      # = 2 · (w·x - y) · x


assert np.allclose(dy3_dw_std(test_w), dy3_dw(test_w))
assert np.allclose(dloss_dw_std(test_w, 2, 10), dloss_dw(test_w, 2, 10))
print("标准写法也通过 ✅")
