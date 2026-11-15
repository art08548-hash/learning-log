# 🏰 部落冲突 · 线性回归热身 1：圣水收集器（单特征，自己挑学习率）
#
# 📜 剧情：
#   部落的圣水收集器开着不关，建筑大师记了 30 次「开了几小时 → 攒了多少圣水」。
#   收集器有时被哥布林偷一点，有时被法术加速，数字带噪声。
#   这次没人替你写 mse 和梯度，学习率也没人替你挑，全部自己来。
#
# 🎯 每个任务的说明就写在要实现的位置正上方
# 🚫 不许用 np.polyfit、np.linalg.lstsq、sklearn 等现成的拟合工具

import numpy as np


# ---------- 已经给你的东西（不用改） ----------

_rng = np.random.default_rng(11)
hours = _rng.uniform(1, 24, size=30)                                  # 开了几小时，形状 (30,)
elixir = 120 * hours + 300 + _rng.normal(0, 20, size=30)             # 攒了多少圣水，形状 (30,)


# ---------- 自己写的版本 ----------

# ============================================================
# 任务 1｜损失和梯度
#   模型：预测 = w × x + b，两个旋钮装进 params = [w, b]
#   def mse(params, xs, ys)
#       # 返回：均方误差，一个数
#   def grad(params, xs, ys)
#       # 返回：均方误差在 params 处的梯度，numpy 数组，形状 (2,)
#       # 手推公式，不许写 for 循环
# ============================================================
def mse(params, xs, ys):
    ...

def grad(params, xs, ys):
    ...


# ============================================================
# 任务 2｜训练（学习率自己挑）
#   def train(xs, ys, lr, n_steps)
#       # 从 params = [0, 0] 出发做 n_steps 步梯度下降
#       # 返回两样东西：(params, losses)，losses 长度 n_steps + 1
#   my_lr    = 你挑的学习率
#   my_steps = 你挑的步数（不超过 100000）
#   params, losses = train(hours, elixir, my_lr, my_steps)
#   要求：训练完的损失，离这本账本能达到的最低损失不超过 1%
# ============================================================
def train(xs, ys, lr, n_steps):
    ...

my_lr = ...
my_steps = ...
params, losses = ..., ...


# ============================================================
# 任务 3｜预测
#   elixir_8h = 用训练好的 params，预测开 8 小时能攒多少圣水
# ============================================================
elixir_8h = ...


# ⬇⬇⬇ 自测（不用改）⬇⬇⬇
_p = np.array([2.0, 1.0]); _xt = np.array([1.0, 2.0, 3.0]); _yt = np.array([4.0, 4.0, 9.0])
assert abs(mse(_p, _xt, _yt) - 2) < 1e-9, "mse 不对"
_g = grad(_p, _xt, _yt)
_h = 1e-5
_want = np.array([(mse(_p + [_h, 0], _xt, _yt) - mse(_p - [_h, 0], _xt, _yt)) / (2 * _h),
                  (mse(_p + [0, _h], _xt, _yt) - mse(_p - [0, _h], _xt, _yt)) / (2 * _h)])
assert isinstance(_g, np.ndarray) and _g.shape == (2,) and np.allclose(_g, _want, atol=1e-5), f"grad 不对：你的 {_g}，验货仪 {_want}"
print("✅ 任务 1 损失和梯度")

assert 0 < my_lr and 0 < my_steps <= 100000
assert isinstance(params, np.ndarray) and params.shape == (2,) and len(losses) == my_steps + 1
_best = mse(np.polyfit(hours, elixir, 1), hours, elixir)          # 自测可以用现成工具算出最低损失
assert np.isfinite(losses[-1]) and losses[-1] < losses[0], f"损失从 {losses[0]:.0f} 变成了 {losses[-1]:.3g}：学习率太大，发散了"
assert losses[-1] <= 1.01 * _best, f"还没走到谷底：你的损失 {losses[-1]:.1f}，最低能到 {_best:.1f}。步子再大点，或者多走几步？"
print(f"✅ 任务 2 训练（lr = {my_lr}，{my_steps} 步，损失 {losses[0]:.0f} → {losses[-1]:.1f}，最低 {_best:.1f}）")

assert abs(elixir_8h - (params[0] * 8 + params[1])) < 1e-9 and abs(elixir_8h - 1260) < 30
print(f"✅ 任务 3 预测（开 8 小时 ≈ {elixir_8h:.0f} 圣水）")
print("🎉 热身 1「圣水收集器」通关！")
