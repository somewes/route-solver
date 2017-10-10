from graph import State, Edge, RouteSolver, Node


class Mario(State):

    def get_initial_state_data(self):
        return {
            'key1': False,
            'key2': False,
            'speed_booster': False,
            'is_finished': False
        }

    def get_computed_state(self):
        return {
            'key_count': self.get_key_count()
        }

    def get_key_count(self):
        keys = ['key1', 'key2']
        return sum([1 if getattr(self, key) else 0 for key in keys])


all_edges = [
    Edge(
        '1-A',
        '1-B-1',
        default_weight=10,
        weights=[
            (State(speed_booster=True), 5)
        ]
    ),
    Edge(
        '1-B-1',
        '1-C-1',
        default_weight=10,
        weights=[
            (State(speed_booster=True), 5)
        ]
    ),
    Edge(
        '1-B-1',
        '1-D-1',
        default_weight=20,
        weights=[
            (State(speed_booster=True), 10)
        ]
    ),
    Edge(
        '1-B-1',
        '1-E-1',
        default_weight=14,
        weights=[
            (State(speed_booster=True), 7)
        ],
        required_state=State(
            key_count=1
        ),
        state_change=State(
            is_finished=True
        )
    ),
    Edge(
        '1-B-4',
        '1-C-1',
        default_weight=12,
        weights=[
            (State(speed_booster=True), 6)
        ]
    ),
    Edge(
        '1-B-4',
        '1-D-1',
        default_weight=22,
        weights=[
            (State(speed_booster=True), 11)
        ]
    ),
    Edge(
        '1-B-4',
        '1-E-1',
        default_weight=16,
        weights=[
            (State(speed_booster=True), 8)
        ],
        required_state=State(
            key_count=1
        ),
        state_change=State(
            is_finished=True
        )
    ),
    Edge(
        '1-C-1',
        '1-B-4',
        default_weight=10,
        weights=[
            (State(speed_booster=True), 5)
        ],
        state_change=State(
            speed_booster=True
        )
    ),
    Edge(
        '1-D-1',
        '1-A',
        default_weight=10,
        weights=[
            (State(speed_booster=True), 5)
        ],
        state_change=State(
            key1=True
        )
    ),
]


route_solver = RouteSolver(Node.get_or_create('1-A'), Mario())
route_solver.run()
