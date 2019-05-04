import sqlite3 as sqlitedb


print("\nConnecting to database..")
con = sqlitedb.connect('PaymentCards_DB.sqlite')
print("\nConnected.")

print("\nCreating cursor..")
cur = con.cursor()
print("\nCreated.")

print("\nCreating table..")
cur.execute('DROP TABLE IF EXISTS CARDOWNERDETAILS')
cur.execute('CREATE TABLE CARDOWNERDETAILS (CARDNUMBER TEXT, FNAME TEXT, LNAME TEXT, EMAIL TEXT, PHONE TEXT, COUNTRY TEXT, STATE TEXT, TOWN TEXT, PINCODE TEXT, DOORNUM TEXT, NEARBYLOC TEXT)')
print("\nCreated..")
