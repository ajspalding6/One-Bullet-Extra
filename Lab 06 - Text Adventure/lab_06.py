

class Room:
    def __init__(self, description, north, east, south, west):
        self.description = description
        self.north = north
        self.east = east
        self.south = south
        self.west = west


def main():
    # North, East, South, West
    room_list = []
    # 0
    room = Room("You are in the conservatory. There is a room to your North and East.", None, 18, None, None)
    room_list.append(room)

    # 1
    room = Room("1", None, 17, None, None)
    room_list.append(room)

    # 2
    room = Room("You are in the billiard room. THere is a room to your North, South, and East.", 3, 30, None, None)
    room_list.append(room)

    # 3
    room = Room("3 ", 4, 28, None, None)
    room_list.append(room)

    # 4
    room = Room("You are in the library. There is a room to your North, South, and East.", None, 27, 3, None)
    room_list.append(room)

    # 5
    room = Room(" 5", 6, 24, None, None)
    room_list.append(room)

    # 6
    room = Room("You are in the study. There is a room to your South and East.", None, None, 5, None)
    room_list.append(room)

    # 7
    room = Room("7 ", None, 8, 21, None)
    room_list.append(room)

    # 8
    room = Room("You are in the hall. There is a room to your West and East.", None, None, 22, 7)
    room_list.append(room)

    # 9
    room = Room("9 ", None, None, 23, None)
    room_list.append(room)

    # 10
    room = Room("You are in the lounge. There is a room to your West, and South.", None, None, 11, None)
    room_list.append(room)

    # 11
    room = Room("11 ", 10, None, 12, 23)
    room_list.append(room)

    # 12
    room = Room("You are in the dining room. There is a room to your North, South, and East.", 11, None, None, 26)
    room_list.append(room)

    # 13
    room = Room("13 ", None, None, 14, 32)
    room_list.append(room)

    # 14
    room = Room("You are in the kitchen. There is a room to your North, and West.", 13, None, None, None)
    room_list.append(room)

    # 15
    room = Room("15 ", 32, None, None, 16)
    room_list.append(room)

    # 16
    room = Room("You are in the ball room. There is a room to your West, East, and North", 31, 15, None, 18)
    room_list.append(room)

    # 17
    room = Room("17", 19, None, 18, 1)
    room_list.append(room)

    # 18
    room = Room("18", 17, 16, None, 0)
    room_list.append(room)

    # 19
    room = Room("19", 30, None, 17, None)
    room_list.append(room)

    # 20
    room = Room("20 ", 25, 34, 29, 27)
    room_list.append(room)

    # 21
    room = Room(" 21", 7, 22, 24, None)
    room_list.append(room)

    # 22
    room = Room(" 22", 8, 23, 25, 21)
    room_list.append(room)

    # 23
    room = Room("23 ", 9, 11, 26, 25)
    room_list.append(room)

    # 24
    room = Room(" 24", 21, 25, 27, 5)
    room_list.append(room)

    # 25
    # room = Room(" 25", 22, 26, 20, 24)
    # room_list.append(room)

    # 26
    room = Room(" 26", 23, None, 34, 25)
    room_list.append(room)

    # 27
    room = Room("27 ", 24, 20, 28, 4)
    room_list.append(room)

    # 28
    room = Room("28 ", 27, 29, 30, 3)
    room_list.append(room)

    # 29
    room = Room("29 ", 20, 33, 31, 28)
    room_list.append(room)

    # 30
    room = Room("30", 28, 31, 19, 2)
    room_list.append(room)

    # 31
    room = Room(" 31", 29, 32, 16, 30)
    room_list.append(room)

    # 32
    room = Room(" 32", 33, 13, 15, 31)
    room_list.append(room)

    # 33
    room = Room("33 ", 34, None, 32, 29)
    room_list.append(room)

    # 34
    room = Room(" 34", 26, 12, 33, 20)
    room_list.append(room)

    current_room = 0
    next_room = 0
    done = False

    while not done:
        room_choice = input(f"\n{room_list[current_room].description} \n\nWhich direction do you want to go? ").lower()

        if room_choice[0] == 'n':
            next_room = room_list[current_room].north
        elif room_choice[0] == 'w':
            next_room = room_list[current_room].west
        elif room_choice[0] == 's':
            next_room = room_list[current_room].south
        elif room_choice[0] == 'e':
            next_room = room_list[current_room].east
        elif room_choice[0] == 'q':
            print("You have quit")
            break
        else:
            print("Please pick a valid direction \nDirection: ")
            continue

        if next_room is None:
            print("You can't go that way!\n")
            continue

        current_room = next_room

main()
