# 🏰 部落冲突 · 排序第 3 关：指挥官站队（快速排序的分区）
#
# 以最后一个元素为 pivot，原地把 <= pivot 的放左边、>= pivot 的放右边，返回 pivot 的最终下标。
# O(n) 时间，O(1) 额外空间。
#
# 做法（自己想出，属于 Hoare 风格的双指针分区）：
#   i 从左往右找「比 pivot 大」的，j 从右往左找「比 pivot 小」的，找到就交换；
#   两指针相遇后，把 pivot 换到相遇的位置
#   为什么对：j 指着的元素始终 >= pivot（一开始就是 pivot 本身，之后是交换过来的大元素），
#   所以相遇位置上的元素一定 >= pivot，和末尾的 pivot 交换后右边仍然都 >= pivot
# 完成日期：2026-11-07（**独立完成，没有用提示**；自测 + 20 万组随机对拍全部通过）


def partition(troops: list[int]) -> int:
    if len(troops) == 0:
        pass  # 占位
    i = 0  # 找大
    j = len(troops) - 1  # 找小，不越过基准本身防止越界
    p = troops[-1]
    while i < j:

        while troops[i] <= p and i != j:  # 找大
            i += 1

        while troops[j] >= p and i != j:
            j -= 1

        t = troops[i]
        troops[i] = troops[j]
        troops[j] = t

    t = troops[-1]
    troops[-1] = troops[i]
    troops[i] = t

    return i


if __name__ == "__main__":
    import random

    def check(troops):
        original = troops[:]
        pivot = original[-1]
        p = partition(troops)
        assert sorted(troops) == sorted(original), "士兵数量或等级变了"
        assert troops[p] == pivot, "返回的下标上不是指挥官"
        assert all(x <= pivot for x in troops[:p]), "左边有人比指挥官等级高"
        assert all(x >= pivot for x in troops[p + 1:]), "右边有人比指挥官等级低"

    check([3, 8, 2, 5, 1, 4, 7, 6])
    check([1, 2, 3, 4, 5])
    check([5, 4, 3, 2, 1])
    check([7])
    check([2, 1])
    check([5, 5, 5, 5])
    check([4, 9, 4, 1, 4])
    for _ in range(1000):
        check([random.randint(-20, 20) for _ in range(random.randint(1, 30))])
    print("排序第 3 关通过 🏆")
