value = []
with open('sample.txt') as file:
    lines = file.readlines()
    for line in lines:
        genres = line.strip().split(',')
        for genre in genres:
            if genre not in value:
                value.append(genre)

value.sort()
print(value)
