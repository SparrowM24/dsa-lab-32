"""
Лабораторная работа №2, раздел II, задание 2.6
Удалить из строки все буквы "а" и вывести количество удаленных символов.
"""

print("Задание 2.6")

text = input("Введите строку: ")
result_string = ''
a_count = 0

for char in text:
    if char in 'aа':  # Обрабатываем и русскую, и латинскую 'a'
        a_count += 1
    else:
        result_string += char

print(result_string)
print(a_count)