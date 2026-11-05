# Lab 5: Adversarial Search — Minimax and Alpha-Beta Pruning

**Course:** Artificial Intelligence Lab  
**Lab:** 5  
**Topic:** Minimax and Alpha-Beta Pruning

## Objective

The purpose of this lab is to use Minimax and Alpha-Beta Pruning on a small game tree. The programs find the best value for the MAX player while assuming that the MIN player also makes the best possible decision.

## Files

- `minimax.py` — Runs the Minimax algorithm and counts evaluated leaf nodes.
- `alpha_beta.py` — Runs Alpha-Beta Pruning and counts evaluated leaf nodes.
- `comparison.py` — Runs both algorithms and compares their results.

## Requirements

- Python 3
- No external Python libraries are required.

## How to Run

Open a terminal in this project folder and run:

```bash
python minimax.py
python alpha_beta.py
python comparison.py
```

## Main Test

The first test uses these leaf values:

`[3, 5, 2, 9, 3, 5, 2, 9]`

Both algorithms should return the same root value. Alpha-Beta Pruning may evaluate fewer leaf nodes because it skips branches that cannot affect the final decision.

## What I Learned

- MAX selects the largest available value.
- MIN selects the smallest available value.
- Minimax works from the leaf nodes towards the root.
- Alpha-Beta Pruning uses alpha and beta bounds to skip unnecessary branches.
- The order of branches can affect how many leaves are pruned, but it should not change the Minimax result.

## Testing Note

I used two leaf-value orders in `comparison.py`. Run the program and check the printed results. Add your own screenshot of the output to the repository after running the files.

## Reflection

After running the programs, write a few lines here in your own words about what you observed. For example, mention whether both algorithms returned the same value and whether the number of evaluated leaves changed.
