##T1.1
# Num = int(input("Number: "))
# while Num > 86400 or Num < 1:
#    Num = int(input("Number: "))
# else:
#    hours = Num // 3600
#    minutes = (Num % 3600) // 60
#    seconds = (Num % 3600) % 60
#    print(hours, "hours", minutes, "minutes", seconds, "seconds")

##T1.2
# import math
# a = float(input("length of side a: "))
# b = float(input("length of side b: "))
# c = float(input("length of side c: "))
# angle_c_rad = math.acos((a**2 + b**2 - c**2)/(2*a*b))
# angle_a_rad = math.acos((b**2 + c**2 - a**2)/(2*b*c))
# angle_b_rad = math.acos((a**2 + c**2 - b**2)/(2*a*c))
# angle_c = math.degrees(angle_c_rad)
# angle_a = math.degrees(angle_a_rad)
# angle_b = math.degrees(angle_b_rad)
# print(f"angle a = {angle_a:.2f} angle b = {angle_b:.2f} angle c = {angle_c:.2f}")

##Discussion 1
# hours = int(input("number of hours worked:"))
# if hours <= 160:
#     Gross_Pay = 10*hours
# else:
#     Gross_Pay = (160*10) + ((hours - 160)*15)
#
# if Gross_Pay <= 1000:
#     Tax = 0.1*Gross_Pay
# elif 1000 < Gross_Pay < 1500:
#     Tax = 100 + (Gross_Pay-1000)*0.2
# else:
#     Tax = 200 + (Gross_Pay - 1500)*0.3
#
# Net_Pay = Gross_Pay - Tax
# print("Gross Pay:", Gross_Pay, "Tax:", Tax, "Net Pay:", Net_Pay)

##Discussion 3
# count = 0
# str = input("Enter a string: ")
# while str != "####":
#     for letter in str:
#         if letter == "a":
#             count +=1
#             break
#     str = input("Enter a string: ")
# print(count, "strings with letter a")

##Discussion 4
# a = 1
# b = 1
# while a < 1000:
#     print(a, end=" ")
#     a, b = b, a+b

##Discussion 5
# N = int(input("PLease enter pattern width: "))
# for x in range(1, N+1):
#     print(x * "*")
# for x in range (N-1, 0, -1):
#     print(x * "*")

##Exercise-Divisible by 17?
# for x in range(100, 1000):
#     if x%17 == 0:
#         print(x)


