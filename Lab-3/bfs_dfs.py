from collections import deque

graph = {
    "A": ["B","C"],
    "B": ["D","E"],
    "C": ["F"],
    "D": [],
    "E": ["G"],
    "F": [],
    "G": []
}

def bfs(start, goal):
    q=deque([(start,[start])]); seen={start}; trace=[]
    while q:
        node,path=q.popleft(); trace.append((node,list(q),path))
        if node==goal: return path,trace
        for n in graph[node]:
            if n not in seen:
                seen.add(n); q.append((n,path+[n]))
    return None,trace

def dfs(start, goal):
    stack=[(start,[start])]; seen=set(); trace=[]
    while stack:
        node,path=stack.pop()
        if node in seen: continue
        seen.add(node); trace.append((node,list(stack),path))
        if node==goal: return path,trace
        for n in reversed(graph[node]):
            if n not in seen: stack.append((n,path+[n]))
    return None,trace

if __name__=="__main__":
    for name,fn in [("BFS",bfs),("DFS",dfs)]:
        path,trace=fn("A","G")
        print(name,"path:",path)
        print(name,"visit order:",[x[0] for x in trace])
        for x in trace: print(" processed=",x[0],"frontier=",x[1],"path=",x[2])
