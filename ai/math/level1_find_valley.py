# 🏰 部落冲突 · AI 数学第 1 关：寻找谷底（导数 = 斜率）
#
# 📜 剧情：
#   你的部落要在一片起伏的山谷里建新村庄，村庄要建在**谷底**（最低点），
#   这样防御塔能俯视四周。可是起了大雾，你看不到整片地形，
#   只有一台「坡度测量仪」：站在某个位置，它能告诉你脚下的坡有多陡。
#   山谷的高度由地形函数给出：
#       L(w) = (w - 4)² + 1        # w 是位置，L(w) 是那里的海拔
#
# 🎯 任务（按顺序做，每做完一个就能跑一次自测）：
#
#   任务 1｜造测量仪
#       def slope(f, x, h=1e-5)
#           # 用数值导数公式算函数 f 在 x 处的斜率并返回
#           # f 是一个函数（当参数传进来），h 是很小的步长
#           # 要求：x 是单个数时返回一个数；x 是 numpy 数组时，一次性返回同样形状的数组
#           #       （不许写 for 循环）
#
#   任务 2｜两种方法对答案
#       s3      = 用 slope 算出的 f(x) = x² 在 x = 3 处的斜率
#       s3_rule = 用幂函数求导规则**手算**出的同一个斜率（直接写数字）
#
#   任务 3｜地形扫描（分三步，每个变量各管一件事）
#
#       3a. 地形函数 L
#           def L(w)
#               # 输入：位置 w（可以是一个数，也可以是 numpy 数组）
#               # 返回：该位置的海拔，即 (w - 4)² + 1
#               # 例：L(4) 应该是 1，L(0) 应该是 17
#
#       3b. 测量点 ws
#           ws = 一个 numpy 数组，存放要测量的 81 个位置
#               # 第 1 个位置是 0，最后 1 个位置是 8
#               # 相邻两个位置之间的间隔全部相等
#
#       3c. 每个测量点的坡度 slopes
#           slopes = 一个 numpy 数组，长度和 ws 一样（81）
#               # slopes[i] = 地形函数 L 在位置 ws[i] 处的斜率
#               # 必须用任务 1 造的 slope 来算，不许写 for 循环
#
#   任务 4｜找到谷底
#       best_w = ws 里斜率最接近 0 的那个位置
#
#   任务 5｜下山方向
#       direction_if_positive = 站在一个斜率为正的地方，想往低处走，
#                               应该往 "left"（w 变小）还是 "right"（w 变大）？
#
# 📘 知识卡：notes/calculus.md 卡 1～7
# 🚫 不许用 np.gradient、sympy 等现成的求导工具

#
# 完成日期：2026-11-09 ✅
#   slope（前向差分 + 广播自动支持数组）一次写对；任务 5 下山方向一次答对
#   Claude 指出的问题：任务 2 一开始测成了 L 而不是 x²；ws 终点写成 1；
#   best_w 先对 ws 取了绝对值（应该是 slopes），再是 argmin 拿到下标后没回 ws 取值；
#   变量名 direction_if_positive 拼错
#   用到的已推导知识：D6 广播；新推出 D19、D20（notes/derived.md）

import numpy as np


# 任务 1
def slope(f, x, h=1e-5):
    return (f(x + h) -f(x)) / h


# 任务 2
s3 = slope(lambda w:w*w,3)

s3_rule = 6

print(s3)

print(s3_rule)


# 任务 3
def L(w):
    return (w - 4) * (w - 4) + 1

ws = np.linspace(0,8,81)

slopes = slope(L,ws)


# 任务 4
best_w = ws[np.argmin(np.abs(slopes))]


# 任务 5
direction_if_positive = "left"


# ⬇⬇⬇ 自测 ⬇⬇⬇

# 任务 1
assert abs(slope(lambda x: x ** 3, 2) - 12) < 1e-3, "slope 对单个数不对"
out = slope(lambda x: x ** 2, np.array([0.0, 1.0, 2.0]))
assert isinstance(out, np.ndarray) and out.shape == (3,), "slope 要能直接吃整个数组，返回同样形状的数组"
assert np.allclose(out, [0, 2, 4], atol=1e-3), "slope 对数组不对"
print("✅ 任务 1 测量仪")

# 任务 2
assert abs(s3 - s3_rule) < 1e-3, f"数值结果 {s3} 和你手算的 {s3_rule} 对不上"
print("✅ 任务 2 两种方法对答案")

# 任务 3
assert isinstance(ws, np.ndarray) and ws.shape == (81,), "ws 要有 81 个点"
assert ws[0] == 0 and ws[-1] == 8, "ws 要从 0 开始、到 8 结束（两端都包含）"
assert np.allclose(np.diff(ws), ws[1] - ws[0]), "ws 要等间距"
assert abs(L(4) - 1) < 1e-12 and abs(L(0) - 17) < 1e-12, "L 写错了"
assert isinstance(slopes, np.ndarray) and slopes.shape == (81,), "slopes 要和 ws 一样长"
assert np.allclose(slopes, slope(L, ws)), "slopes 要用 slope 算"
print("✅ 任务 3 地形扫描")

# 任务 4
assert np.any(np.isclose(ws, best_w)), "best_w 要是 ws 里的某一个点"
assert abs(slope(L, best_w)) <= np.abs(slopes).min() + 1e-12, "best_w 不是斜率最接近 0 的那个 w"
assert abs(L(best_w) - L(ws).min()) < 1e-9, "best_w 不在谷底"
print("✅ 任务 4 找到谷底")

# 任务 5
assert direction_if_positive in ("left", "right"), '只能是 "left" 或 "right"'
w0 = 6.0                      # 站在一个斜率为正的地方
assert slope(L, w0) > 0
step = -0.1 if direction_if_positive == "left" else 0.1
assert L(w0 + step) < L(w0), "往这个方向走，L 变大了，是在上坡"
print("✅ 任务 5 下山方向")
print("🎉 数学第 1 关「寻找谷底」通关！")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

def slope_central(f, x, h=1e-5):
    """中心差分：左右各走 h，再除以两点的横向距离 2h。
    前向差分（上面自己写的）误差和 h 成正比；中心差分误差和 h² 成正比，
    同样的 h 准确得多。深度学习里检查反向传播是否写对（gradient check）用的就是它。"""
    return (f(x + h) - f(x - h)) / (2 * h)


def L_std(w):
    return (w - 4) ** 2 + 1                  # 平方直接写 ** 2


ws_std = np.linspace(0, 8, 81)               # 起点、终点、点数；两端都包含
slopes_std = slope_central(L_std, ws_std)    # 广播：一次算完 81 个位置
best_w_std = ws_std[np.argmin(np.abs(slopes_std))]   # 在 slopes 里找下标 → 去 ws 里取位置

# 对比两种差分在 x² 的 x = 3 处的误差（精确值是 6）
err_forward = abs(slope(lambda x: x ** 2, 3) - 6)            # 约 1e-5，和 h 一样大
err_central = abs(slope_central(lambda x: x ** 2, 3) - 6)    # 约 1e-10 或更小
assert err_central < err_forward / 1000
assert np.isclose(best_w_std, 4.0)
print(f"前向差分误差 {err_forward:.1e}，中心差分误差 {err_central:.1e}")
print("标准写法也通过 ✅")
