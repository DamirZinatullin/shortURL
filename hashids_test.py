import hashids

hashids = hashids.Hashids(min_length=7)
# print(dir(hashids))
print(hashids.encode(12343423))

