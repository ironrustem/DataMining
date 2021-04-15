import urllib.request
from urllib.parse import urlparse
import re
import threading
import logging
from graphviz import Digraph

import requests



def get_logger():
    logger1 = logging.getLogger("threading_example")
    logger1.setLevel(logging.DEBUG)
    fh = logging.FileHandler("threading.log")
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger1.addHandler(fh)
    return logger1


# g-graph
# url-this url
# level-level deep
# url1-past url, use for path in graph
def parseLinks(ng1, g, urlSite, level, urlPast):

    level += 1
    page = requests.get(urlSite)
    paragraphs = re.findall(r'<a href="(.*?)"', str(page.content))
    urlSite1 = urlSite.replace("https://", "")
    urlSite1 = urlSite1.replace("http://", "")
    n = 0
    threads = []

    print("start: " + urlSite + "  |  n1: " + str(len(paragraphs)))
    print()
    for i in range(len(paragraphs)):
        linkAdd = str(paragraphs[i - 1])
        if not linkAdd.startswith('#'):
            if not linkAdd.startswith('http'):
                linkAdd = url + linkAdd
            linkAdd1 = linkAdd.replace("https://", "")
            linkAdd1 = linkAdd1.replace("http://", "")
            if linkAdd1.endswith("/"):
                linkAdd1 = linkAdd1[:-1]
            if urlSite1.endswith("/"):
                urlSite1 = urlSite1[:-1]

            g.edge(urlSite1, linkAdd1)

            if (level < 3) and not (urlSite1 == linkAdd1):
                if (level == 2) and not (urlSite1 in ng):
                    continue
                if linkAdd.endswith("/"):
                    linkAdd = linkAdd[:-1]
                if urlSite.endswith("/"):
                    urlSite = urlSite[:-1]

                x = threading.Thread(target=parseLinks, args=(ng1, g, linkAdd, level, urlSite1,))
                n += 1
                x.start()
                threads.append(x)

    for i in range(len(threads)):
        threads[i].join()

    if n > 0:
        print("n: " + str(n))
        logger.debug(urlSite1)


# multiply matrix
def matrixMultiply(vector, G, b, eVector):
    result = []
    for i1 in range(len(G)):
        total = 0
        for j1 in range(len(G)):
            total += vector[j1] * G[i1][j1]
        result.append((b * total) + eVector)
    return result


def second(g):
    g.view()

    # parse logs
    handle1 = open("threading.log", "r")
    lineLog = []
    for line in handle1:
        if line:
            lineLog.append(line.split("\n")[0].split(" ")[0])
    handle1.close()

    # add number for link
    forNumber = {}
    g = 0
    for i in lineLog:
        forNumber[i] = g
        g += 1

    # add 0 in matrix
    matrix = []
    for i in range(len(lineLog)):
        matrix.append([])
        for i1 in range(len(lineLog)):
            matrix[i].append(0)

    # parse connection between links
    handle = open("second.gv", "r")
    data = handle.readline()
    for line in handle:
        line1 = line.split("\n")[0]
        line1 = line1.replace('}', '')

        if line1:
            line_first = line1.split(" ")[0].replace('\t', '').replace('"', '')
            print("line_first " + line_first)
            print("line1 " + line1)
            line_second = line1.split(" ")[2].replace('\t', '').replace('"', '')

            # add to matrix
            if (line_first in forNumber.keys()) and (line_second in forNumber.keys()):
                n1 = forNumber[line_first]
                n2 = forNumber[line_second]
                matrix[n2 - 1][n1 - 1] = matrix[n2 - 1][n1 - 1] + 1
    handle.close()

    for i3 in range(len(matrix)):
        for j3 in range(len(matrix[i])):
            print(str(matrix[i3][j3]), end=' ')
        print()

    v = []
    for i in range(len(matrix)):
        v.append(float(1 / len(matrix)))

    for i1 in range(len(matrix)):
        t = 0
        for j in range(len(matrix[i1])):
            t += matrix[j][i1]
        print("t: " + str(t))
        for j in range(len(matrix[i1])):
            if (matrix[j][i1] > 0):
                matrix[j][i1] = matrix[j][i1] / t

    for i3 in range(len(matrix)):
        for j3 in range(len(matrix[i])):
            print(str(matrix[i3][j3]), end=' ')
        print()

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
        print(str(v5[i1]))

    print("result: " + str(tot))


# parse links, get links
ng2 = []
g = Digraph('G', filename='second.gv')
f = open('threading.log', 'w+')
f.seek(0)
f.close()
logger = get_logger()
url = 'https://www.google.com'
parseLinks(ng2, g, url, 0, "")
n = 0
second(g)
