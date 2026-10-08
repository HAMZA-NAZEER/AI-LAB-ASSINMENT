# lab2_check.py
from lab2_model import target_mode

cases = [
    (27, True, None), (27, True, "COOL"),
    (18, True, "HEAT"), (17, True, "HEAT"),
    (25, True, "COOL"), (22, False, "IDLE")
]
for c in cases:
    print(c, "->", target_mode(*c))
