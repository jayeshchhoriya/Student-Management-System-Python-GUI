from tkinter import *
from tkinter import messagebox
import cx_Oracle
from tkinter import scrolledtext
from matplotlib import pyplot as plt
import numpy as py
import threading
import time
import socket
import requests
import bs4
from PIL import ImageTk,Image
#SPLASH WINDOW

socket.create_connection(("www.google.com",80))
res=requests.get("https://www.brainyquote.com/quotes_of_the_day.html")
soup=bs4.BeautifulSoup(res.text,'lxml')
quote=soup.find('img',{"class":"p-qotd"})
msg_of_day="https://www.brainyquote.com" + quote['data-img-url']
img="https://www.brainyquote.com" + quote['data-img-url']
r=requests.get(img)
with open("image1.jpg",'wb') as f:
	f.write(r.content)

def screen():
	root=Tk()
	root.title("splash screen")
	root.geometry("1200x700+50+0")
	city="Mumbai"
	a1="http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2="&q="+city
	a3="&appid=c6e315d09197cec231495138183954bd"
	api_address=a1+a2+a3
	res1=requests.get(api_address)
	wdata=requests.get(api_address).json()
	main=wdata['main']
	temp=main['temp']
	temp=str(temp)
	img=ImageTk.PhotoImage(Image.open("image1.jpg"))
	lblImg=Label(root,image=img)
	lblImg.pack(side="top",expand="no",fill="both")
	label=Label(root,text="Temperature : "+temp+"\u00B0"+"C"+"\n"+"City : "+city,font=("arial",16,"bold"))
	label.place(x=500,y=700)
	label.pack()
	root.after(5000,root.destroy)
	root.mainloop()

thread_splash=threading.Thread(target=screen)
thread_splash.start()
thread_splash.join()

#main window

root = Tk()
root.title("S.M.S.")
root.geometry("400x450+250+150")
root.configure(background='gray93')

def f1():
	adst.deiconify()
	root.withdraw()
