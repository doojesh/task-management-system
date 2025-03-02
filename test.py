import bcrypt

# User's password
password = "mypassword"

# Generating a salt and hashing the password
salt = bcrypt.gensalt()  # Generates a random salt
hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

# Printing results
print(f"Salt: {salt}")
print(f"Hashed Password: {hashed_password}")

# Checking the password
input_password = "mypassword"
print(input_password.encode('utf-8'))
if bcrypt.checkpw(input_password.encode('utf-8'), hashed_password):
    print("✅ Password matches!")
else:
    print("❌ Incorrect password!")