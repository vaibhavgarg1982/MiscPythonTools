# graph = {'A': ['B', 'C'],
#             'B': ['C', 'D'],
#             'C': ['D'],
#             'D': ['C'],
#             'E': ['F'],
#             'F': ['C']}

graph1= {'A':['B'], 'B':['C'], 'C':['A'] }  
# DAG = {'A':['B','C'], 'B':['E','F'],'C':['D','E'],'D':['F'], 'E':['F'], 'F':['G']} 
DAGX = {'A':['B1', 'B2', 'B3'],
        'B1':['C1','C2', 'C3'],
        'B2':['C1','C2', 'C3'],
        'B3':['C1','C2', 'C3'],
        'C1':['D1','D2', 'D3'],
        'C2':['D1','D2', 'D3'],
        'C3':['D1','D2', 'D3'],
        'D1':['E'],
        'D2':['E'],
        'D3':['E']
}

duration = {'A':1,
        'B1':2,
        'B2':3,
        'B3':4,
        'C1':5,
        'C2':6,
        'C3':7,
        'D1':8,
        'D2':9,
        'D3':10,
        'E' :0
}



def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        print(f"{start} is hanging (seems to have no successors)")
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths

def find_critical(paths):
    maxpath =[]
    maxdur = 0
    for path in paths:
        sum = 0
        for node in path:
            sum+=(duration[node])
        print(f"{path=} {sum=}")
        if sum>maxdur:
            maxdur = sum
            maxpath = path
    print(f"{maxpath=} {maxdur=}")


# test on various DAGs
paths = (find_all_paths(graph1,"A", "D"))
print(paths)
print("____________________________________") 
find_critical(paths)
pass 