# lab2_percepts.py
PEAS = {
    "Delivery Robot": {
        "Performance": ["fast delivery", "correct destination", "collision avoidance", "low energy use"],
        "Environment": ["roads/sidewalks", "buildings", "pedestrians", "obstacles"],
        "Actuators": ["wheels", "steering", "brakes", "delivery compartment"],
        "Sensors": ["camera", "GPS", "ultrasonic/LiDAR", "wheel/odometry sensors"]
    },
    "LLM Student Support Agent": {
        "Performance": ["correct answers", "helpful responses", "fast response", "privacy-aware behavior"],
        "Environment": ["students", "course information", "university policies", "approved learning material"],
        "Actuators": ["text responses", "notifications", "approved search/API requests"],
        "Sensors": ["student questions", "uploaded documents", "approved university data", "approved search results"]
    }
}
for agent, spec in PEAS.items():
    print("\n", agent)
    for k,v in spec.items(): print(k, ":", ", ".join(v))
