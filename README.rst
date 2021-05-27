pathtree
========

pathtree implements a tree for fast path lookup.

+--------------+
| Build Guide  |
+==============+
| How to build |
| a package:   |
+--------------+
| https://pack |
| aging.python |
| .org/tutoria |
| ls/packaging |
| -projects/   |
+--------------+
| Make the     |
| .whl:        |
+--------------+
| python       |
| setup.py     |
| sdist        |
| bdist\_wheel |
+--------------+
| Get the .whl |
| in：         |
+--------------+
| ./dist/patht |
| ree-0.0.1-py |
| 2.py3-none-a |
| ny.whl       |
+--------------+

Installation
------------

From PyPI

::

    pip install pathtree.0.0.1.wheel

From Anaconda (conda forge)

::

    none for now

From source code

::

    cd pathtree-source-code-path
    python setup.py install

+---------+
| Usage   |
+---------+

.. code:: python

       from pathtree import Tree

       if __name__ == '__main__':
            t = Tree()
            t.Add("/", 1)
            t.Add("/a", 2)
            t.Add("/a/b", 3)

            leaf, _ = t.Find("/a")
            if leaf:
                print(leaf.Value)

            exist, v = t.Get("/a")
            if exist:
                print(v)

Features
========

-  Restrictions
-  Paths must be a '/'-separated list of strings, like a URL or Unix
   filesystem.
-  All paths must begin with a '/'.
-  Path elements may not contain a '/'.
-  Path elements beginning with a ':' or '\*' will be interpreted as
   wildcards.
-  Trailing slashes are inconsequential.

-  Wildcards

   -  Wildcards are named path elements that may match any strings in
      that location. Two different kinds of wildcards are permitted:
   -  :var - names beginning with ":" will match any single path
      element.
   -  \*var - names beginning with "\*" will match one or more path
      elements.
      ``(however, no path elements may come after a star wildcard)``

-  Extensions

   -  Single element wildcards in the last path element can optionally
      end with an extension. This allows for routes like
      '/users/:id.json', which will not conflict with '/users/:id'.

-  Algorithm

   -  Paths are mapped to the tree in the following way:

      -  Each '/' is a Node in the tree. The root node is the leading
         '/'.
      -  Each Node has edges to other nodes. The edges are named
         according to the possible path elements at that depth in the
         path.
      -  Any Node may have an associated Leaf. Leafs are terminals
         containing the data associated with the path as traversed from
         the root to that Node.

   -  Edges are implemented as a map from the path element name to the
      next node in the path.
