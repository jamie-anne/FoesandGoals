tasks = {}


while True:
    print("__MENU___________________")
    print(" [ 1 ] ADD")
    print(" [ 2 ] DISPLAY")
    print(" [ 3 ] MARK AS DONE")
    print(" [ 4 ] REMOVE")
    print(" [ 5 ] SEARCH")
    print(" [ 6 ] EXIT")
    choice = int(input("Enter your choice: "))

    if choice == 1:
        print(" ")
        print("___ADD___________________")
        many = int(input("How many task do you want to add: "))
        i = 1
        while i <= many:
            status = "Pending"
            task = input("Enter task: ")
            tasks[task] = status
            i += 1
        print("Task Added!")
        print(" ")
    elif choice == 2:
        print(" ")
        print("___DISPLAY___________________")
        print(tasks)
        print(" ")
    elif choice == 3:
        print(" ")
        print("___MARK AS DONE___________________")
        mark_as_done = input("Enter the task: ")
        if mark_as_done in tasks:
            status = "Done"
            tasks[mark_as_done] = status
            print("Task Mark As Done!")
            print(" ")
        else:
            print("Task Not Found")
            print(" ")
    elif choice == 4:
        print(" ")
        print("___REMOVE___________________")
        remove = input("Enter the task: ")
        del tasks[remove]
        print("Task Removed!")
        print(" ")
    elif choice == 5:
        print(" ")
        print("___SEARCH___________________")
        search = input("Enter the task: ")
        if search in tasks:
            print("Task Searched!")
            print(" ")
        else:
            print("Task Not Found")
            print(" ")
    elif choice == 6:
        print(" ")
        print("Have a great day!")
        exit()


x = 1
print("Value of x is ", x)
x += 2
print("Value of x is ", x)
x += 3
print("Value of x is ", x)
x += 4
print("Value of x is ", x)


name = "Jamie Anne Banjola"
address = "San Lorenzo Gapan City, Nueva Ecija"
section = "BSIT-2A"
print("Name: ",name)
print("Address: ",address)
print("Section: ",section)

num1 = 55
num2 = 66
num3 = 77
print("First number is: ", num1)
print("Second number is: ", num2)
print("Third number is: ", num3)
sum = num1 + num2 + num3
print("Sum: ", sum)
















