# 🏰 部落冲突 · 排序附加挑战：三色军团（三路分区快速排序）
#
# 🔄 进行中（2026-11-08 开始）—— 下面是题目，代码完成后补上
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
# 测试重点：全部相等的 10^5 数组、只有三种值的 10^5 数组、已排序的 10^5 数组
# 知识卡：notes/sorting.md 卡 6
