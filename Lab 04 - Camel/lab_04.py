""" There is a lot of commented out code because there was a point where everything worked and I went to tweak the code
but that messed everything up. I wanted to leave it all here, so you could see what I've done so far. I got myself in
too deep and tried making it too complicated, but I didn't know how to un-complicate it but still keep it working.
There are a few bugs, but it should run almost completely fine, the only thing that doesn't work is the oasis test.
I put probably about 25 hours into this because I wanted it to be perfect and act like a real game but that failed,
and now I sometimes does not even work properly."""


import time
import random

canteen_level = 3
thirst = 0
native_distance = 0
native_zero = -20
camel_fatigue = 0
distance_traveled = 0
distance_zero = 0
dots = "..."


def main():
    global canteen_level, thirst, native_zero, native_distance, \
        distance_zero, distance_traveled, camel_fatigue, dots

    valid_input = False
    yes_no = "xxxxxxxxxxxxxx" # yes_no needed to be assigned a value and I chose one that had a very
    # small chance of being typed
    Done = False
    Died = False
    print("Welcome to the camel game.\n" + dots)
    print("You have stolen sacred treasure from a group of natives.\n" + dots)
    print("You have to escape by crossing a 200 mile dessert on your camel.\n" + dots)
    print("Based on your choices you could either make it to safety or be caught \n" + dots, "\n\t\tChoose wisely...")
    time.sleep(2) # The time.sleeps' are to allow the user to read the text before it flies by
    print("To choose your fate, type the letter of the choice you wish to make\n")
    while not Done:
        # while not valid_input: I tried to test for an invalid input but it would sometimes create an infinite loop
        time.sleep(2)
        print("\nA. Drink from your canteen")
        print("B. Ahead at moderate speed")
        print("C. Ahead at full speed")
        print("D. Stop for the night")
        print("E. Status check")
        print("Q. Quit\n")

        user_choice = input("What do you chose? ")
        # Quit option

        # Drink water
        if user_choice.upper() == "A":
            choice_a()
            valid_input = True

        # Moderate speed
        elif user_choice.upper() == "B":
            choice_b()
            valid_input = True

        # Full speed
        elif user_choice.upper() == "C":
            choice_c()
            valid_input = True

        # Sleep for the night
        elif user_choice.upper() == "D":
            choice_d()
            valid_input = True

        # Status check
        elif user_choice.upper() == "E":
            choice_e()
            valid_input = True

        # Quit option
        if user_choice.upper() == "Q":
            print(f"You have Quit")

            valid_input = True
            Done = True

        elif not valid_input:
            print(f"You have entered an invalid input, please choose one of the choices above")



        if native_distance <= 0:
            print("The natives caught you!\nGame Over")
            Done = True
            Died = True

        if distance_zero >= 200:
            print("You made it across the dessert! The natives have retreated")
            Done = True
            Died = False

        if thirst >= 6:
            died_of_thirst()
            Done = True
            Died = True

        if camel_fatigue >= 10 and not Died:
            camel_needs_rest()

        if (native_distance < 15) and (native_distance > 0) and (yes_no.upper != "Q"):
            a = True
        else:
            a = False

        if a:
            print(f"The natives are getting close!")

        #if Done or Died:
            #play_again()

        #found_oasis()
def choice_a(): # Drink water
    global canteen_level, thirst, native_zero, native_distance, distance_zero, distance_traveled, camel_fatigue
    canteen_level = canteen_level - 1
    thirst = 0
    if canteen_level > 0:
        print(f"You have {canteen_level} levels of water left")
    elif canteen_level < 0:
        print("You are out of water!")


def choice_b(): # Ahead at moderate speed
    global canteen_level, thirst, native_zero, native_distance, distance_zero, distance_traveled, camel_fatigue, Done
    rand_om = random.randint(5, 12)
    moving(rand_om)

    return native_zero, native_distance, distance_traveled, thirst, distance_zero, camel_fatigue


def choice_c(): # Ahead at full speed
    global canteen_level, thirst, native_zero, native_distance, distance_zero, distance_traveled, camel_fatigue
    rand_om = random.randint(10, 20)
    moving(rand_om)

    return native_zero, native_distance, distance_traveled, thirst, distance_zero, camel_fatigue


