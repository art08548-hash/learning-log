# 🏰 部落冲突 · 第 5 关（Boss）：援军调度（对应 LeetCode 1109 航班预订统计）
#
# n 个村庄，若干条指令 [first, last, troops]：给 first..last（含两端）每个村庄派 troops 个援军。
# 求所有指令执行完后每个村庄的援军数。要求 O(n + 指令数)。
#
# 做法：差分数组 diff（长 n+1），每条指令只改 diff[first] 和 diff[last+1]；
#       最后对 diff 的前 n 位做前缀和，还原出答案
# 完成日期：2026-11-05（自己看出「差分 = 离散导数」；两处 bug 由 Claude 指出后修正）


def dispatch_reinforcements(n: int, orders: list[list[int]]) -> list[int]:
    diff = [0] * (n + 1)
    a = [0] * n
    s = 0
    for i in orders:
        diff[i[0]] += i[2]
        diff[i[1] + 1] -= i[2]

    for i in range(n):
        s += diff[i]
        a[i] = s

    return a


if __name__ == "__main__":
    assert dispatch_reinforcements(5, [[0, 1, 10], [1, 2, 20], [1, 4, 25]]) == [10, 55, 45, 25, 25]
    assert dispatch_reinforcements(2, [[0, 0, 10], [1, 1, 15]]) == [10, 15]
    assert dispatch_reinforcements(4, [[0, 3, 5], [2, 2, -3]]) == [5, 5, 2, 5]
    print("第 5 关通过 🏆 前缀和模块通关！")
