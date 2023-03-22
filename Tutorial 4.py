##Sum of list of numbers
# def list_sum(num_list):
#     if len(num_list) == 1:
#         return num_list[0]
#     else:
#         print("num_list[0] is ", num_list[0])
#         print("num_list[1:] is ", num_list[1:])
#         a= num_list[0] + list_sum(num_list[1:])
#         return a
#         print("a is ", a)
# print(list_sum([2,4,5,6,7]))

##Sum of digits
# def sum_of_digits(n):
#     if n == 0:
#         return 0
#     else:
#         return n%10 + sum_of_digits(int(n/10))
# print(sum_of_digits(567))

##Mathematics
# def power(a,b):
#     if b == 1:
#         return a
#     elif b == 0:
#         return 1
#     elif a == 0:
#         return 0
#     else:
#         x = a * (power(a,b-1))
#         return x
# print(power(4,4))

# astring = "string to copy"
# newstr = astring[:]
# newstr = "o".join(astring)
# print(newstr)

# mylist = [1,2,3,4,5]
# mylist.pop()
# print(mylist)

# hi = [4,2,1,7]
# hi.sort()
# print(hi)

# my = [1,2,3,4,5]
# my.insert(0,"a")
# print(my)

# mylst = ['x', 'y','z','a','b','c']
# mylst.sort()
# sortstr = '2'.join(mylst)
# print(sortstr)

# tree = [[[7], 1, [9]], 3, [[8], 2, [4]]]
# def printTree(t,level):
#     if len(t) == 1:
#         print(" " * level, end=" ")
#         print(t[0])
#     else:
#         printTree(t[2], level +3)
#
#         print(" " * level, end=" ")
#         print(t[1])
#
#         printTree(t[0], level + 3)
# printTree(tree,0)






