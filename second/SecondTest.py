from graphviz import Digraph

g = Digraph('G', filename='second.gv')

handle2 = open("threading.log", "r")
for line in handle2:
    print(1)
    if line:
        line1 = line.split("\n")[0].split(" ")
        g.edge(line1[0], line1[2])
handle2.close()

g.view()