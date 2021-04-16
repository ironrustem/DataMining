import re
import threading
import logging
import uuid

import requests



def logger_connect():
    logger1 = logging.getLogger("logger_connect")
    logger1.setLevel(logging.DEBUG)
    fh = logging.FileHandler("threading.log")
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger1.addHandler(fh)
    return logger1


def logger_n():
    loggerN = logging.getLogger("logger_n")
    loggerN.setLevel(logging.DEBUG)
    fh = logging.FileHandler("threadingN.log")
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    loggerN.addHandler(fh)
    return loggerN


# g-graph
# url-this url
# level-level deep
# url1-past url, use for path in graph
def parseLinks(logger, loggerN, urlSite, level, n5):
    id = str(uuid.uuid4())
    level += 1

    page = requests.get(urlSite)
    paragraphs = re.findall(r'<a(.*?) href="(.*?)"', str(page.content))

    n = 0
    threads = []


    print("start: " + urlSite + "  |  n1: " + str(len(paragraphs)))

    # for i in paragraphs:
    #     print(paragraphs)

    for i in paragraphs:
        linkAdd = str(i[len(i) - 1])
        print(linkAdd + "  00")
        if linkAdd.endswith("/"):
            linkAdd = linkAdd[:-1]
        if linkAdd.startswith("."):
            linkAdd = linkAdd[1:]
        print(linkAdd + "  01")

        if not linkAdd.startswith('#'):
            if linkAdd.startswith('//'):
                linkAdd = linkAdd[2:]
            if (not linkAdd.startswith('http')) and (not linkAdd.startswith('www')):
                if not linkAdd.startswith("/"):
                    linkAdd = "/" + linkAdd
                linkAdd = url + linkAdd
            if linkAdd.startswith('www'):
                linkAdd = "http://" + linkAdd

            if linkAdd.endswith("/"):
                linkAdd = linkAdd[:-1]
            if urlSite.endswith("/"):
                urlSite = urlSite[:-1]
            linkAdd.replace("..", "")

            print(linkAdd + "  10")
            logger.debug(urlSite.replace("https://", "").replace("http://", "") + " = " + linkAdd.replace("https://", "").replace("http://", "") + " = " + id)
            n5.append(linkAdd)

    for i in n5:
        if (level <= 3) and not (urlSite == i) and not (i in urlSite):
            x = threading.Thread(target=parseLinks, args=(logger, loggerN, i, level, n5))
            n += 1
            x.start()
            threads.append(x)

    loggerN.debug(urlSite.replace("https://", "").replace("http://", "") + " = " + str(n))

    for i in range(len(threads)):
        threads[i].join()


def main():
    f = open('threading.log', 'w+')
    f.seek(0)
    f.close()

    f = open('threadingN.log', 'w+')
    f.seek(0)
    f.close()

    logger = logger_connect()
    loggerN = logger_n()
    url = 'https://www.vk.com'
    parseLinks(logger, loggerN, url, 0, [])


url = 'https://www.vk.com'
main()
