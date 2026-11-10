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
#   任务 3｜地形扫描
#       写出地形函数 def L(w)
#       ws     = 从 0 到 8（两端都包含）、等间距的 81 个位置（numpy 数组）
#       slopes = ws 里每个位置的斜率（numpy 数组，长度 81）
#
#   任务 4｜找到谷底
#       best_w = ws 里斜率最接近 0 的那个位置
#
#   任务 5｜下山方向
#       direction_if_positive = 站在一个斜率为正的地方，想往低处走，
#                               应该往 "left"（w 变小）还是 "right"（w 变大）？
#
# 📘 知识卡：notes/calculus.md 卡 1～6
# 🚫 不许用 np.gradient、sympy 等现成的求导工具

import numpy as np


# 任务 1
def slope(f, x, h=1e-5):
    ...


# 任务 2
s3 = ...
s3_rule = ...


# 任务 3
def L(w):
    ...

ws = ...
slopes = ...


# 任务 4
best_w = ...


# 任务 5
direction_if_positive = ...


# ⬇⬇⬇ 自测（不用改）⬇⬇⬇
import numpy as np

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
