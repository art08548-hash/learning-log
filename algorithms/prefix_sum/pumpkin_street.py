# 🎃 南瓜街的糖果账本（对应 LeetCode 560 和为 K 的子数组）
#
# n 栋房子排成一排，candies[i] 是第 i 栋给的糖果数，可能为负（捣蛋屋偷糖）。
# 求有多少段【连续的】房子，净拿到的糖果【恰好】等于 k。
#
# 约束：1 <= n <= 10^5，-1000 <= candies[i] <= 1000
#
# 做法：前缀和 + 哈希表计数，O(n)
# 完成日期：2026-11-02（用了 1 个提示：前缀和之差）


def count_lucky_streets(candies: list[int], k: int) -> int:
    counts = {0: 1}
    prefix_sum = 0
    result = 0

    for candy in candies:
        prefix_sum += candy
        result += counts.get(prefix_sum - k, 0)
        counts[prefix_sum] = counts.get(prefix_sum, 0) + 1

    return result


if __name__ == "__main__":
    assert count_lucky_streets([1, 1, 1], 2) == 2
    assert count_lucky_streets([2, -1, 1, 2], 2) == 4
    assert count_lucky_streets([3, 4, -7, 3, 1, 3, 1, -4, -2, -2], 7) == 3
    print("全部通过 🎃")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

from collections import defaultdict


def count_lucky_streets_std(candies: list[int], k: int) -> int:
    counts = defaultdict(int)
    counts[0] = 1          # 空前缀：让从第 0 栋开始的区间也能被数到
    prefix_sum = result = 0
    for candy in candies:
        prefix_sum += candy
        result += counts[prefix_sum - k]   # 先查
        counts[prefix_sum] += 1            # 再存
    return result


if __name__ == "__main__":
    assert count_lucky_streets_std([1, 1, 1], 2) == 2
    assert count_lucky_streets_std([2, -1, 1, 2], 2) == 4
    assert count_lucky_streets_std([3, 4, -7, 3, 1, 3, 1, -4, -2, -2], 7) == 3
    print("标准写法也通过 ✅")
