# 🏰 部落冲突 · AI 数学第 4 关：谷底行军（梯度下降）
#
# 📜 剧情：
#   前三关你造好了三样东西：量坡度的测量仪、链式法则、整本账本的梯度 grad_mse。
#   但到现在为止，旋钮都是你自己看着梯度的正负「判断」该往哪拧。
#   建筑大师下令：别再手拧了，让预测器**自己**一步一步走到谷底。
#   这一关结束时，你会得到第一个完全手写、自己训练出来的模型：
#       预测造价 = w × x + b      # x 是城墙等级；w 是每一级的单价；b 是开工费
#   这一关把两个旋钮装进一个 numpy 数组：params = [w, b]（写法习惯 H9）
#
# 🎯 任务（按顺序做，每做完一个就能跑一次自测）：
#
#   任务 1｜迈一步
#       def step(params, grad, lr)
#           # params：当前位置，numpy 数组（装着所有旋钮，个数任意）
#           # grad  ：损失在 params 处的梯度，numpy 数组，和 params 同形状
#           # lr    ：学习率，一个正数
#           # 返回：走完一步梯度下降之后的新位置，numpy 数组，和 params 同形状
#           # 要求：不许改动传进来的 params 数组本身
#
#   任务 2｜单旋钮下山（回到第 1 关的山谷）
#       山谷已经给你了：L(w) = (w - 4)² + 1
#       def dL(w)
#           # 返回：L 在 w 处的斜率（手算出公式，写成代码）
#       def descend_1d(df, w0, lr, n_steps)
#           # df     ：一个函数，df(w) 返回山谷在 w 处的斜率
#           # w0     ：出发位置，一个数
#           # lr     ：学习率
#           # n_steps：一共走多少步
#           # 返回：走过的全部位置，numpy 数组，形状 (n_steps + 1,)
#           #       第 0 个元素是出发位置 w0，第 k 个元素是走完第 k 步之后的位置
#
#   任务 3｜三种学习率，三种命运
#       在山谷 L 里从 w0 = 0 出发，各走 20 步，分别用三种学习率：0.1、1.0、1.1
#       观察三条路径，各填一个字符串：
#           "converge"  ——  越来越靠近谷底
#           "bounce"    ——  在几个位置之间来回跳，既不靠近也不远离
#           "explode"   ——  离谷底越来越远
#       fate_01 = lr 为 0.1 时的命运
#       fate_10 = lr 为 1.0 时的命运
#       fate_11 = lr 为 1.1 时的命运
#
#   任务 4｜训练造价预测器
#       账本 xs、ys，损失函数 mse(params, xs, ys)，梯度函数 grad_mse(params, xs, ys) 都已经给你了
#       def train(xs, ys, lr, n_steps)
#           # 从 params = [0.0, 0.0] 出发，对均方误差做 n_steps 步梯度下降
#           # 返回两样东西：(params, losses)
#           #   params：训练结束时的位置，numpy 数组，形状 (2,)，即 [w, b]
#           #   losses：损失的记录，长度 n_steps + 1
#           #           第 0 个是出发时（一步都没走）的损失，第 k 个是走完第 k 步之后的损失
#       然后用 lr = 0.05、n_steps = 2000 训练一次，结果存进：
#           trained, losses = train(xs, ys, 0.05, 2000)
#
#   任务 5｜用模型预测
#       def predict(params, x)
#           # params：[w, b]
#           # x     ：城墙等级，可以是一个数，也可以是 numpy 数组
#           # 返回：预测造价（x 是数组时返回等长的数组）
#       cost_lv8 = 用任务 4 训练出的 trained，预测 8 级城墙的造价（账本里没有 8 级）
#
# 📘 知识卡：notes/calculus.md 卡 15～17
# 🚫 不许用 np.polyfit、np.linalg.lstsq、sklearn 等现成的拟合工具

import numpy as np


# ---------- 已经给你的东西（不用改） ----------

def L(w): return (w - 4) ** 2 + 1                     # 任务 2、3 的山谷

xs = np.array([1.0, 2.0, 3.0, 4.0, 5.0])              # 账本：5 个城墙等级
ys = np.array([25.0, 30.0, 35.0, 40.0, 45.0])         # 账本：对应的 5 个实际造价

def mse(params, xs, ys):
    """均方误差。params = [w, b]。"""
    errs = params[0] * xs + params[1] - ys             # 每条记录的误差
    return np.mean(errs ** 2)

def grad_mse(params, xs, ys):
    """均方误差在 params 处的梯度（就是你第 3 关推出来的 D24），形状 (2,)。"""
    errs = params[0] * xs + params[1] - ys
    return np.array([np.mean(2 * errs * xs), np.mean(2 * errs)])


# ---------- 自己写的版本 ----------

# 任务 1
def step(params, grad, lr):
    ...


# 任务 2
def dL(w):
    ...

def descend_1d(df, w0, lr, n_steps):
    ...


# 任务 3
fate_01 = ...
fate_10 = ...
fate_11 = ...


# 任务 4
def train(xs, ys, lr, n_steps):
    ...

trained, losses = ..., ...


# 任务 5
def predict(params, x):
    ...

cost_lv8 = ...


# ⬇⬇⬇ 自测（不用改）⬇⬇⬇

