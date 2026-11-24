# 🏰 部落冲突 · 线性回归第 1 关：大本营的造价账本（多特征线性回归）
#
# 📜 剧情：
#   上一关的账本太理想了：5 条记录、只有 1 个特征、每条都恰好落在一条直线上。
#   这次建筑大师翻出了部落 200 次城墙升级的真实账本，每次升级记了 3 个特征：
#       第 0 列：城墙等级（1～15）
#       第 1 列：这次升级的城墙段数（50～300）
#       第 2 列：当时的大本营等级（1～16）
#   造价还会受天气、工人心情影响，账本里的数字**带着噪声**，不会精确落在任何公式上。
#   你的任务：从零训练一个多特征的造价预测器，再把它学到的规律翻译成人话。
#
# 🎯 每个任务的说明就写在要实现的位置正上方，按顺序做，每做完一个就能跑一次自测
#
# 📘 知识卡：notes/linear_regression.md 卡 1～4
# 🚫 不许用 np.polyfit、np.linalg.lstsq、np.linalg.solve、sklearn 等现成的拟合工具
# 🚫 除了 train 里那个「走 n_steps 步」的循环，其他地方不许写 for 循环
#
# 进度：2026-11-19 任务 1、2 ✅，2026-11-20 任务 3 ✅，2026-11-21 任务 4 ✅，2026-11-23 任务 5 ✅（任务 6 未做）
#   predict 用 X * w 再按 axis=1 求和；grad 里 u 是每条记录的 2 × 误差
#   grad 第一版 u 形状 (n,) 直接乘 X，广播把它当成「行」去对齐最后一维 → 形状错；
#   第二版乘了元组 (n, 1) 而不是变形后的 u；第三版 u.reshape(n, 1) 通过
#   2026-11-20 任务 3 standardize ✅：第一版用 keepdims 只返回 Xs，改成返回 (Xs, mean, std) 且形状 (d,)
#   2026-11-21 任务 4 ✅ 一次写对：train 复用 grad；三种命运全对；损失 13918 → 8.05（第 100 步就到底）
#     can_reach_zero 是真的跑了 100 万步去验证（约 40 秒）；Claude 建议：用「噪声」推出来更快，且 True if … else False 直接写条件（H12）
#   2026-11-23 任务 5 ✅：第一版直接拿原始 X_new 乘 w_std（预测 3561、912，大了二三十倍）；
#     第二、三版用 standardize(X_new) 重新算了新数据自己的平均值和标准差（两条数据永远变成 ±1）；
#     第四版用训练账本的 x_mean、x_std 换算后通过；自己总结出 D29

import numpy as np


# ---------- 已经给你的东西（不用改） ----------

rng = np.random.default_rng(7)                       # 随机数生成器，种子固定为 7（卡 2）
n = 200                                              # 账本记录条数
_level = rng.integers(1, 16, size=n)                 # 城墙等级 1～15
_segs = rng.integers(50, 301, size=n)                # 城墙段数 50～300
_town = rng.integers(1, 17, size=n)                  # 大本营等级 1～16
X_raw = np.column_stack([_level, _segs, _town]).astype(float)    # 原始特征，形状 (200, 3)
y = 3 * _level + 0.2 * _segs + 5 * _town + 10 + rng.normal(0, 3, size=n)   # 实际造价（万金币），形状 (200,)
# ↑ 真实规律藏在这一行里，但模型看不到它，只能看到 X_raw 和 y


# ---------- 自己写的版本 ----------

# ============================================================
# 任务 1｜多特征预测
#   def predict(X, w, b)
#       # X：特征矩阵，形状 (n, d)，每行是一条记录，每列是一个特征
#       # w：权重，形状 (d,)，每个特征一个权重
#       # b：偏置，一个数
#       # 返回：每条记录的预测值，形状 (n,)
#       #       第 i 条的预测 = X[i, 0]·w[0] + X[i, 1]·w[1] + … + X[i, d-1]·w[d-1] + b
#       # 不许写 for 循环
# ============================================================
def predict(X, w, b):
    return np.sum(X * w,axis=1) + b


