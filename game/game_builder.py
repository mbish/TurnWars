from game.game_engine import Game


class GameBuilder:
    def __init__(self, board_factory, scenario_builder, creation_class=Game):
        self.board_factory = board_factory
        self.scenario_builder = scenario_builder
        self.creation_class = creation_class

    def create_game(self, board_name):
        board = self.board_factory.create(board_name)
        scenario = self.scenario_builder.get_instance()
        return self.creation_class(board, scenario)

    def get_scenario_builder(self):
        return self.scenario_builder
