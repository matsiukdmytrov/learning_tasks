import re

file_path = input("Enter file name: ")

main_list = []
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        main_list.extend(re.findall("[0-9]+",line))
sum_loc = 0
for item in main_list:
    sum_loc += int(item)
print(sum_loc)