# ============================================================
# 任务 2｜损失和梯度
#   def mse(X, y, w, b)
#       # 返回：均方误差，一个数
#   def grad(X, y, w, b)
#       # 返回两样东西：(dw, db)
#       #   dw：均方误差对每个权重的偏导数，numpy 数组，形状 (d,)，第 j 个是对 w[j] 的偏导数
#       #   db：均方误差对 b 的偏导数，一个数
#       # 手推公式，不许用数值测量仪，不许写 for 循环
#       # （d 是几都要能用：自测会用 1 个、3 个、5 个特征的数据来测）
# ============================================================
def mse(X, y, w, b):
    return np.mean((np.sum(X * w,axis=1) + b - y) ** 2)

def grad(X, y, w, b):
    u = 2 * (np.sum(X * w,axis=1) + b - y)
    a = np.ones(np.shape(X))
    c  = np.mean(u.reshape(np.shape(X)[0],1) * a * X,axis=0)
    return c,np.mean(u)


# ============================================================
# 任务 3｜标准化
#   def standardize(X)
#       # X：特征矩阵，形状 (n, d)
#       # 返回三样东西：(Xs, mean, std)
#       #   mean：每一列的平均值，形状 (d,)
#       #   std ：每一列的标准差，形状 (d,)
#       #   Xs  ：标准化之后的特征矩阵，形状 (n, d)，每一列都减去这一列的平均值、再除以这一列的标准差
#   然后把账本的原始特征标准化一次，结果存进：
#       Xs, x_mean, x_std = standardize(X_raw)
# ============================================================
def standardize(X):
    mean = np.mean(X,axis=0)
    std = np.std(X,axis=0)
    return (X - mean) / std,mean,std

Xs, x_mean, x_std = standardize(X_raw)


# ============================================================
# 任务 4｜训练，以及三种命运
#   def train(X, y, lr, n_steps)
#       # 从 w = 全 0（形状 (d,)）、b = 0 出发，对均方误差做 n_steps 步梯度下降
#       # 返回三样东西：(w, b, losses)
#       #   losses：长度 n_steps + 1，第 0 个是出发时的损失，第 k 个是走完第 k 步之后的损失
#
#   用 train 跑下面三组实验，看 losses 的开头和结尾，各填一个字符串：
#       "explode"  ——  损失越来越大（可能还会看到 overflow 警告，或者变成 inf / nan）
#       "slow"     ——  损失在下降，但走完了还离第 3 组的结果差得很远
#       "converge" ——  损失降到了一个稳定的低值
#   fate_raw_big   = 原始特征 X_raw，lr = 0.1， 走 10 步
#   fate_raw_small = 原始特征 X_raw，lr = 1e-5，走 1000 步
#   fate_std       = 标准化特征 Xs， lr = 0.1， 走 1000 步
#
#   把第 3 组的结果存进：w_std, b_std, losses_std
#
#   can_reach_zero = 第 3 组再多走 100 万步，损失能不能降到 0？填 True 或 False
# ============================================================
def train(X, y, lr, n_steps):
    w = np.zeros(np.shape(X)[1],)
    b = 0
    losses = [mse(X,y,w,b)]
    for _ in range(n_steps):
        gw,gb = grad(X,y,w,b)
        w = w - lr * gw
        b = b - lr * gb
        losses.append(mse(X,y,w,b))
    return w,b,np.array(losses)
        

fate_raw_big = "explode"
fate_raw_small = "slow"
fate_std = "converge"

w_std, b_std, losses_std = train(Xs,y,0.1,1000)

can_reach_zero =True if train(Xs,y,0.1,1001000)[2][-1] == 0 else False


