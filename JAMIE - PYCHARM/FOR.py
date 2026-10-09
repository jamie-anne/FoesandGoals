
num = int(input("Enter a number: "))
for x in range(1,11,1):
    print(num,"x",x,"=",num*x)
    x += 1


sum = 0
for x in range(1,21,1):
    if x % 2 == 0:
        sum += x
print("The sum of even numbers from 1 to 20 is: ",sum)


for x in range(1,3,1): #row
    for y in range(1,5,1): #column
        print("*",end="")
    print(" ")

num= int(input("Enter limit: "))
sum = num + 2
for x in range(2,sum,2):
    print(x,end=" ")


num = int(input("Enter a number: "))
tot = 1
for x in range(num,0,-1):
    tot *= x
print(tot)


row= int(input("Enter a number of rows: "))
column = int(input("Enter a number of columns: "))
for x in range(1,row +1):
    for y in range(1,column +1):
        print(y, end=" ")
    print( )
















