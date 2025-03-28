from werkzeug.security import generate_password_hash,check_password_hash
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH =generate_password_hash("mypassowrd123")


passwords =[generate_password_hash("Password" + str(i)) for i in range(50)]
logins = ["Student" +str(i) for i in range(50)]