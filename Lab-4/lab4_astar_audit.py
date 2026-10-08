import heapq

graph = {
    "S": [("A", 1), ("B", 4)],
    "A": [("C", 2)],
    "B": [("G", 5)],
    "C": [("G", 3)],
    "G": []
}

heuristic = {"S": 5, "A": 4, "B": 4, "C": 2, "G": 0}

def search(graph, h, start="S", goal="G"):
    pq = [(h[start], 0, start, [start])]
    best = {start: 0}
    processed = []
    expanded = []
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if g != best.get(node):
            continue
        processed.append(node)
        if node == goal:
            return g, path, processed, expanded
        expanded.append(node)
        for nxt, w in graph.get(node, []):
            ng = g + w
            if ng < best.get(nxt, float("inf")):
                best[nxt] = ng
                heapq.heappush(pq, (ng + h[nxt], ng, nxt, path + [nxt]))
    return None, None, processed, expanded

def show(label, h):
    cost, path, processed, expanded = search(graph, h)
    print(label)
    print("Path:", " -> ".join(path))
    print("Cost:", cost)
    print("Processed:", processed)
    print("Expanded:", expanded)
    print("Expansion count:", len(expanded))
    print()

print("A* manual first values:")
for node, g, h, f in [("S",0,5,5),("A",1,4,5),("C",3,2,5)]:
    print(f"{node}: g={g}, h={h}, f={f}")

show("A* with supplied heuristic", heuristic)
show("UCS (zero heuristic)", {k: 0 for k in heuristic})

over = heuristic.copy()
over["C"] = 10
show("A* with overestimate h(C)=10", over)
