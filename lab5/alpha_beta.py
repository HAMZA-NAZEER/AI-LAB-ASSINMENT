# Lab 5: Alpha-Beta Pruning
# Artificial Intelligence Lab

leaf_count = 0


def alpha_beta(depth, index, is_max, scores, target_depth, alpha, beta):
    global leaf_count

    # Stop when we reach a leaf node
    if depth == target_depth:
        leaf_count += 1
        return scores[index]

    if is_max:
        best_value = float("-inf")

        for child in range(2):
            value = alpha_beta(
                depth + 1, index * 2 + child, False,
                scores, target_depth, alpha, beta
            )
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)

            if alpha >= beta:
                break

        return best_value

    best_value = float("inf")

    for child in range(2):
        value = alpha_beta(
            depth + 1, index * 2 + child, True,
            scores, target_depth, alpha, beta
        )
        best_value = min(best_value, value)
        beta = min(beta, best_value)

        if alpha >= beta:
            break

    return best_value


if __name__ == "__main__":
    scores = [3, 5, 2, 9, 3, 5, 2, 9]
    depth = 3

    result = alpha_beta(
        0, 0, True, scores, depth,
        float("-inf"), float("inf")
    )

    print("Alpha-Beta Result:", result)
    print("Leaves Evaluated:", leaf_count)
