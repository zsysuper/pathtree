# -*- coding: utf-8 -*-
import pprint
import logging

printer = pprint.PrettyPrinter(indent=2)


class Leaf(object):
    def __init__(self, value, wildcards, order):
        self.Value = value
        self.Wildcards = wildcards
        self.order = order


def Tree(logger=logging):
    return Node({}, {}, None, {}, None, 0, logger)


class Node(object):
    def __init__(self, edges, wildcard, leaf,
                 extensions, star, leafs=0, logger=logging):
        self.edges = edges
        self.wildcard = wildcard
        self.leaf = leaf
        self.extensions = extensions
        self.star = star
        self.leafs = leafs
        self.logger = logger

    def Add(self, key, val):
        if not key or not key.startswith('/'):
            self.logger.error("Path must begin with /")
            return None, "Path must begin with /"
        self.leafs += 1
        return self.add(self.leafs, self.splitPath(key), [], val=val)

    def addLeaf(self, leaf):
        extension = self.stripExtensionFromLastSegment(leaf.Wildcards)
        if extension != "":
            if extension in self.extensions:
                self.logger.error("duplicate path")
                return "duplicate path"
            self.extensions[extension] = leaf
            return ""

        if self.leaf:
            self.logger.error("duplicate path")
            return "duplicate path"
        self.leaf = leaf
        return ""

    def add(self, order, elements, wildcards, val):
        if len(elements) == 0:
            self.logger.debug("Add Leaf: %s %s %s" % (val, wildcards, order))
            leaf = Leaf(val, wildcards, order)
            return self.addLeaf(leaf)

        el, elements = elements[0], elements[1:]
        if el == "":
            self.logger.error("empty path elements are not allowed")
            return "empty path elements are not allowed"

        if el[0] == ":":
            if not self.wildcard:
                self.wildcard = Node({}, {}, None, {}, None, 0)
            wildcards.append(el[1:])
            return self.wildcard.add(order, elements, wildcards, val)
        elif el[0] == "*":
            if self.star:
                self.logger.error("duplicate path")
                return "duplicate path"
            wildcards.append(el[1:])
            self.star = Leaf(val, wildcards, order)
            return ""
        try:
            e = self.edges[el]
        except Exception as _:
            e = Node({}, {}, None, {}, None, 0)
            self.edges[el] = e
            self.logger.debug(
                "--------------- add order: %d, elements: %s, wildcaard: %s, val: %s" % (
                    order, elements, wildcards, val))
        return e.add(order, elements, wildcards, val)

    def Find(self, key):
        if len(key) == 0 or key[0] != "/":
            return None, None
        return self.find(self.splitPath(key), list())
    
    def Get(self, key):
        leaf, _ = self.Find(key)
        if leaf:
            return True, leaf.Value
        return False, None

    def find(self, elements, exp):
        leaf = None
        expansions = list()
        if len(elements) == 0:
            if len(exp) > 0 and self.extensions:
                lastExp = exp[len(exp) - 1]
                prefix, extension = self.extensionForPath(lastExp)
                if extension in self.extensions:
                    leaf = self.extensions[extension]
                    if leaf:
                        exp[len(exp) - 1] = prefix
                        return leaf, self.listUnique(exp)
            return self.leaf, self.listUnique(exp)

        starExpansion = ""
        if self.star:
            starExpansion = "/".join(elements)

        el, elements = elements[0], elements[1:]
        if el in self.edges:
            nextNode = self.edges[el]
            if nextNode:
                leaf, expansions = nextNode.find(elements, self.listUnique(exp))

        if self.wildcard:
            exp.append(el)
            wildcardLeaf, wildcardExpansions = self.wildcard.find(elements,
                                                                  self.listUnique(
                                                                      exp))
            if wildcardLeaf and (not leaf or leaf.order > wildcardLeaf.order):
                leaf = wildcardLeaf
                expansions = wildcardExpansions

        if self.star and (not leaf or leaf.order > self.star.order):
            leaf = self.star
            expansions = expansions + exp + [starExpansion]

        return leaf, self.listUnique(expansions)

    @staticmethod
    def extensionForPath(path):
        try:
            dotPosition = path.rindex(".")
            if dotPosition != -1:
                return path[:dotPosition], path[dotPosition:]
        except Exception as e:
            return "", ""

    @staticmethod
    def splitPath(key):
        elements = key.split("/")
        if elements[0] == "":
            elements = elements[1:]
        if elements[len(elements) - 1] == "":
            elements = elements[:len(elements) - 1]
        return elements

    def stripExtensionFromLastSegment(self, segments):
        if len(segments) == 0:
            return ""
        lastSegment = segments[len(segments) - 1]
        prefix, extension = self.extensionForPath(lastSegment)
        if extension != "":
            segments[len(segments) - 1] = prefix
        return extension

    @staticmethod
    def showObj(obj):
        printer.pprint(obj.__dict__)

    @staticmethod
    def listUnique(v):
        if not v:
            return list()
        v_unique = list(set(v))
        v_unique.sort(key=v.index)
        return v_unique


