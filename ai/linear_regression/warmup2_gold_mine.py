# 🏰 部落冲突 · 线性回归热身 2：金矿自动停工（训练到收敛就停）
#
# 📜 剧情：
#   之前的训练都是「固定走多少步」。可是走多少步才够，事先并不知道：
#   走少了没到谷底，走多了白白浪费时间。
#   建筑大师想要一台会自己停下来的训练机：损失几乎不再下降时就收工。
#   账本：40 座金矿的等级 → 每小时产金。
#
# 🎯 每个任务的说明就写在要实现的位置正上方
# 🚫 不许用 np.polyfit、np.linalg.lstsq、sklearn 等现成的拟合工具
#
# 完成日期：2026-11-18 ✅（2026-11-17 任务 1）
#   train_until 用 while 循环；初始值 e = 出发时损失 + 2 × tol，保证第一次一定进得了循环
#   第一版没用上 max_steps；第二版写成 <=，多走了 1 步（51 vs 50），自己改成 < 通过
#   任务 2、3 一次写对：走了 2391 步自己停下，w ≈ 502.6、b ≈ 979.0
#   Claude 的建议：True if 条件 else False 可以直接写成「条件」本身；train_until 里 mse(params) 每轮算了两次

import numpy as np


# ---------- 已经给你的东西（不用改） ----------

_rng = np.random.default_rng(23)
mine_lv = _rng.integers(1, 11, size=40).astype(float)                # 金矿等级 1～10，形状 (40,)
gold = 500 * mine_lv + 1000 + _rng.normal(0, 100, size=40)           # 每小时产金，形状 (40,)

def mse(params, xs, ys):
    errs = params[0] * xs + params[1] - ys
    return np.mean(errs ** 2)

def grad(params, xs, ys):
    errs = params[0] * xs + params[1] - ys
    return np.array([np.mean(2 * errs * xs), np.mean(2 * errs)])


# ---------- 自己写的版本 ----------

# ============================================================
# 任务 1｜会自己停的训练机
#   def train_until(xs, ys, lr, tol, max_steps)
#       # 从 params = [0, 0] 出发，一步一步做梯度下降
#       # 每走完一步，比较「这一步之前的损失」和「这一步之后的损失」：
#       #     两者之差的绝对值 < tol  →  立刻停下（这一步算走过了）
#       # 如果一直没停，走满 max_steps 步也停下
#       # 返回两样东西：(params, steps_used)
#       #   params    ：停下时的位置，numpy 数组，形状 (2,)
#       #   steps_used：一共走了几步，一个整数
# ============================================================
def train_until(xs, ys, lr, tol, max_steps):
    params = np.zeros(2,)
    g = grad(params,xs,ys)
    e = mse(params,xs,ys) + 2 * tol
    steps_used = 0
    while steps_used < max_steps and np.abs(e - mse(params,xs,ys)) >= tol:
        e = mse(params,xs,ys)
        params = params - lr * g
        g = grad(params,xs,ys)
        steps_used += 1
    return params,steps_used


# ============================================================
# 任务 2｜开工
#   用 lr = 0.01、tol = 1e-6、max_steps = 100000 训练金矿账本，结果存进：
#       params, steps_used
#   stopped_early = 是不是在走满 max_steps 之前就自己停了？填 True 或 False（看 steps_used 判断）
# ============================================================
params, steps_used = train_until(mine_lv,gold,0.01,1e-6,100000)
stopped_early = True if steps_used < 100000 else False


# ============================================================
# 任务 3｜预测
#   gold_lv12 = 用训练好的 params，预测 12 级金矿每小时产多少金（账本里最高只有 10 级）
# ============================================================
gold_lv12 = params[0] * 12 + params[1]


# ⬇⬇⬇ 自测（不用改）⬇⬇⬇
def _ref(xs, ys, lr, tol, max_steps):
    p = np.zeros(2); prev = mse(p, xs, ys)
    for k in range(1, max_steps + 1):
        p = p - lr * grad(p, xs, ys); cur = mse(p, xs, ys)
        if abs(prev - cur) < tol:
            return p, k
        prev = cur
    return p, max_steps

for _args in [(0.01, 1e-6, 100000), (0.01, 1.0, 100000), (0.01, 1e-6, 50), (0.001, 1e-3, 100000)]:
    _p, _k = train_until(mine_lv, gold, *_args)
    _rp, _rk = _ref(mine_lv, gold, *_args)
    assert isinstance(_p, np.ndarray) and _p.shape == (2,), "params 要是形状 (2,) 的 numpy 数组"
    assert _k == _rk, f"lr, tol, max_steps = {_args} 时走的步数不对：你的 {_k}，应该是 {_rk}"
    assert np.allclose(_p, _rp), f"lr, tol, max_steps = {_args} 时停下的位置不对"
print("✅ 任务 1 会自己停的训练机")

assert np.allclose(params, _ref(mine_lv, gold, 0.01, 1e-6, 100000)[0]) and steps_used == _ref(mine_lv, gold, 0.01, 1e-6, 100000)[1]
assert stopped_early == (steps_used < 100000)
print(f"✅ 任务 2 开工（走了 {steps_used} 步自己停下，w = {params[0]:.1f}，b = {params[1]:.1f}）")

assert abs(gold_lv12 - (params[0] * 12 + params[1])) < 1e-9
print(f"✅ 任务 3 预测（12 级金矿 ≈ {gold_lv12:.0f} 金 / 小时）")
print("🎉 热身 2「金矿自动停工」通关！")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

def train_until_std(xs, ys, lr, tol, max_steps):
    """for 循环数步数，满足容差就 return；损失每步只算一次（H1）。"""
    params = np.zeros(2)
    prev = mse(params, xs, ys)                 # 这一步之前的损失
    for k in range(1, max_steps + 1):          # k = 走完这一步之后的步数，1, 2, …, max_steps
        params = params - lr * grad(params, xs, ys)
        cur = mse(params, xs, ys)              # 这一步之后的损失
        if abs(prev - cur) < tol:
            return params, k                   # 提前停：这一步算走过了
        prev = cur                             # 这一步的「之后」就是下一步的「之前」
    return params, max_steps                   # 走满了也没停


for _args in [(0.01, 1e-6, 100000), (0.01, 1.0, 100000), (0.01, 1e-6, 50)]:
    _a, _b = train_until_std(mine_lv, gold, *_args), train_until(mine_lv, gold, *_args)
    assert np.allclose(_a[0], _b[0]) and _a[1] == _b[1]
assert stopped_early == (steps_used < 100000)          # 比较本身就是 True / False，不用再套 if else
print("标准写法也通过 ✅")
