from graphviz import Digraph


def setGraph():
    g = Digraph('G', filename='second.gv')

    # handle1 = open("threading.log", "r")
    # connect = {}
    # for line in handle1:
    #     if line:
    #         if not line.split("\n")[0].split(" ")[0] in connect.keys():
    #             connect[line.split("\n")[0].split(" ")[0]] = []
    #         connect[line.split("\n")[0].split(" ")[0]].append(line.split("\n")[0].split(" ")[2])
    # handle1.close()

    handle2 = open("threading.log", "r")
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
            # print("link1: " + link1 + " link2: " + link2)
            if not (link1 in connectsN.keys()):
                if not (link1 in connects.keys()):
                    connects[link1] = []
                connects[link1].append(link2)
                ch.append(link1)


        for j in set(ch):
            connectsN[j] = 1

    for i in connects.keys():
        for j in connects[i]:
            g.edge(i, j)


    g.view()


setGraph()