def choice_d(): # Rest for the night
    global canteen_level, thirst, native_zero, native_distance, distance_zero, distance_traveled, camel_fatigue
    camel_fatigue = 0
    thirst = 0
    native_distance -= random.randint(7, 14)
    native_distance = abs(native_distance)
    print(f"You rested for the night. \nYour thirst is {thirst}\nYour camel fatigue is {camel_fatigue}")
    print(f"Your camel is rested and happy")
    print(f"The natives are {native_distance} miles behind you")
    return native_distance


def choice_e(): # Prints status check
    global canteen_level, thirst, native_zero, native_distance, distance_zero, distance_traveled, camel_fatigue
    print(f"Your thirst level is {thirst}")
    print(f"Your camels fatigue level is {camel_fatigue}")
    print(f"The natives are {native_distance} miles behind you")
    print(f"You have traveled {distance_traveled} miles")
    print(f"Your canteen has {canteen_level} levels of water")
    time.sleep(5)


def camel_needs_rest():
    global camel_fatigue, native_distance, native_zero, thirst, dots
    print(f"\n{dots}Your camel is tired! You need to rest or your camel will die{dots}\n")
    rand_om = random.randint(7, 14)
    native_distance -= rand_om
    print(
        f"\nYou rested for the night. Your camel is no longer tired.\nThe natives moved {rand_om} miles and are "
        f"{native_distance} miles behind you")
    print(f"Your camel is rested and happy")
    camel_fatigue = 0
    thirst = 0
    return camel_fatigue, thirst


def died_of_thirst():
    global thirst, Done, Died
    Done = True
    Died = True
    print(f"You died of thirst!")


"""def reset_game(): If the user chose to play again this would reset the game
    global canteen_level, thirst, native_zero, Done, native_distance, distance_zero, \
        distance_traveled, camel_fatigue, dots, Died
    Done = False
    Died = False
    thirst = 0
    canteen_level = 3
    native_zero = -20
    native_distance = 0
    distance_zero = 0
    distance_traveled = 0
    camel_fatigue = 0
    print(f"Resetting game...\n{dots}\n{dots}\n{dots}")
    return canteen_level, thirst, native_zero, Done, native_distance, \
        distance_zero, distance_traveled, camel_fatigue, Died"""


def moving(rand_om): # Calculates movement and distance each turn
    global canteen_level, thirst, native_zero, native_distance, distance_zero, distance_traveled, camel_fatigue
    Done = False
    camel_fatigue = camel_fatigue + random.randint(0, 3)
    i = 0
    thirst += 1
    print(f"Your thirst level is {thirst}")

    if thirst >= 5:
        print("You died of thirst")
        Done = True
    distance_zero = distance_zero + rand_om # Calculates the players distance from zero
    distance_traveled = rand_om # Calculates the miles travelled each turn
    camel_fatigue += 1
    native_zero += random.randint(7, 14) # Calculates the miles the natives travel each turn and add it to what they
    # already travelled
    native_distance = distance_zero - native_zero # Calculates the natives distance from the player
    native_distance = abs(native_distance) # Assigns it as absolute value since
    # the natives distance will be negative sometimes
    native_zero = abs(native_zero)
    print(f"Your camel fatigue is {camel_fatigue}")
    print(f"You travelled {distance_traveled} miles")
    print(f"The natives are {native_distance} miles behind you")
    time.sleep(2)

    return camel_fatigue, thirst, native_distance, distance_zero, Done

"""def play_again(): I tried to allow the player the option to play again whenever they quit or died
    yes_no = input("Would you like to play again?\n(Y)es\n(N)o\n")
    valid_input = False

    if yes_no.upper() == "Y":
        Done = False
        valid_input = True
        reset_game()

    elif yes_no.upper() == "N":
        valid_input = True
        Done = True

    while not valid_input:
        print(f"You entered an invalid input. Please enter one of the selections above")
        yes_no = input("Would you like to play again?\n(Y)es\n(N)o\n")
        valid_input = True
        if yes_no.upper() == "Y":
            Done = False
            print(Done)
            valid_input = True
            reset_game()
        elif yes_no.upper() == "N":
            valid_input = True
            Done = True
            print(Done)
        else:
            valid_input = False

    return Done, valid_input """

"""def found_oasis(): # This created an infinite loop and I have no idea why
    global thirst, camel_fatigue
    number = random.randrange(19)
    if number == 1:
        print(f"You found an oasis!")
        thirst = 0
        camel_fatigue = 0
        number = 0

    return thirst, camel_fatigue"""

main()
