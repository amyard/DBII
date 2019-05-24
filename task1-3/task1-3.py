''' TASK 1 '''

def handle_numbers(number1, number2, number3):
    num1, num2, num3= int(number1), int(number2), int(number3)
    list_range = list(range(num1, num2+1))
    res = sum(x % num3 == 0 for x in list_range)
    print(f'Task 1 \nResult: {res}\n')


number1 = 3
number2 = 14
number3 = 3

handle_numbers(number1, number2, number3)


# def handle_numbers(number1, number2, number3):
#     try:
#         num1, num2, num3= int(number1), int(number2), int(number3)
#         list_range = list(range(num1, num2 + 1))
#         try:
#             res = sum(x % num3 == 0 for x in list_range)
#             print(f'Result: {res}')
#         except ZeroDivisionError:
#             print('You can not divide by 0')
#     except ValueError:
#         print('You must use digits, not characters')
#
#
#
#
# number1 = 1
# number2 = 'dfs'
# number3 = 0
#
# handle_numbers(number1, number2, number3)


''' TASK 2 '''

def handle_string(value):
    digits = sum(c.isdigit() for c in value)
    chars = sum(c.isalpha() for c in value)
    print(f'Task 2 \nLetters - {chars} \nDigits - {digits}\n')

value = "Hello world!,, 123!"
handle_string(value)




''' Task 3 '''

my_list = [
    ("Tom", "19", "167", "54"),
    ("Jony", "24", "180", "69"),
    ("Json", "21", "185", "75"),
    ("John", "27", "190", "87"),
    ("Jony", "24", "191", "98"),
]

result= [
    ("John", "27", "190", "87"),
    ("Jony", "24", "191", "98"),
    ("Jony", "24", "180", "69"),
    ("Json", "21", "185", "75"),
    ("Tom", "19", "167", "54"),
]



def convert(my_list, new_type=int):
    for i in range(0, len(my_list)):
        my_list[i] = (my_list[i][0], new_type(my_list[i][1]), new_type(my_list[i][2]), new_type(my_list[i][3]) )
    return my_list

def handle_list_of_tuples(my_list):
    my_list = convert(my_list, int)
    res_int = sorted(my_list, key=lambda x : [ x[0], x[1], -x[2],  x[3] ])
    res_srt = convert(res_int, str)
    print(f'Task 3 \nResult: {res_srt}\n')

handle_list_of_tuples(my_list)

# print(f'Expected Result: {result}')