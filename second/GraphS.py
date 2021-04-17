from graphviz import Digraph


def setGraph():
    g = Digraph('G', filename='second.gv')

    handle1 = open("trueURL.log", "r")
    c = []
    for line in handle1:
        if line:
            c.append(line.split("\n")[0].split(" ")[0])
    handle1.close()

    handle2 = open("crawlers.log", "r")
    c = set(c)
    crawler = {}
    for line in handle2:
        if line:
            line1 = line.split("\n")[0]
            if not line1.split(" ")[4] in crawler.keys():
                crawler[line1.split(" ")[4]] = []
            crawler[line1.split(" ")[4]].append((line1.split(" ")[0], line1.split(" ")[2]))
    handle2.close()

    connects = {}
    connectsN = {}
    for i in crawler.keys():
        arr = crawler[i]
        print(arr)
        print()
        ch = []
        for j in arr:
            link1 = j[0]
            link2 = j[1]
            if not (link1 in connectsN.keys()):
                if not (link1 in connects.keys()):
                    connects[link1] = []
                connects[link1].append(link2)
                ch.append(link1)


        for j in set(ch):
            connectsN[j] = 1

    for i in connects.keys():
        for j in connects[i]:
            if (i in c) and (j in c):
                g.edge(i, j)


    g.view()


setGraph()
