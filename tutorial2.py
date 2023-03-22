##T2.1
# for x in range(1900,2021):
#     if x%4 == 0 and x%100 != 0:
#         print(x, end =" ")
#     elif x%400 == 0:
#         print(x, end=" ")

##T2.2
# import random
# sum = 0
# count = 1
# while sum <= 1000 and count <= 100:
#     x = random.randint(1, 20)
#     print(x)
#     sum = sum + x
#     count += 1
#     if count > 100:
#         print("count exceeded")
# print("sum:", sum)
# print ("count number:", count)

##Discussion 2
# password = input("Enter Password: ")
# upcase = False
# lowcase = False
# digit = False
# for char in password:
#     if char.isupper():
#         upcase = True
#     if char.islower():
#         lowcase = True
#     if char.isdigit():
#         digit = True
# length = len(password)
# strong = upcase and lowcase and digit and length > 7
# if strong:
#     print("password is strong")
# else:
#     print("password is weak")

##Exercise - percentage of a string
# str = input("Enter a string:")
# percentage = int((input("Enter percentage:")))
# num = int((percentage/100) * len(str))
# print(str[:num])

##Exercise - alphabet check




















