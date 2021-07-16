
pathtree
=============================

pathtree implements a tree for fast path lookup.

------------
Build Guide
------------
How to build a package:

    https://packaging.python.org/tutorials/packaging-projects/

Make the .whl:

    python setup.py sdist bdist_wheel

Get the .whl in:

    ./dist/pathtree-0.0.7-py2.py3-none-any.whl

------------
Installation
------------

From PyPI

    pip install pathtree.0.0.7.wheel

From Anaconda (conda forge)

    none for now

From source code

    cd pathtree-source-code-path
    python setup.py install



-----
Usage
-----

```python
from pathtree import Tree
if __name__ == '__main__':
    t = Tree()
    t.Add("/", 1)
    t.Add("/a", 2)
    t.Add("/a", 3)
    t.Add("/a", 4, extra_data={"test": "just a test"})
    t.Add("/a/b", 5)
    t.Add("/a/b/c", 6)

    leafs = t.Find("/a")
    if leafs:
        print("found all leafs of path /a -> %s" % leafs)

    leaf = t.FindLeaf("/a", 2)
    if leaf:
        print("found leaf: /a -> %s" % leaf.value)
    
    leaf = t.FindLeaf("/a", 4)
    if leaf:
        print("found leaf: /a -> %s" % leaf.value)
        print("            /a -> leaf.extra_data" % leaf.extra_data)

    node = t.FindPath("/a/b")
    if node:
        print("found path /a/b -> %s" % node)

    t.DeleteLeaf("/a", 2)
    leaf = t.FindLeaf("/a", 2)
    if not leaf:
        print("leaf /a -> 2 has been deleted")

    t.DeletePath("/a/b")
    node = t.FindPath("/a/b")
    if not node:
        print("path /a/b has been deleted")

    node = t.FindPath("/a/b/c")
    if not node:
        print("path /a/b/c has been deleted")
```

Features
=========

 - Restrictions
   - Paths must be a '/'-separated list of strings, like a URL or Unix filesystem.
   - All paths must begin with a '/'.
   - Path elements may not contain a '/'.
   - Trailing slashes are inconsequential.

 - Algorithm
    - Paths are mapped to the tree in the following way:
        - Each '/' is a Node in the tree. The root node is the leading '/'.
        - Each Node has edges to other nodes. The edges are named according to the possible path elements at that depth in the path.
        - Any Node may have an associated Leaf.  Leafs are terminals containing the data associated with the path as traversed from the root to that Node.

    - Edges are implemented as a map from the path element name to the next node in the path.
    
    - Extra_data is an optional information for every edge or leaf

