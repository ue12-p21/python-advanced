#
# parsing
#

def parse_graph1(filename: str):
    """
    parse the input file and builds a graph

    Parameters:
      filename: the input file path from current directory

    Returns:
      corresonding graph implemented as a dictionary of
      adjacency dictionaries
    """
    g = dict()
    with open(filename) as feed:
        for line in feed:
            src, dst, weight = line.split(',')
            src = src.strip()
            dst = dst.strip()
            weight = int(weight.strip())
            # cannot reference g[src]
            # if that key does not yet exist
            if src not in g:
                g[src] = {}
            g[src][dst] = weight
    return g


from collections import defaultdict

def parse_graph2(filename):
    """
    same as parse_graph1 but using a defaultdict
    """
    g = defaultdict(dict)
    with open(filename) as feed:
        for line in feed:
            src, dst, weight = line.split(',')
            src = src.strip()
            dst = dst.strip()
            weight = int(weight.strip())
            g[src][dst] = weight
    return g


#
# number of vertices
#

def number_vertices1(graph):
    vertices = set()
    for s, adj in graph.items():
        vertices.add(s)
        for d, w in adj.items():
            vertices.add(d)
    return len(vertices)


#
# reachables
#

def reachables1(graph, s):
    """
    computes the set of reachable vertices in a graph from source s

    Parameters:
      graph: a graph implemented as a dict of adjacency dicts
      s: the source vertex
    Returns:
      a set of vertices in graph
    """
    reached = {s}
    while True:
        # have we found anything new in this loop iteration ?
        news = set()
        for v in reached:
            # beware that not all vertices have a key in the dict
            if not v in graph:
                continue
            adj = graph[v]
            for next, _ in adj.items():
                if next not in reached:
                    news.add(next)
        if not news:
            return reached
        else:
            reached.update(news)


#
# shortest path
#

# for math.inf - infinity
import math

def shortest_distance1(graph, v1, v2):
    """
    this function computes the length of the shortest path
    in graph between v1 and v2

    Parameters:
      graph: a graph described as a dictionary of dictionaries
      v1: the source vertex
      v2: the destination vertex
    Returns:
      int: the length of the shortest path, or None
    """

    visited = {v1: 0}

    while True:
        edges = {(s, d)
                 for s, adj in graph.items()
                 for (d, w) in adj.items()
                 if s in visited and d not in visited}

        # out of luck, no path can be found
        if not edges:
            return None

        # find the best tuple (edge, distance)
        shortest_length = math.inf
        shortest_edge = None
        for (s, d) in edges:
            w = graph[s][d]
            dist = visited[s] + w
            if dist <= shortest_length:
                shortest_length = dist
                shortest_edge = (s, d)

        # mark newly selected vertex
        best_src, best_dst = shortest_edge
        visited[best_dst] = shortest_length

        # are we done ?
        if best_dst == v2:
            return shortest_length

def shortest_path1(graph, v1, v2):
    """
    same, but also computes shortest path
    in addition to shortest distance

    * use a comprehension to compute fitting edges
    * returns a tuple (distance, path)
    """

    visited = {v1: (0, None)}

    while True:
        edges = set()
        for (s, adj) in graph.items():
            for (d, w) in adj.items():
                if s in visited and d not in visited:
                    edges.add((s, d))
        # print(f"{edges=}")

        # out of luck, no path can be found
        if not edges:
            return None

        # find the best tuple (edge, distance)
        shortest_length = math.inf
        shortest_edge = None
        for (s, d) in edges:
            w = graph[s][d]
            past_distance, _ = visited[s]
            dist = past_distance + w
            if dist <= shortest_length:
                shortest_length = dist
                shortest_edge = (s, d)

        # mark newly selected vertex
        best_src, best_dst = shortest_edge
        visited[best_dst] = (shortest_length, best_src)

        # are we done ?
        if best_dst == v2:
            path = [v2]
            previous = best_src
            while previous:
                # print(f"inserting {previous}")
                path.insert(0, previous)
                previous = visited[previous][1]
            return shortest_length, path



def shortest_path2(graph, v1, v2):
    """
    like shortest_path1, but more efficient
    as it maintains the border incrementally
    """

    # keep track of what has been visited
    # with what distance, and from what vertex
    visited = {v1: (0, None)}
    # the edges at the border between
    # the visited and unvisited parts
    border_edges = set()
    # the vertex that was just selected
    selected_vertex = v1

    while True:
        # add to the border the edges that
        # go out of the last selected vertex
        # to unvisited
        # print(f"{selected_vertex=}")
        adj = graph.get(selected_vertex, {})
        for (dest, weight) in adj.items():
            if dest not in visited:
                border_edges.add((selected_vertex, dest))
        # remove from the border any edge that would
        # end at the newly_elected vertex
        border_edges = {
            (s, d) for (s, d) in border_edges
            if d != selected_vertex
        }
        # print(f"{border_edges=}")

        # out of luck, no path can be found
        if not border_edges:
            print("no edges")
            return None

        # find the best tuple (edge, distance)
        shortest_length = math.inf
        shortest_edge = None
        for (s, d) in border_edges:
            w = graph[s][d]
            past_distance, _ = visited[s]
            dist = past_distance + w
            if dist <= shortest_length:
                shortest_length = dist
                shortest_edge = (s, d)

        # mark newly selected vertex
        best_src, best_dst = shortest_edge
        visited[best_dst] = (shortest_length, best_src)
        selected_vertex = best_dst

        # are we done ?
        if best_dst == v2:
            path = [v2]
            previous = best_src
            while previous:
                # print(f"inserting {previous}")
                path.insert(0, previous)
                previous = visited[previous][1]
            return shortest_length, path


# for tests
def shortest_distance2(*args):
    try:
        d, path = shortest_path2(*args)
        return d
    except TypeError:
        return None

#
# utility
#

def to_graphviz(graph, engine='dot'):
    """
    converts a graph implemented as a dict of dicts
    into a graphviz object that can be automatically
    displayed in the notebook
    """
    try:
        import graphviz
        gv = graphviz.Digraph(engine=engine)
        for s, adj in graph.items():
            for d, w in adj.items():
                gv.edge(s, d, label=str(w))
        return gv
    except Exception as exc:
        print("oops:", exc)

###
def planar1(n):
    G = {}
    for i in range(1, n+1):
        for j in range(1, n+1):
            G[(i, j)] = {}
            if i < n:
                G[(i, j)][(i+1, j)] = i
            if j < n:
                G[(i, j)][(i, j+1)] = j
    return G