# ============================================================
# 任务 5｜给新城墙估价
#   两次新的升级，账本里没有：
#       第 1 次：城墙 10 级，200 段，大本营 12 级
#       第 2 次：城墙 1 级，50 段，大本营 1 级
#   X_new = 这两次升级的原始特征，形状 (2, 3)
#   cost_new = 用任务 4 训练出的 w_std、b_std 预测这两次的造价，形状 (2,)
# ============================================================
X_new = np.array([[10,200,12],[1,50,1]])
cost_new = np.sum((X_new - x_mean) / x_std * w_std,axis=1) + b_std


# ============================================================
# 任务 6｜把规律翻译成人话
#   w_std 是「标准化特征」的权重，人看不懂（「段数每多 1 个标准差，造价多多少」）。
#   把它换算回原始单位，得到一组对原始特征 X_raw 直接生效的权重和偏置：
#   def to_original(w_std, b_std, mean, std)
#       # 返回两样东西：(w_orig, b_orig)
#       #   要求：对任何原始特征 X，predict(X, w_orig, b_orig) 和
#       #         predict((X - mean) / std, w_std, b_std) 完全相等
#       # 不许写 for 循环
#   w_orig, b_orig = to_original(w_std, b_std, x_mean, x_std)
#   然后看看 w_orig：城墙每升 1 级、每多 1 段、大本营每升 1 级，造价各多多少万金币？
# ============================================================
def to_original(w_std, b_std, mean, std):
    ...

w_orig, b_orig = ..., ...


# ⬇⬇⬇ 自测（不用改）⬇⬇⬇
import warnings

def _num_grad(X, y, w, b, h=1e-5):                    # 自测自带的验货仪（中心差分）
    dw = np.zeros_like(w)
    for j in range(w.size):
        e = np.zeros_like(w); e[j] = h
        dw[j] = (mse(X, y, w + e, b) - mse(X, y, w - e, b)) / (2 * h)
    db = (mse(X, y, w, b + h) - mse(X, y, w, b - h)) / (2 * h)
    return dw, db

# 任务 1
_X = np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]])
_out = predict(_X, np.array([10.0, -1.0]), 0.5)
assert isinstance(_out, np.ndarray) and _out.shape == (3,), "predict 要返回形状 (n,) 的 numpy 数组"
assert np.allclose(_out, [8.5, 26.5, 44.5]), f"predict 不对：你的 {_out}，应该是 [ 8.5 26.5 44.5]"
assert predict(X_raw, np.zeros(3), 7.0).shape == (200,)
print("✅ 任务 1 多特征预测")

# 任务 2
assert abs(mse(_X, np.array([8.5, 26.5, 44.5]), np.array([10.0, -1.0]), 0.5)) < 1e-12, "预测全对时 mse 应该是 0"
_r = np.random.default_rng(0)
for _d in (1, 3, 5):
    _Xt = _r.normal(size=(30, _d)); _yt = _r.normal(size=30)
    _wt = _r.normal(size=_d);       _bt = _r.normal()
    _dw, _db = grad(_Xt, _yt, _wt, _bt)
    assert isinstance(_dw, np.ndarray) and _dw.shape == (_d,), f"{_d} 个特征时 dw 的形状应该是 ({_d},)，你的是 {np.shape(_dw)}"
    _wdw, _wdb = _num_grad(_Xt, _yt, _wt, _bt)
    assert np.allclose(_dw, _wdw, atol=1e-5), f"{_d} 个特征时 dw 不对：你的 {_dw}，验货仪 {_wdw}"
    assert abs(_db - _wdb) < 1e-5, f"{_d} 个特征时 db 不对：你的 {_db}，验货仪 {_wdb}"
print("✅ 任务 2 损失和梯度（gradient check 通过）")

