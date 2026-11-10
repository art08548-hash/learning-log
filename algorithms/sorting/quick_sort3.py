# 🏰 部落冲突 · 排序附加挑战：三色军团（三路分区快速排序，荷兰国旗问题）
#
# 请实现：
#     def partition3(troops: list[int], lo: int, hi: int) -> tuple[int, int]
#         # 随机选一个 pivot，原地把 troops[lo..hi] 分成三段：
#         #     troops[lo .. lt-1]  全部 <  pivot
#         #     troops[lt .. gt]    全部 == pivot
#         #     troops[gt+1 .. hi]  全部 >  pivot
#         # 返回 (lt, gt)
#
#     def quick_sort3(troops: list[int]) -> None
#         # 用 partition3 实现的原地快速排序
#
# 要求：partition3 O(n) 时间、O(1) 额外空间（只用交换）；
#       quick_sort3 全部相等时也不能退化；不许用 sorted() / .sort()
#
# 做法（自己想出，分三遍扫）：
#   1. 随机 pivot 换到末尾；从 hi 往 lo 扫一遍，把所有 == pivot 的收到末尾 [hi-counts+1, hi]
#   2. 对剩下的 [lo, hi-counts+1] 用第 4 关的两路分区（末尾那个 pivot 当哨兵）
#   3. 相遇点 i 以后是「> pivot 的一段 + == pivot 的一段」，首尾对称交换 i+r ↔ hi-r，
#      把 == pivot 的整块换到 i 开头
#   和 Bentley-McIlroy 三路分区的思路很像（它是在分区过程中把相等的收到两头，最后换到中间）
#
# 完成日期：2026-11-09（2026-11-08 开始；自己的思路写到底；
#   Claude 指出的问题：第一遍扫描写成 j >= 0，扫出了 [lo, hi]；
#   `troops[hi] = troops[i]` 只赋值没交换，下标 i 上的士兵被复制了一份 → 改成交换）
# 自测：partition3 2000 组随机小数组 + 10^5 全部相等 / 三种值 / 已排序 / 倒序 / 随机，全部通过


import random


def partition(troops: list[int],lo,hi) -> int:

    k = random.randint(lo,hi)

    i,j = lo,hi

    troops[j],troops[k] = troops[k],troops[j]

    p = troops[j]

    counts = 0

    while j >= lo:

        if troops[j] == p:

            troops[j],troops[hi - counts] = troops[hi - counts],troops[j]

            counts += 1

        j -= 1

    j = hi - counts + 1

    while i < j:

        while i < j and troops[i] <= p:
            i += 1

        while i < j and troops[j] >= p:
            j -= 1

        troops[i],troops[j] = troops[j],troops[i]

    troops[hi],troops[i] = troops[i],troops[hi]#修改

    counts -= 1

    for r in range(counts):

        troops[hi - r - 1] = troops[i + r + 1]
        troops[i + r + 1] = p

    return (i,i + counts)


def quick_sort(troops: list[int],lo = 0,hi = None) -> None:
    if hi is None:
        hi = len(troops) - 1

    if lo >= hi:
        return

    l,h = partition(troops,lo,hi)

    quick_sort(troops,lo,l - 1)

    quick_sort(troops,h + 1,hi)


partition3, quick_sort3 = partition, quick_sort   # 题目要求的名字


# ============================================================
# 📘 业界标准写法（Dijkstra 三路分区，一遍扫完）
# ============================================================
#
# 三个指针把 troops[lo..hi] 分成四段，循环中始终保持：
#     [lo, lt-1]   < p     已确定
#     [lt, i-1]   == p     已确定
#     [i,  gt]     ?       还没看过
#     [gt+1, hi]   > p     已确定
# 每一步看 a[i]：
#     < p：和 a[lt] 交换。a[lt] 是已经看过的 == p（或者 lt == i 就是它自己），所以 lt、i 都 +1
#     > p：和 a[gt] 交换。换过来的 a[gt] 还没看过，所以只有 gt -1，i 不动
#     == p：直接 i +1
# 「没看过」那一段每一步缩短 1 → 正好 n 步，O(n) 时间、O(1) 空间

def partition3_std(a: list[int], lo: int, hi: int) -> tuple[int, int]:
    p = a[random.randint(lo, hi)]      # 记的是值，不用换到末尾
    lt, i, gt = lo, lo, hi
    while i <= gt:
        if a[i] < p:
            a[lt], a[i] = a[i], a[lt]
            lt += 1
            i += 1
        elif a[i] > p:
            a[i], a[gt] = a[gt], a[i]
            gt -= 1
        else:
            i += 1
    return lt, gt


def _quick_sort3_std(a: list[int], lo: int, hi: int) -> None:
    if lo >= hi:
        return
    lt, gt = partition3_std(a, lo, hi)
    _quick_sort3_std(a, lo, lt - 1)
    _quick_sort3_std(a, gt + 1, hi)


def quick_sort3_std(a: list[int]) -> None:
    _quick_sort3_std(a, 0, len(a) - 1)


# ============================================================
# 🧪 自测：两个版本都跑
# ============================================================

def run_tests(partition3, quick_sort3, name):
    import time
    from collections import Counter

    def check_partition(arr, lo, hi):
        before = arr[:]
        lt, gt = partition3(arr, lo, hi)
        assert lo <= lt <= gt <= hi, f"边界不对：lo={lo}, lt={lt}, gt={gt}, hi={hi}"
        assert arr[:lo] == before[:lo] and arr[hi+1:] == before[hi+1:], "动到了 [lo, hi] 以外的士兵"
        assert Counter(arr[lo:hi+1]) == Counter(before[lo:hi+1]), "士兵数量变了（丢了或多了）"
        p = arr[lt]
        assert all(x < p for x in arr[lo:lt])
        assert all(x == p for x in arr[lt:gt+1])
        assert all(x > p for x in arr[gt+1:hi+1])
        return lt, gt

    check_partition([3], 0, 0)
    check_partition([2, 1], 0, 1)
    assert check_partition([7, 7, 7, 7, 7], 0, 4) == (0, 4)
    check_partition([4, 9, 4, 1, 4, 8, 0, 4], 0, 7)
    check_partition([9, 3, 1, 3, 7, 3, 2, 9], 2, 6)
    for _ in range(2000):
        n = random.randint(1, 12)
        a = [random.randint(0, 3) for _ in range(n)]
        lo = random.randint(0, n - 1); hi = random.randint(lo, n - 1)
        check_partition(a, lo, hi)

    for _ in range(500):
        case = [random.randint(-20, 20) for _ in range(random.randint(0, 50))]
        a = case[:]; quick_sort3(a); assert a == sorted(case)

    N = 10**5
    big = {
        "全部相等": [7] * N,
        "只有三种值": [random.choice([1, 2, 3]) for _ in range(N)],
        "已排好序": list(range(N)),
        "倒序": list(range(N, 0, -1)),
        "完全随机": [random.randint(-10**9, 10**9) for _ in range(N)],
    }
    for case_name, case in big.items():
        a = case[:]
        t = time.perf_counter()
        quick_sort3(a)
        t = time.perf_counter() - t
        assert a == sorted(case), case_name
        print(f"  ✅ {case_name:<6} {t:.2f}s")
    print(f"🎉 {name} 全部通过")


if __name__ == "__main__":
    run_tests(partition3, quick_sort3, "自己的版本")
    run_tests(partition3_std, quick_sort3_std, "📘 标准写法")
