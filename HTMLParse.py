import urllib.request
from bs4 import BeautifulSoup
import queue


class Node:
    def __init__(self, url, parent):
        self.url = url
        self.parent = parent

    def __geturl__(self):
        return self.url

    def __getchildren__(self):
        return self.children

    def __setchildren__(self, children):
        self.children = children


class Parse:
    def __init__(self):
        url = "http://2007.runescape.wikia.com/wiki/Ancient_Cavern"
        completed = [url.split(".com", 1)[1]]
        node = Node(url, None)
        children = self.get_linked(url)
        node.__setchildren__(children)
        self.q = queue.Queue()
        self.q.put(node)
        domain = "http://2007.runescape.wikia.com"
        while not self.q.empty():
            node = self.q.get()
            completed = list(set(completed))
            completed.append(node.__geturl__().split(".com", 1)[1])
            print(node.__geturl__())
            for child in node.__getchildren__():
                temp = Node(domain + child, node)
                children = self.get_linked(domain + child)
                temp.__setchildren__((set(children) - set(node.__getchildren__())) - set(completed))
                print(temp.__geturl__())
                self.q.put(temp)

    def get_linked(self, url):
        current_page = url.split("/wiki/", 1)[1]
        f = urllib.request.urlopen(url)
        stream = f.read()
        output = stream.decode("utf8")
        f.close()
        x = BeautifulSoup(output, "html.parser").find('div', attrs={'id': 'WikiaArticle'})
        children = []
        if x is not None:
            for a in x.find_all('a', href=True):
                if "/wiki/" in a['href'] and 'http' not in a['href'] and current_page not in a['href'] and ':' not in a[
                    'href']:
                    children.append(a['href'])  # .replace("%27", "'"))
        return set(children)


parse = Parse()
