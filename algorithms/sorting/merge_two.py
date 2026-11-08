# 🏰 部落冲突 · 排序第 1 关：两军会师（对应 LeetCode 88 / 21 合并两个有序数组 / 链表）
#
# 合并两个已按从小到大排好序的列表，结果也要有序。O(len(a) + len(b))，不许用 sort。
#
# 做法：两个指针各指一个列表，每次把较小的放进结果；一边用完后，把另一边剩下的补上
#   相等时先取 clan_a 的元素（用 > 判断），保证稳定
# 完成日期：2026-11-05（结构自己写出；while 条件写反由 Claude 指出后修正）


def merge(clan_a: list[int], clan_b: list[int]) -> list[int]:
    a = []
    i = 0
    j = 0
    while i < len(clan_a) and j < len(clan_b):
        if clan_a[i] > clan_b[j]:
            a.append(clan_b[j])
            j += 1
        else:
            a.append(clan_a[i])
            i += 1
    k = len(clan_a) - i if j == len(clan_b) else len(clan_b) - j

    for _ in range(k):
        if j == len(clan_b):
            a.append(clan_a[i])
            i += 1
        else:
            a.append(clan_b[j])
            j += 1

    return a


if __name__ == "__main__":
    assert merge([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge([], [1, 2]) == [1, 2]
    assert merge([1, 1, 2], [1, 3]) == [1, 1, 1, 2, 3]
    assert merge([-3, 7], []) == [-3, 7]
    assert merge([10, 20, 30], [1, 2]) == [1, 2, 10, 20, 30]
    print("排序第 1 关通过 🏆")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

def merge_std(clan_a: list[int], clan_b: list[int]) -> list[int]:
    result = []
    i = j = 0
    while i < len(clan_a) and j < len(clan_b):
        if clan_b[j] < clan_a[i]:        # 相等时取左边 → 稳定
            result.append(clan_b[j])
            j += 1
        else:
            result.append(clan_a[i])
            i += 1
    result.extend(clan_a[i:])            # 用完的那一边切片为空，extend 无影响
    result.extend(clan_b[j:])
    return result


if __name__ == "__main__":
    assert merge_std([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]
    assert merge_std([], [1, 2]) == [1, 2]
    print("标准写法也通过 ✅")
