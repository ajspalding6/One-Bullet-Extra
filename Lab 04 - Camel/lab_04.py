import random
import time

miles_number = 10
miles_travelled = miles_number
thirst = 0
camel_tiredness = 0
native_zero = 0
native_distance = 0
canteen_level = 3
done = False
died = False
valid_input = False


def main():

    global miles_travelled, thirst, native_zero, canteen_level, done, \
        died, camel_tiredness, native_distance, valid_input

    print("Welcome to the camel game.\n")
    print("You have stolen sacred treasure from a group of natives.\n")
    print("You have to escape by crossing a 200 mile dessert on your camel.\n")
    print("Based on your choices you could either make it to safety or be caught\n\n\t\tChoose wisely...")
    print("\nTo choose your fate, type the letter of the choice you wish to make\n")

    while not done:
        valid_input = False  # Declares valid_input as false so that the loop will run if no input is provided
        time.sleep(2)
        print("\nA. Drink from your canteen")
        print("B. Ahead at moderate speed")
        print("C. Ahead at full speed")
        print("D. Stop for the night")
        print("E. Status check")
        print("Q. Quit\n")
        user_choice = input("What do you chose? ")

        if user_choice.upper() == "Q":
            choice_q()

        elif user_choice.upper() == "A":
            choice_a()

        elif user_choice.upper() == "B":
            choice_b()

        elif user_choice.upper() == "C":
            choice_c()

        elif user_choice.upper() == "D":
            choice_d()

        elif user_choice.upper() == "E":
            choice_e()

        elif not valid_input:  # This loops if the input is not A-E or Q
            print(f"You have entered an invalid input. Please enter on of the options above")

        if user_choice.upper != "Q" and not done:
            if miles_travelled >= 220 and not died:
                print(f"You made it safely across the dessert!")
                done = True
                died = False
                if done:
                    valid_input = False
                    while not valid_input:
                        play_again()
                continue
            if thirst > 6:
                print(f"You died of thirst!")
                done = True
                died = True
                if done:
                    valid_input = False
                    while not valid_input:
                        play_again()
                continue
            elif thirst > 4:
                print(f"You are thirsty. You need to drink water soon")
                died = False

            elif camel_tiredness > 8:
                print(f"Your camel died and the natives caught you!\nGame over!")
                done = True
                died = True
                if done:
                    valid_input = False  # valid_input will be declared true in the play_again
                    # function but the loop needs and initial value in order to run
                    while not valid_input:
                        play_again()
                continue
            elif camel_tiredness > 5:
                print(f"Your camel is getting tired!")

        if done:
            valid_input = False
            while not valid_input:
                play_again()
        user_choice = 0


def choice_a():  # Drink water
    global thirst, canteen_level, valid_input
    if canteen_level > 0:
        canteen_level -= 1
        thirst = 0
        print(f"You have {canteen_level} drinks left in your canteen")
    else:
        print(f"You have no more water! You need to find an oasis soon or you will die of thirst")
    valid_input = True
    return thirst, canteen_level, valid_input


def choice_b():  # Ahead at full speed
    global thirst, camel_tiredness, native_distance, native_zero, miles_travelled, valid_input, done, died
    thirst += 1
    number = random.randrange(10, 20)
    camel_tiredness += random.randrange(1, 3)
    miles_travelled += number
    native_zero += random.randrange(7, 14)
    native_distance = miles_travelled - native_zero
    print(f"You travelled {number} miles")
    print(f"The natives are {native_distance} miles behind you")
    found_oasis()
    valid_input = True
    if native_distance <= 0:
        print(f"The natives caught you! Game over!")
        done = True
        died = True
    elif native_distance < 15:
        print("The natives are getting close!")
    return thirst, camel_tiredness, native_distance, native_zero, miles_travelled, valid_input, done, died


def choice_c():  # Ahead at moderate speed
    global thirst, camel_tiredness, native_distance, native_zero, miles_travelled, valid_input, done, died
    thirst += 1
    camel_tiredness += 1
    number = random.randrange(5, 12)
    miles_travelled += number
    native_zero += random.randrange(7, 14)
    native_distance = miles_travelled - native_zero
    print(f"You travelled {number} miles")
    print(f"The natives are {native_distance} miles behind you")
    found_oasis()
    valid_input = True
    if native_distance <= 0:
        print(f"The natives caught you! Game over!")
        done = True
        died = True
    elif native_distance < 15:
        print("The natives are getting close!")
    return thirst, camel_tiredness, native_distance, native_zero, miles_travelled, valid_input, done, died


def choice_d():  # Stop for the night
    global thirst, camel_tiredness, native_distance, native_zero, miles_travelled, valid_input, done, died
    thirst = 0
    camel_tiredness = 0
    native_zero += random.randrange(10, 20)
    native_distance = miles_travelled - native_zero
    print(f"Your thirst level is {thirst}")
    print(f"Your camels tiredness is {camel_tiredness}. Your camel is happy and rested")
    print(f"The natives are {native_distance} miles behind you")
    valid_input = True
    if native_distance <= 0:
        print(f"The natives caught you! Game over!")
        done = True
        died = True
    elif native_distance < 15:
        print("The natives are getting close!")
    return thirst, camel_tiredness, native_distance, native_zero, valid_input, done, died


def choice_e():  # Status check
    global miles_travelled, canteen_level, native_distance, valid_input
    print(f"You have travelled {miles_travelled-miles_number} miles.")
    print(f"You have {canteen_level} drinks in your canteen.")
    print(f"The natives are {native_distance} miles behind you")
    valid_input = True
    return valid_input


def choice_q():  # Quit the game
    global done, valid_input
    print(f"You have quit")
    done = True
    valid_input = True
    return done, valid_input


def found_oasis():  # Chance of finding oasis
    global thirst, canteen_level, camel_tiredness
    if random.randrange(1, 20) == 10:
        print(f"You found an oasis! Your thirst is reset, your canteen is filled, and your camel is rested")
        thirst = 0
        canteen_level = 3
        camel_tiredness = 0

    return thirst, canteen_level, camel_tiredness


def reset_game():  # If the user wants to play again, this will reset the game
    global thirst, camel_tiredness, native_distance, native_zero, \
        miles_travelled, done, died, valid_input, canteen_level, miles_number
    canteen_level = 3
    thirst = 0
    camel_tiredness = 0
    native_zero = 0
    native_distance = 0
    miles_travelled = miles_number
    done = False
    died = False
    valid_input = False
    print("Resetting game...")
    time.sleep(2)
    print("Welcome to the camel game.\n")
    print("You have stolen sacred treasure from a group of natives.\n")
    print("You have to escape by crossing a 200 mile dessert on your camel.\n")
    print("Based on your choices you could either make it to safety or be caught\n\n\t\tChoose wisely...")
    print("\nTo choose your fate, type the letter of the choice you wish to make\n")
    time.sleep(2)
    return thirst, camel_tiredness, native_distance, native_zero, \
        miles_travelled, done, died, valid_input, canteen_level


def play_again():  # This is the input of playing again and testing for a valid input
    global done, valid_input
    valid_input = False
    user_input = input("Would you like to play again?\nY/N ")
    if user_input.upper() == "Y":
        reset_game()
        valid_input = True
    if user_input.upper() == "N":
        done = True
        valid_input = True
    if not valid_input:
        print("You entered an invalid input. Please enter a choice from above")
    return valid_input, done


main()
