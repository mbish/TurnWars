class TypeType:
    cover = 0
    passable_movement_types = {}
    event_names = {}
    def __init__(self, cover, passable_movement_types, event_names):
        self.cover = cover
        self.passable_movement_types = passable_movement_types 
        self.event_names = event_names
