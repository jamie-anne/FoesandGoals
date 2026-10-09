
# number pattern
num = int(input("Enter a number: "))
x = 1
while x <= num:
    y = 1
    while y <= x:
        print(y, end=" ")
        y += 1
    print( )
    x += 1

#Asterisk pattern
#num = int(input("Enter a number: "))
x = 1
y = 5
j = 1
while x <= y:
    print(y * " ",j * "*")
    y -= 1
    j += 2

#total numbers
sum = 0
i = 1
while i <= 4:
    numm = int(input("Enter a number: "))
    sum += numm
    i += 1
print("Total sum: ",sum)

#Countdown
num = int(input("Enter starting number: "))
x = 1
while num >= x:
    print(num)
    num -= 1
else:
    print("Time's up!")


# Reverse digits of a number using while loop
num = int(input("Enter a number: "))
rev = 0

while num > 0:
    digit = num % 10
    rev = rev * 10 + digit
    num //= 10
print("Reversed:", rev)

# Count digits of a number using while loop
num = int(input("Enter a number: "))
count = 0

if num == 0:
    count = 1
else:
    while num > 0:
        num //= 10
        count += 1
print("Number of digits:", count)

#full block
x = 5
i = 1
while i <= x:
    print("*" * x)
    i+=1


#hollow square
rows = 5
i = 1
while i <= rows:
    if i == 1 or i == rows:
        print("*" * rows)   # full row
    else:
        print("*" + "   " + "*")  # hollow middle
    i += 1


#pattern asterisk
x = 5
i = x
while i >= 0:
    print(" " * (x-i) + "*" * i)
    i -= 1


x = 5
i = x
while i >= 1:
    print(" " * (x - i) + "*" * (2 * i - 1))
    i -= 1

i = 2
while i <= x:
    print(" " * (x - i) + "*" * (2 * i - 1))
    i += 1

x = 5
i = x
while i >= 1:
    print(i)
    i -= 1