# 任务 1
_p = np.array([1.0, -2.0, 3.0])
_out = step(_p, np.array([10.0, 0.0, -4.0]), 0.5)
assert isinstance(_out, np.ndarray) and _out.shape == (3,), "step 要返回和 params 同形状的 numpy 数组"
assert np.allclose(_out, [-4.0, -2.0, 5.0]), f"step 走错了：你的 {_out}，应该是 [-4. -2.  5.]"
assert np.allclose(_p, [1.0, -2.0, 3.0]), "step 把传进来的 params 改掉了，要返回一个新数组"
assert np.allclose(step(np.array([0.0, 0.0]), np.array([-230.0, -70.0]), 0.01), [2.3, 0.7]), "step 在两个旋钮的情况下不对"
print("✅ 任务 1 迈一步")

# 任务 2
for _w in [0.0, 4.0, 7.5, -3.0]:
    _want = (L(_w + 1e-5) - L(_w - 1e-5)) / 2e-5
    assert abs(dL(_w) - _want) < 1e-4, f"dL 在 w={_w} 处不对：你的 {dL(_w)}，测量仪 {_want:.4f}"
_path = descend_1d(dL, 0.0, 0.1, 3)
assert isinstance(_path, np.ndarray) and _path.shape == (4,), "descend_1d 走 3 步要返回形状 (4,) 的 numpy 数组（含出发位置）"
assert np.allclose(_path, [0.0, 0.8, 1.44, 1.952]), f"descend_1d 路径不对：你的 {_path}，应该是 [0. 0.8 1.44 1.952]"
_path = descend_1d(lambda w: 2 * w, 10.0, 0.25, 5)
assert np.allclose(_path, [10.0, 5.0, 2.5, 1.25, 0.625, 0.3125]), f"换一个山谷后 descend_1d 不对：你的 {_path}"
assert descend_1d(dL, 3.0, 0.1, 0).shape == (1,), "走 0 步时路径里应该只有出发位置"
print("✅ 任务 2 单旋钮下山")

# 任务 3
_fates = ("converge", "bounce", "explode")
assert fate_01 in _fates and fate_10 in _fates and fate_11 in _fates, '只能填 "converge"、"bounce" 或 "explode"'
def _fate(lr):
    d = np.abs(descend_1d(dL, 0.0, lr, 20) - 4)        # 每一步离谷底 w = 4 的距离
    return "converge" if d[-1] < d[0] - 1e-9 else ("explode" if d[-1] > d[0] + 1e-9 else "bounce")
assert fate_01 == _fate(0.1), "lr = 0.1 的命运不对，把路径 print 出来看看"
assert fate_10 == _fate(1.0), "lr = 1.0 的命运不对，把路径 print 出来看看"
assert fate_11 == _fate(1.1), "lr = 1.1 的命运不对，把路径 print 出来看看"
print("✅ 任务 3 三种学习率，三种命运")

# 任务 4
_p1, _l1 = train(xs, ys, 0.01, 1)
assert isinstance(_p1, np.ndarray) and _p1.shape == (2,), "train 返回的 params 要是形状 (2,) 的 numpy 数组"
assert len(_l1) == 2, "走 1 步时 losses 里应该有 2 个数（出发时 + 走完第 1 步）"
assert abs(_l1[0] - 1275) < 1e-9, f"losses 第 0 个应该是出发点 [0, 0] 的损失 1275，你的是 {_l1[0]}"
assert np.allclose(_p1, [2.3, 0.7]), f"从 [0, 0] 用 lr=0.01 走 1 步应该到 [2.3 0.7]，你的是 {_p1}"
assert abs(_l1[1] - mse(np.array([2.3, 0.7]), xs, ys)) < 1e-9, "losses 第 1 个应该是走完第 1 步之后那个位置的损失"
_p2, _l2 = train(xs, ys, 0.01, 50)
assert len(_l2) == 51 and all(_l2[k + 1] < _l2[k] for k in range(50)), "lr=0.01 时损失应该每一步都在下降"
assert np.allclose(train(xs, ys, 0.01, 50)[0], _p2), "连续调用两次 train 结果不一样：每次都要从 [0, 0] 重新出发"
assert isinstance(trained, np.ndarray) and len(losses) == 2001, "trained, losses 要来自 train(xs, ys, 0.05, 2000)"
assert np.allclose(trained, [5.0, 20.0], atol=1e-3), f"训练结果不对：你的 {trained}，账本的真实规律是 w = 5、b = 20"
assert losses[-1] < 1e-6, f"训练结束时损失应该接近 0，你的是 {losses[-1]}"
print(f"✅ 任务 4 训练造价预测器（w = {trained[0]:.4f}，b = {trained[1]:.4f}，损失 {losses[0]:.0f} → {losses[-1]:.2e}）")

# 任务 5
assert abs(predict(np.array([2.0, 1.0]), 3.0) - 7.0) < 1e-9, "predict 不对：w=2、b=1 时，等级 3 的预测应该是 7"
assert np.allclose(predict(np.array([2.0, 1.0]), np.array([0.0, 1.0, 10.0])), [1.0, 3.0, 21.0]), "predict 要支持 x 是 numpy 数组"
assert np.allclose(predict(trained, xs), ys, atol=1e-2), "用 trained 预测账本里的 5 个等级，应该和实际造价几乎一样"
assert abs(cost_lv8 - 60) < 1e-2, f"8 级城墙的预测造价不对：你的 {cost_lv8}"
print("✅ 任务 5 用模型预测")
print("🎉 数学第 4 关「谷底行军」通关！你训练出了第一个手写模型！")
