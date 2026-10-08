# lab2_model.py
# Stateful control agent: remembers the previous target mode.
def target_mode(temperature, occupied, previous_mode=None):
    if occupied and temperature > 25:
        target = "COOL"
    elif occupied and temperature < 18:
        target = "HEAT"
    elif not occupied:
        target = "OFF"
    else:
        target = "IDLE"
    send_command = target != previous_mode
    return target, send_command

def run_trace(percepts):
    previous = None
    for i, (temp, occupied) in enumerate(percepts, 1):
        target, send = target_mode(temp, occupied, previous)
        print(f"{i}: previous={previous}, percept=(temp={temp}, occupied={occupied}), target={target}, "
              f"{'COMMAND' if send else 'NO-COMMAND'}")
        previous = target

if __name__ == "__main__":
    run_trace([(27, True), (27, True), (16, True), (16, True), (22, True), (22, False)])
