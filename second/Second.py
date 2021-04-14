import urllib.request
import urllib.parse
import re
import threading
import logging
from graphviz import Digraph


def get_logger():
    logger = logging.getLogger("threading_example")
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("threading.log")
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger


def parseLinks(g, url, level):
    print("start")
    level += 1
    values = {'s': 'pandas',
              'submit': 'search'}
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8')
    req = urllib.request.Request(url, data)
    resp = urllib.request.urlopen(req)
    respData = resp.read()
    paragraphs = re.findall(r'<a href="(.*?)"', str(respData))

    url1 = url.replace("https://", "")
    url2 = str(url1.replace("http://", ""))

    n = 0
    for i in range(len(paragraphs)):
        h = str(paragraphs[i - 1])
        if not h.startswith('#'):
            if h.startswith('http'):
                h1 = h.replace("https://", "")
                h2 = str(h1.replace("http://", ""))

                g.edge(url2, h2)
                if level < 3:
                    n += 1
                    x = threading.Thread(target=parseLinks, args=(g, i, level,))
                    x.start()
                    x.join()

            else:
                l = url + h
                l1 = l.replace("https://", "")
                l2 = str(l1.replace("http://", ""))
                g.edge(url2, l2)
                if level < 3:
                    n += 1
                    x = threading.Thread(target=parseLinks, args=(g, l, level,))
                    x.start()
                    x.join()

    if n > 0:
        logger.debug(url2 + " " + str(n))


def matmult(v, G, b, e):
    result = []
    for i in range(len(G)):
        total = 0
        for j in range(len(G)):
            total += v[j] * G[i][j]
        result.append((b * total) + e)
    return result



g = Digraph('G', filename='second.gv')
f = open('threading.log', 'w+')
f.seek(0)
f.close()
logger = get_logger()
url = 'https://m.vk.com/wrustem'
parseLinks(g, url, 0)
g.view()


handle1 = open("threading.log", "r")
lineLog = []
for line in handle1:
    if line:
        lineLog.append(line)
handle1.close()


links1 = []
for i in lineLog:
    links1.append(i.split("\n")[0].split(" ")[0])
    print(i)
    print(i.split("\n")[0].split(" ")[1])

forNumber = {}
g = 0
for i in links1:
    forNumber[i] = [g, lineLog[g].split("\n")[0].split(" ")[1]]
    g += 1

print("length: " + str(len(forNumber)))
matrix = []
for i in range(len(links1)):
    matrix.append([])
    for i1 in range(len(links1)):
        matrix[i].append(0)


handle = open("second.gv", "r")
data = handle.readline()
lineLog = []
for line in handle:
        line1 = line.split("\n")[0]
        line2 = line1.split(" ")[0]

        line3 = line1.replace('}', '')
        if line3:
            line11 = line3.split(" ")[0]
            line21 = line3.split(" ")[2]

            l1 = line11.replace('\t', '')  # первый линк
            l2 = line21.replace('\t', '')  # второй линк
            l19 = l1.replace('"', '')  # первый линк
            l29 = l2.replace('"', '')  # второй линк


            print("line: " + line)
            print("l19: " + l19)
            print("l29: " + l29)

            if (l19 in forNumber.keys()) and (l29 in forNumber.keys()):
                n1 = forNumber[l19][0]
                n3 = forNumber[l19][1]
                n2 = forNumber[l29][0]
                matrix[n1 - 1][n2 - 1] = matrix[n1 - 1][n2 - 1] + float(1 / int(n3))


handle.close()



v = []
for i in range(len(matrix)):
    v.append(float(1/len(matrix)))


print("11111")
for i1 in range(len(matrix)):
    t = 0
    for j in range(len(matrix[i1])):
        t += matrix[i1][j]
    print(t)

e = float(1 - 0.85) / len(matrix)

v1 = matmult(v, matrix, 0.85, e)
v2 = matmult(v1, matrix, 0.85, e)
v3 = matmult(v2, matrix, 0.85, e)
v4 = matmult(v3, matrix, 0.85, e)
v5 = matmult(v3, matrix, 0.85, e)
#
tot = 0
for i1 in range(len(v4)):
    tot += v4[i1]

print(tot)





