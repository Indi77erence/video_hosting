a = [1, 2, 4, 3]


rez = [bin(i) for i in a]
print(rez)
answer = {int(z, 2): z.count("1") + z.count('0') for i, z in enumerate(rez)}
print(answer)
rezult = [i[0] for i in sorted(answer.items(), key=lambda x: x[1])]
print(rezult)

print(rezult[::-1])


