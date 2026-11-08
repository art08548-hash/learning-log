# 🏰 部落冲突 · 排序第 2 关：全军整编（归并排序，对应 LeetCode 912 排序数组）
#
# 用归并排序把乱序列表按从小到大排好，返回新列表。O(n log n)，不许用 sort。
#
# 做法：长度 <= 1 直接返回；对半切；左右两半分别递归排序；用第 1 关的 merge 合并
# 完成日期：2026-11-06（框架自己写出；漏接递归返回值由 Claude 指出后修正）


def merge(clan_a: list[int], clan_b: list[int]) -> list[int]:
    a = []
    i = j = 0
    while i < len(clan_a) and j < len(clan_b):
        if clan_a[i] > clan_b[j]:
            a.append(clan_b[j])
            j += 1
        else:
            a.append(clan_a[i])
            i += 1
    a.extend(clan_a[i:])
    a.extend(clan_b[j:])
    return a


def merge_sort(troops: list[int]) -> list[int]:

    if len(troops) <= 1:
        return troops

    l = troops[0:len(troops)//2]
    r = troops[len(troops)//2:]

    l = merge_sort(l)
    r = merge_sort(r)

    return merge(l, r)


if __name__ == "__main__":
    import random

    assert merge_sort([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]
    assert merge_sort([]) == []
    assert merge_sort([7]) == [7]
    assert merge_sort([3, -1, 3, 0, -1, 2]) == [-1, -1, 0, 2, 3, 3]
    assert merge_sort([9, 8, 7, 6, 5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5, 6, 7, 8, 9]

    for _ in range(1000):
        arr = [random.randint(-100, 100) for _ in range(random.randint(0, 50))]
        assert merge_sort(arr) == sorted(arr)

    big = [random.randint(-10**9, 10**9) for _ in range(10**5)]
    assert merge_sort(big) == sorted(big)

    print("排序第 2 关通过 🏆")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

def merge_sort_std(troops: list[int]) -> list[int]:
    if len(troops) <= 1:
        return troops
    mid = len(troops) // 2
    return merge(merge_sort_std(troops[:mid]), merge_sort_std(troops[mid:]))


if __name__ == "__main__":
    assert merge_sort_std([5, 2, 4, 6, 1, 3]) == [1, 2, 3, 4, 5, 6]
    print("标准写法也通过 ✅")
