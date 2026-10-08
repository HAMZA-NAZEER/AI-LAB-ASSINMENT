graph={"A":["B","C"],"B":["D","E"],"C":["F"],"D":[],"E":["G"],"F":[],"G":[]}

def dls(start,goal,limit):
    trace=[]
    def rec(node,path,depth):
        trace.append((node,depth,list(path)))
        if node==goal: return ("FOUND",path)
        cutoff=False
        if depth==limit: return ("CUTOFF",None)
        for n in graph[node]:
            if n in path: continue
            status,result=rec(n,path+[n],depth+1)
            if status=="FOUND": return status,result
            if status=="CUTOFF": cutoff=True
        return ("CUTOFF",None) if cutoff else ("FAILURE",None)
    status,path=rec(start,[start],0)
    return status,path,trace

def iddfs(start,goal,max_depth):
    attempts=[]
    for limit in range(max_depth+1):
        status,path,trace=dls(start,goal,limit)
        attempts.append((limit,status,path,trace))
        if status=="FOUND": return status,path,attempts
    return "FAILURE",None,attempts

if __name__=="__main__":
    for limit in [1,2,3,4]:
        status,path,trace=dls("A","G",limit)
        print("DLS limit",limit,":",status,path)
    for maxd in [1,2,3,4]:
        status,path,attempts=iddfs("A","G",maxd)
        print("IDDFS max",maxd,":",status,path,"limits attempted:",[a[0] for a in attempts])
