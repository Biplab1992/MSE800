keys = ['a', 'b', 'c']
values = [1, 2, 3]
dictionary = {k: v for k, v in zip(keys, values)}
print(dictionary)


numbers = [1, 2, 3, 4, 5]
even_squares = {n: n**2 for n in numbers if n % 2 == 0}
print(even_squares)

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4}
dict3 = {'d': 5, 'e': 6}
# merged_dict = {**dict1, **dict2, **dict3}
merged_dict = {**dict2, **dict1, **dict3}
print(merged_dict)

dict1 = {'a': 1, 'b': 2, 'c': 3}
dict2 = {'d': 4, 'e': 5, 'f': 6}
# print only the keys that are vowels
merged_dict = {**{k: v for k, v in dict1.items() if k in 'aeiou'}, **{k: v for k, v in dict2.items() if k in 'aeiou'}}
print(merged_dict)


x, _, y = (1, "ignored", 3)
print(x, y)


names = ["John", "Mike", "Sam", "Mark", "Ben"]
for i, name in enumerate(names):
    print (i, names[i])
#for i, name in enumerate(names, start=1):
 #   print (i, names[i])

names = ["Alice", "Bob", "Cathy"]
ages = [25, 30, 35]
paired = list(zip(names, ages))
print(paired)
print(type(paired))

paired_dict = dict(paired)
print(paired_dict)
print(type(paired_dict))

ids = [1, 2, 3]
names = ['Alice', 'Bob', 'Cathy', 'Mike']
grades = ['A', 'B', 'A+', 'A']
students = list(zip(ids, names, grades))
print(students)

students_dict = {id: {'name': name, 'grade': grade} for id, name, grade in students}
for id, info in students_dict.items():
    print(id, info['name'], info['grade'])