def f3():
	vist.deiconify()
	root.withdraw()
	con=None	
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		msg1=''
		cursor=con.cursor()
		sql="select * from student"
		cursor.execute(sql )
		data=cursor.fetchall()
		for d in data:
			msg1=msg1+"Roll no :"+str(d[0])+" Name :"+str(d[1])+" Marks :"+str(d[2])+"\n"			
		
		stData.configure(state=NORMAL)
		stData.delete(1.0, END) 
		stData.insert(INSERT,msg1)
		
		stData.configure(state=DISABLED)



	except cx_Oracle.DatabaseError as e:
		print("Issue",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()
def f6():
	upst.deiconify()
	root.withdraw()
def f11():
	dest.deiconify()
	root.withdraw()
def f17():
	con=None	
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		cursor=con.cursor()
		sql="select NAME from student"
		cursor.execute(sql)
		gp = list(cursor.fetchall())
		for i,row in enumerate(cursor.fetchall()):
			gp.append(row[i])
			list(gp[i])

		#for getting name in list
		names = [item for t in gp for item in t] 
		sql1 ="select MARKS from student"
		cursor.execute(sql1)
		gp1 = list(cursor.fetchall())
		for i,row in enumerate(cursor.fetchall()):

			gp1.append(row[i])
			list(gp1[i])

		marks = [item for t in gp1 for item in t] 
		a=py.arange(len(names))
		plt.bar(a,marks,width=0.25,label="Marks")
		plt.title("PERFORMANCE")
		plt.ylabel("Marks")
		plt.xlabel("Name")
		plt.xticks(a,names)
		plt.legend()
		plt.grid()
		plt.show()
			
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()			



lblroot = Label(root,text ="Student Management System",font=("castellar",14,"bold"))
btnAdd = Button(root,text="Add",width=12,font=("ink free",15,"bold"),command=f1,bg='turquoise4' ,fg='White')
btnView = Button(root,text="View",width=12,font=("ink free",15,"bold"),command=f3,bg='turquoise4' ,fg='White')
btnUpdate = Button(root,text="Update",width=12,font=("ink free",15,"bold"),command=f6,bg='turquoise4' ,fg='White')
btnDelete = Button(root,text="Delete",width=12,font=("ink free",15,"bold"),command=f11,bg='turquoise4' ,fg='White')
btnGraph = Button(root,text="Graph",width=12,font=("ink free",15,"bold"),bg='turquoise4' ,fg='White',command=f17)

lblroot.pack(pady=10)
btnAdd.pack(pady=15)

btnView.pack(pady=15)
btnUpdate.pack(pady=15)
btnDelete.pack(pady=15)
btnGraph.pack(pady=15)

#ADDING WINDOW

adst= Toplevel(root)
adst.title("Add Student")
adst.geometry("400x450+250+150")
adst.configure(background='gray93')
adst.withdraw()

def f2():
	root.deiconify()
	adst.withdraw()
def f13():
	con = None
	cursor = None
	try:
		con = cx_Oracle.connect("system/abc123")
		rno = entAddrno.get()
		name = entAddname.get()
		marks = entAddmarks.get()
		if rno.isdigit() and name.isalpha() and int(rno) > 0 and marks.isdigit() and int(marks) > 0 and int(marks) < 100 :
			rno=int(rno)
			marks=int(marks)
			cursor = con.cursor()
			sql = "insert into student values('%d', '%s', '%d')"
			args = (rno , name , marks)
			cursor.execute(sql%args)
			con.commit()
			msg= str(cursor.rowcount)+" Row Inserted"
			messagebox.showinfo("Success",msg)
			entAddname.delete(0,END)
			entAddrno.delete(0,END)
			entAddmarks.delete(0,END)
			entAddrno.focus()
		else:
			messagebox.showerror('Error','Invalid input')
			entAddname.delete(0,END)
			entAddrno.delete(0,END)
			entAddmarks.delete(0,END)
			entAddrno.focus()

				
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Error",e)
		entAddname.delete(0,END)
		entAddrno.delete(0,END)
		entAddmarks.delete(0,END)
		entAddrno.focus()
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()

lblAddrno = Label(adst,text="Enter Roll Number",font=("arial", 12,"bold" ))
entAddrno = Entry(adst,bd=5)
lblAddname = Label(adst,text="Enter Name",font=("arial",12,"bold"))
entAddname = Entry(adst,bd=5)
lblAddmarks = Label(adst,text="Enter Marks",font=("arial",12,"bold"))
entAddmarks = Entry(adst,bd=5)
btnAddsave = Button(adst,text="Save",font=("ink free",12,"bold"),width=12,bg='turquoise4' ,fg='White',command=f13)
btnAddback = Button(adst,text="Back",command=f2,font=("ink free",12,"bold"),width=12,bg='turquoise4' ,fg='White')

lblAddrno.pack(pady=10)
entAddrno.pack(pady=10)
lblAddname.pack(pady=10)
entAddname.pack(pady=10)
lblAddmarks.pack(pady=10)
entAddmarks.pack(pady=10)
btnAddsave.pack(pady=10)
btnAddback.pack(pady=10)

#VIEW WINDOW

vist = Toplevel(root)
vist.title("View Student")
vist.geometry("400x400+200+200")
vist.configure(background='gray93')
vist.withdraw()

def f4():
	root.deiconify()
	vist.withdraw()

stData = scrolledtext.ScrolledText(vist,width=40,height=10)
btnViewback = Button(vist,text="Back",font=("ink free",15,"bold"),width=12,command=f4,bg='turquoise4' ,fg='White')

stData.pack(pady=20)
btnViewback.pack(pady=10)


#UPDATE WINDOW

upst = Toplevel(root)
upst.title("Update Student Information")
upst.geometry("400x400+200+200")
upst.configure(background='gray93')
upst.withdraw()
def f5():
	root.deiconify()
	upst.withdraw()
def f7():
	upnm.deiconify()
	upst.withdraw()
def f9():
	upmrk.deiconify()
	upst.withdraw()
btnUpdatename = Button(upst,text="Update Name",font=("ink free",15,"bold"),width=12,command=f7,bg='turquoise4' ,fg='White')
btnUpdatemarks = Button(upst,text="Update Marks",font=("ink free",15,"bold"),width=12,command=f9,bg='turquoise4' ,fg='White')
btnUpdateback = Button(upst,text="Back",font=("ink free",15,"bold"),width=12,command=f5,bg='turquoise4' ,fg='White')

btnUpdatename.pack(pady=20)
btnUpdatemarks.pack(pady=20)
btnUpdateback.pack(pady=20)


#UPDATE NAME WINDOW

upnm = Toplevel(root)
upnm.title("Update Student's Name")
upnm.geometry("400x400+200+200")
upnm.configure(background='gray93')
upnm.withdraw()

def f8():
	upst.deiconify()
	upnm.withdraw()
def f14():
	con=None
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		rno = (entupnmrno.get())
		name = (entupnmname.get())
		if rno.isdigit() and int(rno) > 0 and name.isalpha():
			rno=int(rno)
			cursor = con.cursor()
			sql = "update student set name='%s' where rno='%d'"			
			args = (name,rno)
			cursor.execute(sql%args)
			con.commit()
			msg= str(cursor.rowcount)+" Row Updated"
			messagebox.showinfo("Success",msg)
			entupnmrno.delete(0,END)
			entupnmname.delete(0,END)
			entupnmrno.focus()	
		else:
			messagebox.showerror('Error','Invalid input')
			entupnmrno.delete(0,END)
			entupnmname.delete(0,END)
			entupnmrno.focus()	


	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Error",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()	

			
			
lblupnmrno = Label(upnm,text="Enter Roll Number",font=("arial",12,"bold"))
entupnmrno = Entry(upnm,bd=5)
lblupnmname = Label(upnm,text="Enter New Name",font=("arial",12,"bold"))
entupnmname = Entry(upnm,bd=5)
btnupnmsave = Button(upnm,text="Save",font=("ink free",12,"bold"),width=12,bg='turquoise4' ,fg='White',command=f14)
btnupnmback = Button(upnm,text="Back",font=("ink free",12,"bold"),width=12,command=f8,bg='turquoise4' ,fg='White')


lblupnmrno.pack(pady=10)
entupnmrno.pack(pady=10)
lblupnmname.pack(pady=10)
entupnmname.pack(pady=10)
btnupnmsave.pack(pady=10)
btnupnmback.pack(pady=10)

#UPDATE MARKS WINDOW
upmrk = Toplevel(root)
upmrk.title("Update Student's Marks")
upmrk.geometry("400x400+200+200")
upmrk.configure(background='gray93')
upmrk.withdraw()


def f10():
	upst.deiconify()
	upmrk.withdraw()
def f15():
	con=None
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		rno = (entupmrkrno.get())
		mark = (entupmrkmark.get())
		if rno.isdigit() and int(rno) > 0 and mark.isdigit() and int(mark)>0 and int(mark)<100:
			rno=int(rno)
			mark=int(mark)
			cursor = con.cursor()
			sql = "update student set marks=('%d') where rno='%d'"			
			args = (mark,rno)
			cursor.execute(sql%args)
			con.commit()
			msg= str(cursor.rowcount)+" Row Updated"
			messagebox.showinfo("Success",msg)
			entupmrkrno.delete(0,END)
			entupmrkmark.delete(0,END)
			entupmrkrno.focus()	
		else:
			messagebox.showerror('Error','Invalid input')
			entupmrkrno.delete(0,END)
			entupmrkmark.delete(0,END)
			entupmrkrno.focus()	


	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Error",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()	

lblupmrkrno = Label(upmrk,text="Enter Roll Number",font=("arial",12,"bold"))
entupmrkrno = Entry(upmrk,bd=5)
lblupmrkmark = Label(upmrk,text="Enter New Marks",font=("arial",12,"bold"))
entupmrkmark = Entry(upmrk,bd=5)
btnupmrksave = Button(upmrk,text="Save",font=("ink free",12,"bold"),width=12,bg='turquoise4' ,fg='White',command=f15)
btnupmrkback = Button(upmrk,text="Back",font=("ink free",12,"bold"),width=12,command=f10,bg='turquoise4' ,fg='White')


lblupmrkrno.pack(pady=10)
entupmrkrno.pack(pady=10)
lblupmrkmark.pack(pady=10)
entupmrkmark.pack(pady=10)
btnupmrksave.pack(pady=10)
btnupmrkback.pack(pady=10)

#DELETE WINDOW
dest = Toplevel(root)
dest.title("Delete Student")
dest.geometry("400x400+200+200")
dest.configure(background='gray93')
dest.withdraw()
def f12():
	root.deiconify()
	dest.withdraw()

def f16():			
	con=None
	cursor=None
	try:
		con = cx_Oracle.connect("system/abc123")
		rno = (entdestrno.get())
		cursor=con.cursor()
		if rno.isdigit() and int(rno) > 0:
			rno=int(rno)
			cursor = con.cursor()
			sql = "delete from student where rno='%d'"
			args = (rno)
			cursor.execute(sql%args)
			con.commit()
			msg= str(cursor.rowcount)+" Row Deleted"
			messagebox.showinfo("Success",msg)
			entdestrno.delete(0,END)
			entdestrno.focus()
				
		else:
			messagebox.showerror('Error','Invalid input')
			entdestrno.delete(0,END)
			entdestrno.focus()
			return
	except cx_Oracle.DatabaseError as e:
		con.rollback()
		messagebox.showerror("Error",e)
	finally:
		if cursor is not None:
			cursor.close()
		if con is not None:
			con.close()	


lbldestrno= Label(dest,text="Enter Roll number to be deleted",font=("arial",12,"bold"))
entdestrno = Entry(dest,bd=5)
btndestsave = Button(dest,text="Save",width=12,font=("ink free",12,"bold"),bg='turquoise4' ,fg='White',command=f16)
btndestback = Button(dest,text="Back",width=12,font=("ink free",12,"bold"),command=f12,bg='turquoise4' ,fg='White')

lbldestrno.pack(pady=15)
entdestrno.pack(pady=15)
btndestsave.pack(pady=15)
btndestback.pack(pady=15)

#GRAPH WINDOW

gpst = Toplevel(root)
gpst.title("Graph")
gpst.geometry("400x400+200+200")
gpst.configure(background='gray93')
gpst.withdraw()

def f18():
	root.deiconify()
	gpst.withdraw()

btngpback = Button(gpst,text="Back",font=("ink free",15,"bold"),width=12,command=f18,bg='turquoise4' ,fg='White')



root.mainloop()