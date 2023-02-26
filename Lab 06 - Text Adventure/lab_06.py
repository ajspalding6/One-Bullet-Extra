def main():
    room_list = (Conservatory, BilliardRoom, Library, Study, Hall, Lounge, DiningRoom, Kitchen, BallRoom)
    room = Room()
    room.description = "You are in the conse"
    pass


class Room:
    def __init__(self, description, north, east, south, west):
        self.description = ""
        self.north = 0
        self.east = 0
        self.south = 0
        self.west = 0


class Conservatory:
    pass


class BilliardRoom:
    pass


class Library:
    pass


class Study:
    pass


class Hall:
    pass


class Lounge:
    pass


class DiningRoom:
    pass


class Kitchen:
    pass


class BallRoom:
    pass