def found(n, p, expectedExpansions, val):
    leaf, expansions = n.Find(p)
    if not leaf:
        print("Didn't find: %s" % p)
        return False
    expansions.sort()
    expectedExpansions.sort()
    if expansions != expectedExpansions:
        print("%s: Wildcard expansions (actual) %s != %s (expected)" % (
            p, expansions, expectedExpansions))
        return False
    if leaf.Value != val:
        print("%s: Value (actual) %s != %s (expected)" % (p, leaf.Value, val))
        return False
    return True


def notfound(n, p):
    leaf, _ = n.Find(p)
    if leaf:
        print("Should not have found: %s" % p)
        return False
    return True


def TestColon():
    print("\n============ TestColon ============")
    n = Tree()

    n.Add("/:first/:second/", 1)
    n.Add("/:first", 2)
    n.Add("/", 3)

    found(n, "/", [], 3)
    found(n, "/a", ["a"], 2)
    found(n, "/a/", ["a"], 2)
    found(n, "/a/b", ["a", "b"], 1)
    found(n, "/a/b/", ["a", "b"], 1)
    found(n, "/a/c/", ["a", "c"], 1)

    notfound(n, "/a/b/c")


def TestStar():
    print("\n============ TestStar ============")
    n = Tree()

    n.Add("/first/second/*star", 1)
    n.Add("/:first/*star/", 2)
    n.Add("/*star", 3)
    n.Add("/", 4)

    found(n, "/", [], 4)
    found(n, "/a", ["a"], 3)
    found(n, "/a/", ["a"], 3)
    found(n, "/a/b", ["a", "b"], 2)
    found(n, "/a/b/", ["a", "b"], 2)
    found(n, "/a/b/c", ["a", "b/c"], 2)
    found(n, "/a/b/c/", ["a", "b/c"], 2)
    found(n, "/a/b/c/d", ["a", "b/c/d"], 2)
    found(n, "/first/second", ["first", "second"], 2)
    found(n, "/first/second/", ["first", "second"], 2)
    found(n, "/first/second/third", ["third"], 1)


def TestMixedTree():
    print("\n============ TestMixedTree ============")
    n = Tree()

    n.Add("/", 0)
    n.Add("/path/to/nowhere", 1)
    n.Add("/path/:i/nowhere", 2)
    n.Add("/:id/to/nowhere", 3)

    n.Add("/:a/:b", 4)
    n.Add("/not/found", 5)

    found(n, "/", [], 0)
    found(n, "/path/to/nowhere", [], 1)
    found(n, "/path/to/nowhere/", [], 1)
    found(n, "/path/from/nowhere", ["from"], 2)
    found(n, "/walk/to/nowhere", ["walk"], 3)
    found(n, "/path/to/", ["path", "to"], 4)
    found(n, "/path/to", ["path", "to"], 4)
    found(n, "/not/found", ["not", "found"], 4)
    notfound(n, "/path/to/somewhere")
    notfound(n, "/path/to/nowhere/else")
    notfound(n, "/path")
    notfound(n, "/path/")

    notfound(n, "")
    notfound(n, "xyz")
    notfound(n, "/path//to/nowhere")


def TestExtensions():
    print("\n============ TestExtensions ============")
    n = Tree()

    n.Add("/:first/:second.json", 1)
    n.Add("/a/:second.xml", 2)
    n.Add("/:first/:second", 3)

    found(n, "/a/b", ["a", "b"], 3)
    found(n, "/a/b.json", ["a", "b"], 1)
    found(n, "/a/b.xml", ["b"], 2)
    found(n, "/a/b.c.xml", ["b.c"], 2)
    found(n, "/other/b.xml", ["other", "b.xml"], 3)


if __name__ == "__main__":
    # Testing...
    TestColon()
    TestStar()
    TestMixedTree()
    TestExtensions()
