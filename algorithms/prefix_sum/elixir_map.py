# 🏰 部落冲突 · 第 2 关：圣水矿脉勘探（对应 LeetCode 304 二维区域和检索 - 矩阵不可变）
#
# m × n 网格 elixir，多次询问以 (r1, c1) 为左上角、(r2, c2) 为右下角的矩形和，
# 每次 query 必须 O(1)。
#
# 做法：二维前缀和（容斥），预处理 O(m·n)，查询 O(1)
# 完成日期：2026-11-03（独立完成，一次通过）


class ElixirMap:
    def __init__(self, elixir: list[list[int]]):
        self.prefix = [[0] * (len(elixir[0]) + 1) for _ in range(len(elixir) + 1)]
        for i in range(1, len(elixir) + 1):
            for j in range(1, len(elixir[0]) + 1):
                self.prefix[i][j] = (self.prefix[i - 1][j] + self.prefix[i][j - 1]
                                     - self.prefix[i - 1][j - 1] + elixir[i - 1][j - 1])

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        return (self.prefix[r2 + 1][c2 + 1] - self.prefix[r1][c2 + 1]
                - self.prefix[r2 + 1][c1] + self.prefix[r1][c1])


if __name__ == "__main__":
    elixir = [
        [3, 0, 1, 4],
        [5, 6, 3, 2],
        [1, 2, 0, 1],
        [4, 1, 0, 5],
    ]
    m = ElixirMap(elixir)
    assert m.query(1, 1, 2, 2) == 11
    assert m.query(0, 0, 1, 1) == 14
    assert m.query(2, 0, 3, 3) == 14
    assert m.query(0, 3, 3, 3) == 12
    assert m.query(1, 2, 1, 2) == 3
    assert m.query(0, 0, 3, 3) == 38
    print("第 2 关通过 🏆")


# ============================================================
# 📘 业界标准写法（对照用；上面是自己写的版本）
# ============================================================

class ElixirMapStd:
    def __init__(self, elixir: list[list[int]]):
        m, n = len(elixir), len(elixir[0])
        P = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m):
            for j in range(n):
                P[i + 1][j + 1] = P[i][j + 1] + P[i + 1][j] - P[i][j] + elixir[i][j]
        self.P = P

    def query(self, r1: int, c1: int, r2: int, c2: int) -> int:
        P = self.P
        return P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1]


# numpy 版本（需要安装 numpy）：二维前缀和 = 先沿列累加，再沿行累加
#
#     import numpy as np
#
#     class ElixirMapNumpy:
#         def __init__(self, elixir):
#             P = np.array(elixir).cumsum(axis=0).cumsum(axis=1)
#             self.P = np.pad(P, ((1, 0), (1, 0)))      # 上方和左边各补一圈 0
#
#         def query(self, r1, c1, r2, c2):
#             P = self.P
#             return int(P[r2 + 1][c2 + 1] - P[r1][c2 + 1] - P[r2 + 1][c1] + P[r1][c1])


if __name__ == "__main__":
    s = ElixirMapStd([[3, 0, 1, 4], [5, 6, 3, 2], [1, 2, 0, 1], [4, 1, 0, 5]])
    assert [s.query(1, 1, 2, 2), s.query(0, 0, 1, 1), s.query(0, 0, 3, 3)] == [11, 14, 38]
    print("标准写法也通过 ✅")
