import bcrypt

password = b'Muslima'

# b = password.encode('utf-8')
# a = bcrypt.gensalt()
_hash = bcrypt.hashpw(password, bcrypt.gensalt())
print(_hash)
