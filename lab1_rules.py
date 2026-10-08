# lab1_rules.py
# Rule-based scholarship screening example.
# Thresholds are synthetic lab assumptions.

def evaluate_case(score, complete, attendance, disciplinary_issue):
    reasons = []
    if score < 70:
        reasons.append("score is below 70")
    if not complete:
        reasons.append("application is incomplete")
    if attendance < 75:
        reasons.append("attendance is below 75%")
    if disciplinary_issue:
        reasons.append("disciplinary issue is present")
    passed = not reasons
    return passed, ("All conditions satisfied." if passed else "; ".join(reasons))

tests = [
    {"name":"Pass", "score":85, "complete":True, "attendance":90, "disciplinary_issue":False},
    {"name":"Failure: completeness", "score":85, "complete":False, "attendance":90, "disciplinary_issue":False},
    {"name":"Failure: attendance", "score":85, "complete":True, "attendance":74, "disciplinary_issue":False},
    {"name":"Threshold boundary", "score":70, "complete":True, "attendance":75, "disciplinary_issue":False},
]

if __name__ == "__main__":
    for case in tests:
        result, reason = evaluate_case(case["score"], case["complete"], case["attendance"], case["disciplinary_issue"])
        print(case["name"])
        print("Input:", case)
        print("Expected:", "PASS" if case["name"] in ["Pass","Threshold boundary"] else "FAIL")
        print("Actual:", "PASS" if result else "FAIL")
        print("Reason:", reason)
        print("-"*50)
