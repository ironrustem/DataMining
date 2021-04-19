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


# g-graph
# url-this url
# level-level deep
# url1-past url, use for path in graph
def parseLinks(logger, urlSite, level, urlPast):
    idP = str(uuid.uuid4())
    level += 1
    page = requests.get(urlSite)
    paragraphs = re.findall(r'<a(.*?) href="(.*?)"', str(page.content))
    n = 0
    threads = []
    n6 = []

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



            n6.append(linkAdd)

    for i in n6:
        if (level <= 4) and not (urlSite == i) and not (i in urlPast):
            print(i)
            ulrPast1 = urlPast.copy()
            ulrPast1.append(urlSite)
            x = threading.Thread(target=parseLinks, args=(logger, i, level, ulrPast1))
            n += 1
            x.start()
            threads.append(x)

        if i in urlPast:
            urlPast.append(urlSite)
            for j in range(len(urlPast) - 1):
                url1 = urlPast[j].replace("https://", "").replace("http://", "")
                url1 = url1.replace("www.", "").split("?")[0]
                url2 = urlPast[j+1].replace("https://", "").replace("http://", "")
                url2 = url2.replace("www.", "").split("?")[0]
                logger.debug(url1 + " = " + url2 + " = " + idP)

    for i in range(len(threads)):
        threads[i].join()


def main():
    f = open('crawlers.log', 'w+')
    f.seek(0)
    f.close()
    logger = logger_connect()
    parseLinks(logger, url, 0, [])


url = 'https://www.vk.com'
main()

