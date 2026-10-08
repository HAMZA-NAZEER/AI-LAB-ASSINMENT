import heapq

# Controlled weighted extension of the original graph.
# Added corridor C -> G. Weights are nonnegative travel-cost units.
graph = {
    "A":[("B",1),("C",2)],
    "B":[("D",1),("E",1)],
    "C":[("F",0),("G",10)],
    "D":[],
    "E":[("G",1)],
    "F":[],
    "G":[]
}

def bfs_weighted(start,goal):
    from collections import deque
    q=deque([(start,[start])]); seen={start}
    while q:
        node,path=q.popleft()
        if node==goal: return path
        for n,w in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n,path+[n]))
    return None

def ucs(start,goal):
    pq=[(0,start,[start])]; best={start:0}; processed=[]
    while pq:
        cost,node,path=heapq.heappop(pq)
        if cost!=best.get(node): continue
        processed.append(node)
        if node==goal: return path,cost,processed
        for nxt,w in graph[node]:
            nc=cost+w
            if nc<best.get(nxt,float("inf")):
                best[nxt]=nc; heapq.heappush(pq,(nc,nxt,path+[nxt]))
    return None,float("inf"),processed

def path_cost(path):
    total=0
    for a,b in zip(path,path[1:]):
        total += dict(graph[a])[b]
    return total

if __name__=="__main__":
    bp=bfs_weighted("A","G"); print("BFS:",bp,"cost:",path_cost(bp))
    up,uc,order=ucs("A","G"); print("UCS:",up,"cost:",uc,"processed:",order)
