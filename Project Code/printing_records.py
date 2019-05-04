import sqlite3 as sqlitedb


print("\nConnecting to database..")
con = sqlitedb.connect('PaymentCards_DB.sqlite')
print("\nConnected.")

print("\nCreating cursor..")
cur = con.cursor()
print("\nCreated.")

print("\nDetails printing..\n")
cur.execute("SELECT * FROM CARDOWNERDETAILS")
col_name_list = [tuple[0] for tuple in cur.description]
print(col_name_list)
result = cur.execute('SELECT * FROM CARDOWNERDETAILS')
for i in result:
    print(i)