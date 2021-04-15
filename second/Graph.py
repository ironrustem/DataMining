from graphviz import Digraph


def setGraph():
    g = Digraph('G', filename='second.gv')

    handle1 = open("threading.log", "r")
    connect = {}
    for line in handle1:
        if line:
            if line.split("\n")[0].split(" ")[0] in connect.keys():
                connect[line.split("\n")[0].split(" ")[0]].append(line.split("\n")[0].split(" ")[2])
            else:
                connect[line.split("\n")[0].split(" ")[0]] = []
                connect[line.split("\n")[0].split(" ")[0]].append(line.split("\n")[0].split(" ")[2])
    handle1.close()

    handle2 = open("threadingN.log", "r")
    for line in handle2:
        if line:
            if int(line.split("\n")[0].split(" ")[2]) > 0:
                con = connect[line.split("\n")[0].split(" ")[0]]
                for i in con:
                    g.edge(line.split("\n")[0].split(" ")[0], i)
    handle2.close()

    g.view()



setGraph()
