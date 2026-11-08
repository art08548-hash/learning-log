# 🏰 部落冲突 · 第 3 关：药水工坊（对应 LeetCode 974 和可被 K 整除的子数组）
#
# elixir[i] 是每天的圣水净变化（可能为负）。求总变化量是 k 的整数倍的连续区间个数。
#
# 做法：前缀和 % k + 哈希表计数，O(n)
#   原理：p_j % k == p_i % k  ⇔  (p_j - p_i) 是 k 的倍数（双向等价，不漏不多）
#   Python 的 % 结果自动非负，负数前缀和不用额外处理
# 完成日期：2026-11-05（思路和原理自己讲出；代码框架由 Claude 给出，核心三行自己填写）


def count_perfect_periods(elixir: list[int], k: int) -> int:
    counts = {0: 1}     # 余数 → 出现次数（空前缀：余数 0 出现过 1 次）
    prefix = 0
    result = 0

    for x in elixir:
        prefix += x
        remainder = prefix % k
        result += counts.get(remainder, 0)               # 先查
        counts[remainder] = counts.get(remainder, 0) + 1  # 再存

    return result


if __name__ == "__main__":
    assert count_perfect_periods([4, 5, 0, -2, -3, 1], 5) == 7
    assert count_perfect_periods([5], 9) == 0
    assert count_perfect_periods([2, -2, 2, -4], 6) == 2
    assert count_perfect_periods([-1, 2, 9], 2) == 2
    print("第 3 关通过 🏆")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

from collections import Counter


def count_perfect_periods_std(elixir: list[int], k: int) -> int:
    counts = Counter({0: 1})          # Counter：访问不存在的键直接返回 0
    prefix = result = 0
    for x in elixir:
        prefix = (prefix + x) % k     # 直接存余数；C++ / Java 要写 (p % k + k) % k
        result += counts[prefix]
        counts[prefix] += 1
    return result


if __name__ == "__main__":
    assert count_perfect_periods_std([4, 5, 0, -2, -3, 1], 5) == 7
    assert count_perfect_periods_std([-1, 2, 9], 2) == 2
    print("标准写法也通过 ✅")
