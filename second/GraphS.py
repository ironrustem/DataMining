from graphviz import Digraph


def matrixMultiply(vector, G, b, eVector):
    result = []
    for i1 in range(len(G)):
        total = 0
        for j1 in range(len(G)):
            total += vector[j1] * G[i1][j1]
        result.append((b * total) + eVector)
    return result

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

    forNumber = {}
    g1 = 0
    for i in set(c):
        forNumber[i] = g1
        g1 += 1

    # add 0 in matrix
    matrix = []
    for i in range(len(set(c))):
        matrix.append([])
        for i1 in range(len(set(c))):
            matrix[i].append(0)

    for i in connects.keys():
        for j in connects[i]:
            if (i in c) and (j in c):
                g.edge(i, j)

                n1 = forNumber[i]
                n2 = forNumber[j]
                matrix[n1][n2] += 1

    for i3 in range(len(matrix)):
        for j3 in range(len(matrix[i3])):
            print(str(matrix[i3][j3]), end=' ')
        print()

    for i1 in range(len(matrix)):
        t = 0
        for j in range(len(matrix[i1])):
            t += matrix[j][i1]
        print("t: " + str(t))
        for j in range(len(matrix[i1])):
            if (matrix[j][i1] > 0):
                matrix[j][i1] = matrix[j][i1] / t

    for i3 in range(len(matrix)):
        for j3 in range(len(matrix[i3])):
            print(str(matrix[i3][j3]), end=' ')
        print()

    v = []
    for i in range(len(matrix)):
        v.append(float(1 / len(matrix)))

    print("111")
    e = float(1 - 0.85) / len(matrix)
    v1 = matrixMultiply(v, matrix, 0.85, e)
    v2 = matrixMultiply(v1, matrix, 0.85, e)
    v3 = matrixMultiply(v2, matrix, 0.85, e)
    v4 = matrixMultiply(v3, matrix, 0.85, e)
    v5 = matrixMultiply(v4, matrix, 0.85, e)

    tot = 0
    for i1 in range(len(v5)):
        tot += v5[i1]
        print(v5[i1])

    print("result: " + str(tot))

    g.view()


# def pr():


setGraph()
