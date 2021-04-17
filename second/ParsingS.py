import re
import threading
import logging
import uuid
import requests


def logger_connect():
    logger1 = logging.getLogger("logger_connect")
    logger1.setLevel(logging.DEBUG)
    fh = logging.FileHandler("crawlers.log")
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    logger1.addHandler(fh)
    return logger1


def logger_n():
    loggerN = logging.getLogger("logger_n")
    loggerN.setLevel(logging.DEBUG)
    fh = logging.FileHandler("trueURL.log")
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    loggerN.addHandler(fh)
    return loggerN


# g-graph
# url-this url
# level-level deep
# url1-past url, use for path in graph
def parseLinks(logger, loggerN, urlSite, level, n5, urlPast):
    idP = str(uuid.uuid4())
    level += 1
    page = requests.get(urlSite)
    paragraphs = re.findall(r'<a(.*?) href="(.*?)"', str(page.content))
    n = 0
    threads = []
    n6 = []
    n5.append(urlSite)

    # print("start: " + urlSite + "  |  n1: " + str(len(paragraphs)))
    for i in paragraphs:
        linkAdd = str(i[len(i) - 1])
        if linkAdd.endswith("/"):
            linkAdd = linkAdd[:-1]
        if linkAdd.startswith("."):
            linkAdd = linkAdd[1:]

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

            url1 = urlSite.replace("https://", "").replace("http://", "")
            url1 = url1.replace("www.", "").split("?")[0]
            url2 = linkAdd.replace("https://", "").replace("http://", "")
            url2 = url2.replace("www.", "").split("?")[0]
            logger.debug(url1 + " = " + url2 + " = " + idP)

            n6.append(linkAdd)

    for i in n6:
        if (level <= 3) and not (urlSite == i) and not (i in n5):
            print(i)
            ulrPast1 = urlPast.copy()
            ulrPast1.append(urlSite)
            x = threading.Thread(target=parseLinks, args=(logger, loggerN, i, level, n5, ulrPast1))
            n += 1
            x.start()
            threads.append(x)

        if i in n5:
            urlPast.append(urlSite)
            for j in urlPast:
                url1 = j.replace("https://", "").replace("http://", "")
                url1 = url1.replace("www.", "").split("?")[0]
                loggerN.debug(url1)

    for i in range(len(threads)):
        threads[i].join()


def main():
    f = open('crawlers.log', 'w+')
    f.seek(0)
    f.close()

    f = open('trueURL.log', 'w+')
    f.seek(0)
    f.close()

    logger = logger_connect()
    loggerN = logger_n()
    parseLinks(logger, loggerN, url, 0, [], [])


url = 'https://www.vk.com'
main()
