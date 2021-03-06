# DBII
> login - admin@gmail.com    
> pass - zaza1234    


> **Instruction:**
1. ```git clone https://github.com/amyard/DBII.git```
2. ```cd DBII```
3. ```python manage.py makemigrations```
4. ```python manage.py migrate```
5. ```python populate_data.py``` - populate models with data 
5. ```python manage.py runserver```

> **Need to do:**    

To find the right person to a DB2 team we are giving you a simple test job. Please note that this task has 3 simple tasks and 1 project task what should be deployed to Heroku.

Deadline: ASAP! Like on the real project :)

Technologies:
- Django
- PostgreSQL

Deploy to Heroku

#### Test job:

> **1.**    

Write a function that takes as a parameters number1(int), number2(int) and number3. (e.g. handle_numbers(number1, number2, number3))
Function need to return the count of integers that are divisible by number3 in range [number1, number2]

Example:    
number1 = 1    
number2 = 10    
number3 = 2    

Result: 
5, because 2, 4, 6, 8, 10 are divisible by 2    

> **2.**    

Write a function that takes sentense as a parameter (e.g. handle_string(value)) and count number of letters and digits.
Example:
value = "Hello world! 123!"    

Result:    
Letters -  10    
Digits -  3    

> **3.**    

Write a function that takes list of tuples (e.g. handle_list_of_tuples(list)) and sort it based on the next rules:
name / age / height / weight    
Example:    
list = [    
        ("Tom", "19", "167", "54"),   
        ("Jony", "24", "180", "69"),    
        ("Json", "21", "185", "75"),     
        ("John", "27", "190", "87"),     
        ("Jony", "24", "191", "98"),     
    ]    

Result:    
[    
    ("John", "27", "190", "87"),    
    ("Jony", "24", "191", "98"),    
    ("Jony", "24", "180", "69"),    
    ("Json", "21", "185", "75"),    
    ("Tom", "19", "167", "54"),    
]    

> **4.**    

Web-based django application with custom user model(custom fields: birthday, country, city).
Each user need to be able to sign-up/sign-in via email/password. (also sign-out)
After sign-up user will get an confirmation email with verification code(or link, or both).
Only after verify email he can sign in to the website.    
Website must be protected from anonymous users and be available only for logged users.
On the main page:    
    - show all list Posts(e.g. title/body/image etc) with pagination. That list also need to have sorting form. (Country, city, search by keyword)    
    - below each post user see number of the likes and the "like" button which add +1 like. User can like post only once, then it marked as liked, but he can to delete his like, and like again and so on. (Reference to social network likes.)    
    - User can go to a single post page and see the post details and comments to the post also with pagination.


**Good luck!**