# 任务 3
assert x_mean.shape == (3,) and x_std.shape == (3,), "mean、std 要各是形状 (3,)：每一列一个"
assert Xs.shape == (200, 3)
assert np.allclose(Xs.mean(axis=0), 0) and np.allclose(Xs.std(axis=0), 1), "标准化之后每一列的平均值应该是 0、标准差应该是 1"
assert np.allclose(Xs * x_std + x_mean, X_raw), "Xs 乘回 std、加回 mean 应该得到原来的 X_raw"
print("✅ 任务 3 标准化")

# 任务 4
_w1, _b1, _l1 = train(_X, np.array([1.0, 2.0, 3.0]), 0.01, 1)
assert isinstance(_w1, np.ndarray) and _w1.shape == (2,), "train 返回的 w 要是形状 (d,) 的 numpy 数组"
assert len(_l1) == 2 and abs(_l1[0] - 14 / 3) < 1e-9, "losses 第 0 个应该是出发点（w 全 0、b = 0）的损失"
assert np.allclose(_w1, [22 / 150, 28 / 150]) and abs(_b1 - 0.04) < 1e-9, f"走 1 步的结果不对：w {_w1}，b {_b1}"
with warnings.catch_warnings():
    warnings.simplefilter("ignore")                     # 发散实验会有 overflow 警告，这里静音
    _, _, _lb = train(X_raw, y, 0.1, 10)
    _, _, _ls = train(X_raw, y, 1e-5, 1000)
_, _, _lg = train(Xs, y, 0.1, 1000)
_want = lambda l: "explode" if not (l[-1] < l[0]) else ("slow" if l[-1] > 3 * _lg[-1] else "converge")
_fates = ("explode", "slow", "converge")
assert fate_raw_big in _fates and fate_raw_small in _fates and fate_std in _fates, '只能填 "explode"、"slow" 或 "converge"'
assert fate_raw_big == _want(_lb), "第 1 组的命运不对，把 losses 的开头和结尾 print 出来看看"
assert fate_raw_small == _want(_ls), "第 2 组的命运不对，把 losses 的开头和结尾 print 出来看看"
assert fate_std == _want(_lg), "第 3 组的命运不对，把 losses 的开头和结尾 print 出来看看"
assert len(losses_std) == 1001 and np.allclose(losses_std, _lg), "w_std, b_std, losses_std 要来自第 3 组实验"
assert can_reach_zero in (True, False) and can_reach_zero == False, "再想想：账本里的造价是怎么来的？"
print(f"✅ 任务 4 训练（损失 {losses_std[0]:.0f} → {losses_std[-1]:.2f}）")

# 任务 5
assert np.shape(X_new) == (2, 3), "X_new 的形状应该是 (2, 3)"
assert np.allclose(X_new, [[10, 200, 12], [1, 50, 1]]), "X_new 写的是原始特征：等级、段数、大本营等级"
assert np.shape(cost_new) == (2,)
assert np.allclose(cost_new, [140, 28], atol=2), f"估价差得太远了：你的 {cost_new}。新数据要和训练数据做同样的处理吗？"
print(f"✅ 任务 5 给新城墙估价（{cost_new[0]:.1f}、{cost_new[1]:.1f} 万金币）")

# 任务 6
_Xr = np.random.default_rng(1).uniform(0, 300, size=(20, 3))
assert np.allclose(predict(_Xr, w_orig, b_orig), predict((_Xr - x_mean) / x_std, w_std, b_std)), "换算后的预测和原来的不一样"
assert np.allclose(w_orig, [3, 0.2, 5], atol=0.15) and abs(b_orig - 10) < 2.5
print(f"✅ 任务 6 规律翻译成人话：城墙每升 1 级 +{w_orig[0]:.2f}，每多 1 段 +{w_orig[1]:.3f}，大本营每升 1 级 +{w_orig[2]:.2f}，基础 {b_orig:.2f}（万金币）")
print("🎉 线性回归第 1 关「大本营的造价账本」通关！")
