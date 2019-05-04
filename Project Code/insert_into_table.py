import sqlite3 as sqlitedb


print("\nConnecting to database..")
con = sqlitedb.connect('PaymentCards_DB.sqlite')
print("\nConnected.")

print("\nCreating cursor..")
cur = con.cursor()
print("\nCreated.")

print("\nInserting columns..")
loop = int(input("Enter how many records you will enter : "))
for i in range(0,loop):
	cardnumber = input("Enter card number : ")
	fname = input("Enter fname : ")
	lname = input("Enter lname : ")
	email = input("Enter email : ")
	phone = input("Enter phone number : ")
	country = input("Enter country : ")
	state = input("Enter state : ")
	town = input("Enter town : ")    
	pincode = input("Enter pincode : ")
	doornum = input("Enter door number : ")
	nearbyloc = input("Enter near by location : ")
	try:
		if cur.execute('INSERT INTO CARDOWNERDETAILS (CARDNUMBER,FNAME,LNAME,EMAIL,PHONE,COUNTRY,STATE,TOWN,PINCODE,DOORNUM,NEARBYLOC) VALUES(?,?,?,?,?,?,?,?,?,?,?)',(cardnumber,fname,lname,email,phone,country,state,town,pincode,doornum,nearbyloc)):
			print("\nInsertion success..")
		else:
			print("\nInsertion failed!")
            
		con.commit()
	except:
		print("\nInvalid roll number!")