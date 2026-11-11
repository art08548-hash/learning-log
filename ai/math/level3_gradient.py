# 🏰 部落冲突 · AI 数学第 3 关：双旋钮校准（偏导数与梯度）
#
# 📜 剧情：
#   上一关的造价预测器只有一个旋钮 w。建筑大师发现它不够准：
#   每次升级城墙，除了「每一级值多少金币」，还要先交一笔固定的**开工费**。
#   于是预测公式升级成两个旋钮：
#       预测造价 = w × x + b      # x 是城墙等级；w 是每一级的单价；b 是开工费
#   现在损失 L 同时取决于 w 和 b 两个旋钮，地形从一条山路变成了一整片山地。
#   「斜率」不再是一个数，而是**每个旋钮各一个**，合起来叫梯度。
#   （这一关所有函数里的 w、b 都是单个数，不用支持数组）
#
# 🎯 任务（按顺序做，每做完一个就能跑一次自测）：
#
#   任务 1｜双旋钮测量仪
#       def numeric_grad(f, w, b, h=1e-5)
#           # f 是一个吃两个数的函数，调用方式是 f(w, b)，返回一个数
#           # 返回：f 在点 (w, b) 处的梯度，numpy 数组，形状 (2,)
#           #       第 0 个元素 = f 对 w 的偏导数（数值近似）
#           #       第 1 个元素 = f 对 b 的偏导数（数值近似）
#
#   任务 2｜手算偏导
#       地形函数已经给你了：T(w, b) = w² + 3wb + b³
#           def dT_dw(w, b)     # 返回：T 对 w 的偏导数（手算出公式，写成代码）
#           def dT_db(w, b)     # 返回：T 对 b 的偏导数（手算出公式，写成代码）
#
#   任务 3｜一条记录的梯度
#       一条真实记录：等级 x 的城墙，实际造价 y（x、y 是固定的数）
#           误差 e = w × x + b - y
#           损失 L = e²
#       def grad_one(w, b, x, y)
#           # 返回：损失 L 在点 (w, b) 处的梯度，numpy 数组，形状 (2,)
#           #       第 0 个元素 = L 对 w 的偏导数，第 1 个元素 = L 对 b 的偏导数
#           # 手算公式，不许用测量仪
#
#   任务 4｜整本账本的梯度
#       账本里有 5 条记录，已经给你了：xs 是 5 个等级，ys 是对应的 5 个实际造价
#       整本账本的损失 = 5 条记录各自损失的**平均值**（这叫均方误差，见卡 14）
#       def mse(w, b, xs, ys)
#           # xs、ys 是等长的 numpy 数组
#           # 返回：均方误差，一个数
#       def grad_mse(w, b, xs, ys)
#           # 返回：均方误差在点 (w, b) 处的梯度，numpy 数组，形状 (2,)
#           # 手算公式，不许用测量仪，不许写 for 循环
#
#   任务 5｜两个旋钮各往哪拧
#       站在起点 (w, b) = (0, 0)，账本用上面的 xs、ys：
#       g0       = 均方误差在起点处的梯度（用 grad_mse 算）
#       w_should = 想让损失变小，旋钮 w 应该 "increase"（调大）还是 "decrease"（调小）？
#       b_should = 想让损失变小，旋钮 b 应该 "increase" 还是 "decrease"？
#
# 📘 知识卡：notes/calculus.md 卡 11～14
# 🚫 任务 2～4 你写的函数里不许调用 numeric_grad、np.gradient、sympy

#
# 完成日期：2026-11-11 ✅
#   任务 2 的两个偏导数、mse、任务 3 的两个公式、任务 5 的方向全部一次推对；
#   测量仪直接用了上一关学的中心差分
#   Claude 指出的问题：numeric_grad 少了括号（先乘除后加减，/ 2 * h 是除以 2 再乘 h）；
#   grad_mse 第 0 个分量把 xs 乘在了 np.mean 外面（应该先乘再平均）；返回了列表而不是 numpy 数组
#   学卡 13 时自己追问并推出 D23；用到 D6、D19、D21、D22；新推出 D24（notes/derived.md）

import numpy as np


# ---------- 已经给你的东西（不用改） ----------

def T(w, b): return w ** 2 + 3 * w * b + b ** 3      # 任务 2 的地形

xs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])             # 账本：5 个城墙等级
ys = np.array([25.0, 30.0, 35.0, 40.0, 45.0])        # 账本：对应的 5 个实际造价


# ---------- 自己写的版本 ----------

# 任务 1
def numeric_grad(f, w, b, h=1e-5):
    return np.array([(f(w + h,b) - f(w - h,b)) / (2 * h),(f(w,b + h) - f(w,b - h)) / (2 * h)])


# 任务 2
def dT_dw(w, b):
    return 2 * w + 3 * b

def dT_db(w, b):
    return 3 * b ** 2 + 3 * w


# 任务 3
def grad_one(w, b, x, y):
    return np.array([(w * x + b - y) * 2 * x,(w * x + b - y) * 2])


# 任务 4
def mse(w, b, xs, ys):
    return np.mean((w * xs + b - ys) ** 2)

def grad_mse(w, b, xs, ys):
    return np.array([np.mean((w * xs + b - ys) * xs) * 2,np.mean(w * xs + b -ys) * 2])


# 任务 5
g0 = grad_mse(0,0,xs,ys)
w_should = "increase"
b_should = "increase"


# ⬇⬇⬇ 自测（不用改）⬇⬇⬇
def _ref(f, w, b, h=1e-5):            # 自测自带的验货仪
    return np.array([(f(w + h, b) - f(w - h, b)) / (2 * h),
                     (f(w, b + h) - f(w, b - h)) / (2 * h)])

