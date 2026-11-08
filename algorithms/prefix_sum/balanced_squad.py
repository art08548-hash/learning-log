# 🏰 部落冲突 · 第 4 关：均势部落战（对应 LeetCode 525 连续数组）
#
# army[i] 为 1 表示野蛮人，0 表示弓箭手。求两种兵数量相等的最长连续一段的长度。
#
# 做法：弓箭手当 -1 → 问题变成「和为 0 的最长子数组」
#       前缀和 + 哈希表存「前缀和第一次出现的下标」，初始化 {0: -1}，O(n)
# 完成日期：2026-11-05（0 → -1 的转化自己想出；循环写法 / 查找目标的 bug 在 Claude 指出后修正）


def longest_balanced_squad(army: list[int]) -> int:
    for idx in range(len(army)):
        if army[idx] == 0:
            army[idx] = -1

    counts = {0: -1}
    prefix = 0
    l = 0

    for k, i in enumerate(army):
        prefix += i

        if prefix in counts:
            l = max(l, k - counts.get(prefix))

        if prefix not in counts:
            counts[prefix] = k

    return l


if __name__ == "__main__":
    assert longest_balanced_squad([0, 1]) == 2
    assert longest_balanced_squad([0, 1, 0]) == 2
    assert longest_balanced_squad([0, 0, 1, 0, 0, 0, 1, 1]) == 6
    assert longest_balanced_squad([1, 1, 1]) == 0
    assert longest_balanced_squad([1, 0, 1, 1, 0, 0, 1]) == 6
    print("第 4 关通过 🏆")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

def longest_balanced_squad_std(army: list[int]) -> int:
    first = {0: -1}          # 前缀和 → 第一次出现的下标
    prefix = best = 0
    for i, x in enumerate(army):
        prefix += 1 if x == 1 else -1     # 边遍历边转化，不修改传进来的数组
        if prefix in first:
            best = max(best, i - first[prefix])
        else:
            first[prefix] = i
    return best


if __name__ == "__main__":
    assert longest_balanced_squad_std([0, 0, 1, 0, 0, 0, 1, 1]) == 6
    assert longest_balanced_squad_std([1, 1, 1]) == 0
    print("标准写法也通过 ✅")
