from werkzeug.security import generate_password_hash
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = generate_password_hash("admin_password")


stud_logins = ["student" + str(i) for i in range(50)]
stud_passwords = [generate_password_hash("password" + str(i)) for i in range(50)]

adviser_logins = [f"adviser_{i}" for i in range(50)]
adviser_passwords = [generate_password_hash("adviser_password" + str(i)) for i in range(50)]
