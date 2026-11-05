# Lab 5: Minimax and Alpha-Beta Comparison

from minimax import minimax
import minimax as minimax_module
from alpha_beta import alpha_beta
import alpha_beta as alpha_beta_module


def run_comparison(scores):
    depth = 3

    minimax_module.leaf_count = 0
    minimax_result = minimax(0, 0, True, scores, depth)
    minimax_leaves = minimax_module.leaf_count

    alpha_beta_module.leaf_count = 0
    alpha_beta_result = alpha_beta(
        0, 0, True, scores, depth,
        float("-inf"), float("inf")
    )
    alpha_beta_leaves = alpha_beta_module.leaf_count

    print("Scores:", scores)
    print()
    print("Minimax Result:", minimax_result)
    print("Minimax Leaves Evaluated:", minimax_leaves)
    print()
    print("Alpha-Beta Result:", alpha_beta_result)
    print("Alpha-Beta Leaves Evaluated:", alpha_beta_leaves)
    print()

    if minimax_result == alpha_beta_result:
        print("Check: Both algorithms give the same result.")
    else:
        print("Check: Results are different. Please check the code.")

    print("Leaves Saved:", minimax_leaves - alpha_beta_leaves)


if __name__ == "__main__":
    # Main test from the lab task
    run_comparison([3, 5, 2, 9, 3, 5, 2, 9])

    # A second test with a different order of leaf values
    print("\nSecond Test (different leaf order)")
    run_comparison([9, 3, 5, 2, 9, 3, 5, 2])
