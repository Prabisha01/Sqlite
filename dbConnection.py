import sqlite3

conn = sqlite3.connect("student.db")

cursor = conn.cursor()

cursor.execute(
    """
    Create table if not exists users 
    (id Integer Primary key autoincrement, 
    name text,
    age Integer
    )
    """
)
print("Created Successfully")
cursor.execute(
    """Insert into users (name, age) values ("Prabisha", 5)"""
)

cursor.execute(
    """
    Create table if not exists passwordTable  
    (id Integer Primary key autoincrement, 
    username text,
    password text
    )
    """
)
cursor.execute("""
               Insert into passwordTable (username, password) values ("Prabisha", "12345")
               """)
username = input("Enter the username")
password = input("Enter the password")


query = cursor.execute(
    "Select * from passwordTable where username = ? and password =? ",(username, password)
)
print(query)

result = cursor.fetchone()
if result :
    print("login successful")
else:
    print("invalid")

# print("Inserted successfully")

cursor.execute("""
               update users set name = "prabisha Khaddka" where id =1
               """)

cursor.execute("""
               select * from users
               """)

row = cursor.fetchall()
for rows in row:
    print(rows) 
    
cursor.execute("""Delete from users where id = 1""")
print("deleted")
conn.commit()
conn.close()
