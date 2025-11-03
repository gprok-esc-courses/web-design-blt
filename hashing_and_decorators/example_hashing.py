from hashlib import md5

user1 = "jdoe"
user2 = "admin"

pass1 = "1111"
pass2 = "1111"

hashed1 = md5((user1 + pass1).encode('utf-8'))
hashed2 = md5((user2 + pass2).encode('utf-8'))
hashed3 = md5(('mdoe' + '1111').encode('utf-8'))

print(hashed1.hexdigest())
print(hashed2.hexdigest())
print(hashed3.hexdigest())

u = input("Username: ")
p = input("Password: ")
hashed = md5((u + p).encode('utf-8'))
print(hashed.hexdigest())