_points = [(0.0, 0.0), (1.0, 2.0), (-2.0, 0.5), (3.5, -1.0)]     # 用来验货的几个 (w, b)

# 任务 1
_f = lambda w, b: w ** 2 * b + 5 * b
out = numeric_grad(_f, 2.0, 1.0)
assert isinstance(out, np.ndarray) and out.shape == (2,), "numeric_grad 要返回形状 (2,) 的 numpy 数组"
for w0, b0 in _points:
    assert np.allclose(numeric_grad(_f, w0, b0), _ref(_f, w0, b0), atol=1e-3), f"numeric_grad 在 ({w0}, {b0}) 处不对：你的 {numeric_grad(_f, w0, b0)}，应该约为 {_ref(_f, w0, b0)}"
print("✅ 任务 1 双旋钮测量仪")

# 任务 2
for w0, b0 in _points:
    want = _ref(T, w0, b0)
    assert abs(dT_dw(w0, b0) - want[0]) < 1e-4, f"dT_dw 在 ({w0}, {b0}) 处不对：你的 {dT_dw(w0, b0)}，验货仪 {want[0]:.4f}"
    assert abs(dT_db(w0, b0) - want[1]) < 1e-4, f"dT_db 在 ({w0}, {b0}) 处不对：你的 {dT_db(w0, b0)}，验货仪 {want[1]:.4f}"
print("✅ 任务 2 手算偏导")

# 任务 3
out = grad_one(1.0, 2.0, 3.0, 4.0)
assert isinstance(out, np.ndarray) and out.shape == (2,), "grad_one 要返回形状 (2,) 的 numpy 数组"
for x0, y0 in [(2.0, 10.0), (3.0, -4.0), (-1.5, 6.0)]:
    for w0, b0 in _points:
        want = _ref(lambda w, b: (w * x0 + b - y0) ** 2, w0, b0)
        assert np.allclose(grad_one(w0, b0, x0, y0), want, atol=1e-4), f"x={x0}, y={y0}，点 ({w0}, {b0}) 处 grad_one 不对：你的 {grad_one(w0, b0, x0, y0)}，验货仪 {want}"
print("✅ 任务 3 一条记录的梯度")

# 任务 4
assert abs(mse(0, 0, xs, ys) - 1275) < 1e-9, "mse 写错了：w=0, b=0 时每条预测都是 0，均方误差应该是 1275"
assert abs(mse(5, 20, xs, ys)) < 1e-12, "mse 写错了：w=5, b=20 时每条都预测正确，均方误差应该是 0"
out = grad_mse(1.0, 2.0, xs, ys)
assert isinstance(out, np.ndarray) and out.shape == (2,), "grad_mse 要返回形状 (2,) 的 numpy 数组"
for w0, b0 in _points + [(5.0, 20.0)]:
    want = _ref(lambda w, b: np.mean((w * xs + b - ys) ** 2), w0, b0)
    assert np.allclose(grad_mse(w0, b0, xs, ys), want, atol=1e-4), f"点 ({w0}, {b0}) 处 grad_mse 不对：你的 {grad_mse(w0, b0, xs, ys)}，验货仪 {want}"
print("✅ 任务 4 整本账本的梯度")

# 任务 5
assert np.allclose(g0, grad_mse(0, 0, xs, ys)), "g0 要是起点 (0, 0) 处的梯度"
assert w_should in ("increase", "decrease") and b_should in ("increase", "decrease"), '只能是 "increase" 或 "decrease"'
dw = 0.01 if w_should == "increase" else -0.01
db = 0.01 if b_should == "increase" else -0.01
assert mse(0 + dw, 0, xs, ys) < mse(0, 0, xs, ys), "按你说的方向拧 w，损失变大了"
assert mse(0, 0 + db, xs, ys) < mse(0, 0, xs, ys), "按你说的方向拧 b，损失变大了"
print("✅ 任务 5 两个旋钮各往哪拧")
print("🎉 数学第 3 关「双旋钮校准」通关！")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

def grad_mse_std(w, b, xs, ys):
    """误差只算一次，存进变量 errs，两个偏导数都用它。"""
    errs = w * xs + b - ys                   # 每条记录的误差，数组，和 xs 等长
    dL_dw = np.mean(2 * errs * xs)           # 每条记录「2 × 误差 × 输入」的平均
    dL_db = np.mean(2 * errs)                # 每条记录「2 × 误差」的平均
    return np.array([dL_dw, dL_db])


def numeric_grad_std(f, params, h=1e-5):
    """旋钮个数任意的测量仪：params 是装着所有旋钮的 numpy 数组，f 吃这个数组、返回一个数。
    一次只挪动一个旋钮，其余保持原样。深度学习里的 gradient check 就是这个函数。"""
    grad = np.zeros_like(params, dtype=float)      # 和 params 同形状的全 0 数组，用来装结果
    for i in range(params.size):                   # 逐个旋钮量
        step = np.zeros_like(params, dtype=float)
        step[i] = h                                # 只有第 i 个旋钮挪动 h
        grad[i] = (f(params + step) - f(params - step)) / (2 * h)
    return grad


assert np.allclose(grad_mse_std(1.0, 2.0, xs, ys), grad_mse(1.0, 2.0, xs, ys))
_loss = lambda params: np.mean((params[0] * xs + params[1] - ys) ** 2)     # params = [w, b]
assert np.allclose(numeric_grad_std(_loss, np.array([1.0, 2.0])), grad_mse(1.0, 2.0, xs, ys), atol=1e-4)
print("标准写法也通过 ✅（手算梯度和测量仪一致 = gradient check 通过）")
