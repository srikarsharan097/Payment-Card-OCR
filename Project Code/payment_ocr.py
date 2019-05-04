from imutils import contours
import numpy as np
import imutils
import cv2
import sqlite3 as sqlitedb
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image

top = Tk() 
top.geometry("715x505")
top.title('Address')
top.configure(background='#D6EAF8')

def order_placed():
	order_placed_label = Label(top, bg="#58D68D", text = "Order placed").place(x = 170, y = 470)

main_label = Label(top, text="Payment", font="times", width=65,bg="#3498DB", fg="#FDFEFE", justify="center").place(x=0, y=10)

cardnumber_label = Label(top, text = "Card number").place(x = 60,y = 60)
fname_label = Label(top, text = "First name").place(x = 60,y = 100)
lname_label = Label(top, text = "Last name").place(x = 60,y = 140)  
email_label = Label(top, text = "Email id").place(x = 60,y = 180)  
phone_label = Label(top, text = "Phone number").place(x = 60,y = 220)  
country_label = Label(top, text = "Country").place(x = 60,y = 260)
address_label = Label(top, text = "Address").place(x = 60,y = 300)


cardnumber_entry = Entry(top)
cardnumber_entry.place(x = 150, y = 60)  
fname_entry = Entry(top)
fname_entry.place(x = 150, y = 100)  
lname_entry = Entry(top)
lname_entry.place(x = 150, y = 140)
email_entry = Entry(top)
email_entry.place(x = 150, y = 180)
phone_entry = Entry(top)
phone_entry.place(x = 150, y = 220)
country_entry = Entry(top)
country_entry.place(x = 150, y = 260)
address_entry = Text(top, height=5, width=20)
address_entry.place(x = 150, y = 300)

sbmitbtn = Button(top,command = order_placed ,text = "Place order",padx=5,pady=0.5,font="times", activebackground = "#58D68D", activeforeground = "#FDFEFE", bg = "#3498DB", fg = "#FDFEFE", relief="groove").place(x = 150, y = 410)

img_path = filedialog.askopenfilename(filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All files", "*")])

FIRST_NUMBER = {
	"3": "American Express",
	"4": "Visa",
	"5": "MasterCard",
	"6": "Discover Card"
}

ref_img = "E:/Study/Project/Automatic details extraction from Payment cards with OCR and OpenCV/ocr_a_reference.png"
ref = cv2.imread(ref_img)
ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]

refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
refCnts = refCnts[0] if imutils.is_cv2() else refCnts[1]
refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
digits = {}

for (i, c) in enumerate(refCnts):
	(x, y, w, h) = cv2.boundingRect(c)
	roi = ref[y:y + h, x:x + w]
	roi = cv2.resize(roi, (57, 88))
	digits[i] = roi

rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

image = cv2.imread(img_path)
image = imutils.resize(image, width=300)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)
tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0,
	ksize=-1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal)))
gradX = gradX.astype("uint8")

gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(gradX, 0, 255,
	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]
locs = []

for (i, c) in enumerate(cnts):
	(x, y, w, h) = cv2.boundingRect(c)
	ar = w / float(h)

	if ar > 2.5 and ar < 4.0:
		if (w > 40 and w < 55) and (h > 10 and h < 20):
			locs.append((x, y, w, h))

locs = sorted(locs, key=lambda x:x[0])
output = []

for (i, (gX, gY, gW, gH)) in enumerate(locs):
	groupOutput = []
	group = gray[gY - 5:gY + gH + 5, gX - 5:gX + gW + 5]
	group = cv2.threshold(group, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	digitCnts = digitCnts[0] if imutils.is_cv2() else digitCnts[1]
	digitCnts = contours.sort_contours(digitCnts,
		method="left-to-right")[0]

	for c in digitCnts:
		(x, y, w, h) = cv2.boundingRect(c)
		roi = group[y:y + h, x:x + w]
		roi = cv2.resize(roi, (57, 88))

		scores = []
		for (digit, digitROI) in digits.items():
			result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF)
			(_, score, _, _) = cv2.minMaxLoc(result)
			scores.append(score)

		groupOutput.append(str(np.argmax(scores)))

	cv2.rectangle(image, (gX - 5, gY - 5),
		(gX + gW + 5, gY + gH + 5), (0, 0, 255), 2)
	cv2.putText(image, "".join(groupOutput), (gX, gY - 15),
		cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

	output.extend(groupOutput)

print("Credit Card Type: {}".format(FIRST_NUMBER[output[0]]))
final_image = image
#cv2.imshow("Image", final_image)
cv2.waitKey(1)

array_to_image = Image.fromarray(final_image)
array_to_image.save("array to image.png")


cardnumber = int("".join(output))

print(int("".join(output)))


main_label = Label(top, text="Payment", font="times", bg="#3498DB", fg="#FDFEFE", width=37, justify="center").place(x=0, y=10)

cardnumber_label = Label(top, text = "Card number").place(x = 60,y = 60)
fname_label = Label(top, text = "First name").place(x = 60,y = 100)
lname_label = Label(top, text = "Last name").place(x = 60,y = 140)  
email_label = Label(top, text = "Email id").place(x = 60,y = 180)  
phone_label = Label(top, text = "Phone number").place(x = 60,y = 220)  
country_label = Label(top, text = "Country").place(x = 60,y = 260)
address_label = Label(top, text = "Address").place(x = 60,y = 300)


cardnumber_entry = Entry(top)
cardnumber_entry.place(x = 150, y = 60)  
fname_entry = Entry(top)
fname_entry.place(x = 150, y = 100)  
lname_entry = Entry(top)
lname_entry.place(x = 150, y = 140)
email_entry = Entry(top)
email_entry.place(x = 150, y = 180)
phone_entry = Entry(top)
phone_entry.place(x = 150, y = 220)
country_entry = Entry(top)
country_entry.place(x = 150, y = 260)
address_entry = Text(top, height=5, width=20)
address_entry.place(x = 150, y = 300)


con = sqlitedb.connect('PaymentCards_DB.sqlite')
cur = con.cursor()
result_cursor = cur.execute('SELECT * FROM CARDOWNERDETAILS WHERE CARDNUMBER = ?',(cardnumber,))
for result_tuple in result_cursor:
	result_list = list(result_tuple)

cardnumber_entry.insert(0,result_list[0])
fname_entry.insert(0,result_list[1])
lname_entry.insert(0,result_list[2])
email_entry.insert(0,result_list[3])
phone_entry.insert(0,result_list[4])
country_entry.insert(0,result_list[5])
address_entry.insert(INSERT,result_list[6] +"\n"+ result_list[7] +"\n"+ result_list[8] +"\n"+ result_list[9]+"\n"+ result_list[10]+"\n")

final_image_getting= ImageTk.PhotoImage(Image.open("array to image.png"))
final_image_label = Label(top, image=final_image_getting).place(x = 400, y = 60)  

top.mainloop()