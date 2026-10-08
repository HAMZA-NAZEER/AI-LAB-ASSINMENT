# lab1_compare.py
# A small demonstration that conversational fluency is not proof of general intelligence.

examples = [
    ("Fluent but incorrect", "What is 17 x 19?", "The system gives a confident but incorrect answer."),
    ("Reliable task check", "Verify the arithmetic with an independent calculator/program.", "The result can be checked against a deterministic computation.")
]

for title, task, observation in examples:
    print(title)
    print("Task:", task)
    print("Observation:", observation)
    print()
