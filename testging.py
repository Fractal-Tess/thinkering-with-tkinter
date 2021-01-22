import sqlite3
conn = sqlite3.connect('accounts.db')
c = conn.cursor()


c.execute("SELECT * FROM Accounts")
print(c.fetchall()[2][2])

for _ in range(4):
    for i in range(4):
        pass