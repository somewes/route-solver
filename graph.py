from copy import copy


class State(object):
    def __init__(self, *args, **kwargs):
        for key, value in self.get_initial_state_data().items():
            setattr(self, key, value)

        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_initial_state_data(self):
        return {}

    def get_state(self):
        state = self.__dict__
        for key, value in self.get_computed_state().items():
            state[key] = value

        return state

    def get_computed_state(self):
        return {}

    def apply_state_change(self, state):
        for key, value in state.get_state().items():
            setattr(self, key, value)

    def has_required_state(self, required_state):
        if not required_state:
            return True

        # Check player state against required state
        state = self.get_state()

        for key, value in required_state.get_state().items():
            if type(value) is bool:
                if value != state[key]:
                    return False
            elif value > state[key]:
                return False

        return True


class Node(object):
    node_map = {}

    def __init__(self, name):
        self.name = name
        self.node_map[self.name] = self

        self.edges = {}

    def add_edge(self, edge):
        """
        :type edge: Edge
        """
        self.edges[edge.end_node] = edge

    def __str__(self):
        return 'Node: {0}'.format(self.name)

    @classmethod
    def get_or_create(cls, name):
        node = cls.node_map.get(name) or Node(name)
        return node


class Edge(object):
    def __init__(self, start_node_name, end_node_name, default_weight, weights, required_state=None, state_change=None):
        self.start_node = Node.get_or_create(start_node_name)
        self.end_node = Node.get_or_create(end_node_name)

        self.start_node.add_edge(self)

        self.default_weight = default_weight
        self.weights = weights

        self.required_state = required_state
        self.state_change = state_change

    def get_weight(self, player):
        lowest_weight = self.default_weight

        for item in self.weights:
            state = item[0]
            weight = item[1]

            if player.has_required_state(state) and weight < lowest_weight:
                lowest_weight = weight

        return lowest_weight

    def __str__(self):
        return '{0} - {1}'.format(self.start_node, self.end_node)


class RouteSolver(object):

    def __init__(self, start_node, player):
        self.start_node = start_node
        self.player = player
        self.successful_routes = []

    def get_available_edges(self, node, player):
        edges = []
        for end_node, edge in node.edges.items():
            if player.has_required_state(edge.required_state):
                edges.append(edge)

        return edges

    def mark_edge_visited(self, edge, player, visited_edges):
        visited_edges.add(frozenset({
            'edge': edge,
            'player': frozenset(player.get_state().items())
        }.items()))

    def edge_visited(self, edge, player, visited_edges):
        return frozenset({
            'edge': edge,
            'player': frozenset(player.get_state().items())
        }.items()) in visited_edges

    def apply_state_change(self, edge, player):
        for key, value in edge.state_change.items():
            setattr(player, key, value)

    def traverse(self, edge=None, player=None, visited_edges=None, current_route=None):
        node = edge.end_node if edge else self.start_node
        player = player or self.player
        visited_edges = visited_edges or set()
        current_route = current_route or []

        if edge:
            self.mark_edge_visited(edge, player, visited_edges)
            if edge.state_change:
                player.apply_state_change(edge.state_change)
            current_route.append([edge, edge.get_weight(player)])

        if player.is_finished:
            self.successful_routes.append(current_route)
            return current_route

        edges = self.get_available_edges(node, player)

        for edge in edges:
            if not self.edge_visited(edge, player, visited_edges):
                self.traverse(edge, copy(player), copy(visited_edges), copy(current_route))

    def run(self):
        self.traverse()

        print 'Total Routes Found:', len(self.successful_routes)
        lowest_weight = None
        best_route = None

        for successful_route in self.successful_routes:
            route_weight = 0
            for item in successful_route:
                weight = item[1]
                route_weight += weight

            if lowest_weight is None or route_weight < lowest_weight:
                lowest_weight = route_weight
                best_route = successful_route

        print 'The best route is {0}'.format(lowest_weight)
        for item in best_route:
            print '- {0}'.format(item[0])
