'''
for i in range(1,100,1):
    if  i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)


numbers = [1,2,3,4,5,6,7,8,9]
num = 0
for number in numbers:
    if number > 0:
        num = number
print(num)


for i in range(1, 6):
    num = int(input("Enter a number: "))
nums = 0
if num > 0:
    nums = num
print("The largest number is: ",num)


row = int(input("Enter a number: "))
column = int(input("Enter a number: "))

for x in range(1,row + 1,1): #row
    for y in range(1,column + 1,1): #column
        print("*",end="")
    print(" ")



for i in range(1,4,1):
    for j in range(1,4,1):
        print("*", end="")
    print(" ")

'''

import random
choices = ["bato","gunting","papel","bato","gunting","papel","bato","gunting","papel"]
user_score = 0
computer_score = 0
for round in range (1,6):
    print(" ")
    print(f"Round: {round}")
    user = input("Choose your attack (bato, gunting, papel): ")
    if user not in  choices:
        print("Piliin mo kung ano yung nasa choices!")
        continue

    computer = random.choice(choices)
    print(f"Computer choose: {computer}")

    match user:
        case "bato":
            if computer == "bato":
                print("Tie lang")
            elif computer == "gunting":
                print("Wow panalo!")
                user_score += 1
            elif computer == "papel":
                print("Oops talo ka HAHA.")
                computer_score += 1

        case "gunting":
            if computer == "bato":
                print("Sige nga guntingin mo yung bato")
                computer_score += 1
            elif computer == "gunting":
                print("Okay fine.")
            elif computer == "papel":
                print("Ouch naman")
                user_score += 1

        case "papel":
            if computer == "bato":
                print("Aray ko")
                user_score += 1
            elif computer == "gunting":
                print("Gupit ka sakin bro")
                computer_score += 1
            elif computer == "papel":
                print("Sa basurahan tayong dalawa")

print(" ")
print("SCORE")
print(f"USER: {user_score} | COMPUTER: {computer_score}")
if user_score > computer_score:
    print("==========Final Result==========")
    print("You won the game!")
elif user_score < computer_score:
    print("==========Final Result==========")
    print("You lose :(")
else:
    print("==========Final Result==========")
    print("Tie")































