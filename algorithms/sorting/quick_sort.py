# 🏰 部落冲突 · 排序第 4 关：全军大阅兵（快速排序，对应 LeetCode 912 排序数组）
#
# 原地快速排序，平均 O(n log n)，不许用 sort。
#
# 做法：
#   partition：先随机挑一个位置 k，和这一段末尾交换，让随机元素当 pivot；
#              再用第 3 关的双指针（Hoare 风格）分区；最后把 pivot 换到相遇处
#   quick_sort：l >= r 直接返回（空段或单个元素）；分区；左右两段分别递归
# 完成日期：2026-11-08（按自己的思路写到底；Claude 指出的问题：partition 里
#   j 未赋值 / pivot 用了下标而不是值 / 末尾交换没记住原位置；quick_sort 缺终止条件、
#   没传范围；终止条件 l == r 漏了空段。随机 pivot 自己加上）


import random


def partition(troops: list[int], i=0, j=None) -> int:
    if j is None:
        j = len(troops) - 1

    k = random.randint(i, j)

    t = troops[j]
    troops[j] = troops[k]
    troops[k] = t

    p = troops[j]
    pi = j
    while i < j:

        while troops[i] <= p and i != j:  # 找大
            i += 1

        while troops[j] >= p and i != j:
            j -= 1

        t = troops[i]
        troops[i] = troops[j]
        troops[j] = t

    t = troops[pi]
    troops[pi] = troops[i]
    troops[i] = t

    return i


def quick_sort(troops: list[int], l=0, r=None) -> None:
    if r is None:
        r = len(troops) - 1

    if l >= r:
        return

    p = partition(troops, l, r)

    a = l
    b = p - 1
    quick_sort(troops, a, b)

    a = p + 1
    b = r
    quick_sort(troops, a, b)


if __name__ == "__main__":
    def check(arr):
        expected = sorted(arr)
        quick_sort(arr)
        assert arr == expected

    check([5, 2, 4, 6, 1, 3])
    check([])
    check([7])
    check([2, 1])
    check([3, -1, 3, 0, -1, 2])
    check([9, 8, 7, 6, 5, 4, 3, 2, 1])
    for _ in range(1000):
        check([random.randint(-100, 100) for _ in range(random.randint(0, 50))])
    check([random.randint(-10**9, 10**9) for _ in range(10**5)])
    check(list(range(10**5)))
    print("排序第 4 关通过 🏆")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

def partition_std(a: list[int], lo: int, hi: int) -> int:
    k = random.randint(lo, hi)
    a[k], a[hi] = a[hi], a[k]          # 随机元素换到末尾当 pivot
    p = a[hi]
    i, j = lo, hi
    while i < j:
        while i < j and a[i] <= p:
            i += 1
        while i < j and a[j] >= p:
            j -= 1
        a[i], a[j] = a[j], a[i]
    a[i], a[hi] = a[hi], a[i]
    return i


def _quick_sort_std(a: list[int], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    p = partition_std(a, lo, hi)
    _quick_sort_std(a, lo, p - 1)
    _quick_sort_std(a, p + 1, hi)


def quick_sort_std(a: list[int]) -> None:
    _quick_sort_std(a, 0, len(a) - 1)   # 外层包装：对外参数简单，对内统一传 lo / hi


if __name__ == "__main__":
    t = list(range(10**5))
    quick_sort_std(t)
    assert t == list(range(10**5))
    print("标准写法也通过 ✅")
