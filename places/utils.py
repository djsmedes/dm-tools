from collections import deque

from base.models import Profile
from .models import Place


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


def get_topo_sorted_place_list(owner: Profile) -> list:
    polygons = topological_sort_shapes(
        Place.objects.filter(_dimensions=2).filter(owner=owner)
    )
    return polygons + list(
        Place.objects.filter(_dimensions__lt=2).filter(owner=owner)
    )
