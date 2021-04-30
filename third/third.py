import random
from time import sleep


def setRandom():
    sleep(0.2)
    ran = random.randint(0, 1000)
    return ran


def setRandomArray(c):
    ran = []
    for j in range(c):
        sleep(0.2)
        ran1 = random.randint(0, len(base) - 1)
        ran.append([ran1, 0])
    return ran


def getBin(n5):
    b = 2147483648;
    str5 = ''
    while b > 0:
        z = n5 & b
        if z == 0:
            str5 = str5 + '0'
        else:
            str5 = str5 + '1'
        b = b >> 1
    return str5


def zero_moment(arr):
    max1 = -1
    max2 = -1
    for x1 in arr:
        x2 = ((3 * x1) + 1) % 1001
        if x2 > max2:
            x3 = "" + str(getBin(x2))
            check = False
            n2 = 0
            for i1 in range(len(x3)):
                if check:
                    max1 = max(n2, max1)
                    max2 = pow(2, max1)
                    break
                i2 = len(x3) - i1 - 1
                if x3[i2] == "1":
                    check = True
                else:
                    n2 += 1
    return max2


def addToSecond(x1, n1):
    for j in setFor2a1:
        if j[0] >= n1:
            if base[x1] == base[j[0]]:
                j[1] += 1
    for j in setFor2b1:
        if j[0] >= n1:
            if base[x1] == base[j[0]]:
                j[1] += 1


def getSecond(g):
    sumG = 0
    if g == "a":
        for j in setFor2a1:
            sumG += ((2 * j[1]) - 1) * n
        return sumG / a
    else:
        for j in setFor2b1:
            sumG += ((2 * j[1]) - 1) * n
        return sumG / b


def forPrint(finish):
    if finish:
        print(
            f'\r zero: {str(zero_moment(base))}   first: {str(len(base))}   secondA: {getSecond("a")}   secondB: {getSecond("b")}',
            end="", flush=True)
    else:
        print(
            f'\r zero: {str(zero_moment(base))}   first: {str(len(base))}',
            end="", flush=True)


base = []
n = 0
sumN = 0
while True:
    n += 1
    x = setRandom()

    sumN1 = sumN + x
    if sumN1 > 1000000:
        break

    base.append(x)
    sumN = sumN1
    if n % 10 == 0:
        forPrint(False)

a = 100
b = 500
setFor2a1 = setRandomArray(a)
setFor2b1 = setRandomArray(b)

n2 = 0
for i in base:
    addToSecond(i, n2)
    n += 1

h = 1000000 - sumN
base.append(h)
addToSecond(x, n2 + 1)
forPrint(True)
