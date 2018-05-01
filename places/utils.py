from collections import deque


def topological_sort_shapes(places) -> list:
    # construct dependency graph
    graph = {place.id: [] for place in places}
    index = {place.id: place for place in places}
    for place in places:
        for other_place in places:
            if place is not other_place and place.shape.within(other_place.shape):
                graph[other_place.id].append(place.id)

    # topological sort
    order, enter, state = deque(), set(graph), {}

    def dfs(node):
        state[node] = 0
        for k in graph.get(node, ()):
            sk = state.get(k, None)
            if sk == 0:
                raise ValueError("cycle")
            if sk == 1:
                continue
            enter.discard(k)
            dfs(k)
        order.appendleft(node)
        state[node] = 1

    while enter:
        dfs(enter.pop())

    return [index[pk] for pk in order]
