# Lab 5: Minimax Algorithm
# Artificial Intelligence Lab

leaf_count = 0


def minimax(depth, index, is_max, scores, target_depth):
    global leaf_count

    # Stop when we reach a leaf node
    if depth == target_depth:
        leaf_count += 1
        return scores[index]

    if is_max:
        left_value = minimax(depth + 1, index * 2, False, scores, target_depth)
        right_value = minimax(depth + 1, index * 2 + 1, False, scores, target_depth)
        return max(left_value, right_value)

    left_value = minimax(depth + 1, index * 2, True, scores, target_depth)
    right_value = minimax(depth + 1, index * 2 + 1, True, scores, target_depth)
    return min(left_value, right_value)


if __name__ == "__main__":
    scores = [3, 5, 2, 9, 3, 5, 2, 9]
    depth = 3

    result = minimax(0, 0, True, scores, depth)

    print("Minimax Result:", result)
    print("Leaves Evaluated:", leaf_count)
