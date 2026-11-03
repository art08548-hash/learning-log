# 🏰 部落冲突 · 第 1 关：金库流水账（对应 LeetCode 303 区域和检索 - 数组不可变）
#
# gold[i] 是第 i 小时的金币净变化。多次询问 [left, right]（含两端）的总变化，
# 每次 query 必须 O(1)。
#
# 做法：__init__ 预处理前缀和 O(n)，query 用 prefix[right+1] - prefix[left] O(1)
# 完成日期：2026-11-03（思路自己想出；两处 bug 由 Claude 指出后修正）
#   bug 1：循环从 1 开始，漏加了 gold[0]，前缀数组也少一位
#   bug 2：query 返回了切片（列表），而不是两个前缀和之差


class GoldVault:
    def __init__(self, gold: list[int]):
        self.goldsum = [0]
        for x in gold:
            self.goldsum.append(self.goldsum[-1] + x)

    def query(self, left: int, right: int) -> int:
        return self.goldsum[right + 1] - self.goldsum[left]


if __name__ == "__main__":
    vault = GoldVault([3, -2, 5, 1, -4, 6])
    assert vault.query(0, 2) == 6
    assert vault.query(2, 5) == 8
    assert vault.query(1, 1) == -2
    assert vault.query(0, 5) == 9
    print("第 1 关通过 🏆")
