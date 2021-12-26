from itertools import combinations

arr = [1,2,3,4]

for i in combinations(arr, 3):
    print(list(i))