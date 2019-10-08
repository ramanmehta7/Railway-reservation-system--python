from tkinter import *
import pymysql
import tkinter.messagebox as box

conn = pymysql.connect(host='localhost',user='root',db='train')
cur = conn.cursor()

def quitwindow():
    global window
    window.quit()
    window.destroy()

def pay_ticket(cr_var,new_window,passengers,cls,sour,dest,date,train_name):
    print(len(cr_var))

    if len(cr_var)==19:
        box.showinfo("Greetings","Tickets Booked")
    
        cur.execute("select "+cls+" from available where source='"+sour+"' and destination='"+dest+"' and date='"+date+"' and name='"+train_name+"'")
        seats=cur.fetchall()
        value=seats[0][0]-int(passengers)
    
        cur.execute("update available set "+cls+"="+str(value)+" where source='"+sour+"' and destination='"+dest+"' and date='"+date+"' and name='"+train_name+"'")
        conn.commit()
        new_window.quit()
        new_window.destroy()

    else:
        box.showinfo("Access Denied","Invalid Credentials")
        new_window.quit()
        new_window.destroy()

    
def book(new_window,train_name,result,passengers,cls,sour,dest,date):
    for row in result:
        if row[0]==train_name:
            price=int(passengers)*int(row[1])
            print(price)

    credit_lab=Label(new_window,text="Enter card details").grid(row=4,column=2)
    cr_var=StringVar()
    credit=Entry(new_window,textvariable=cr_var).grid(row=4,column=3)
    
    pay_btn=Button(new_window,text="PAY",command=lambda : pay_ticket(cr_var.get(),new_window,passengers,cls,sour,dest,date,train_name))
    pay_btn.grid(row=5,column=2)
    

def search(new_window,sour,dest,date,passengers,cls):
    cur.execute("select name,price from available where source='"+sour+"' and destination='"+dest+"' and date='"+date+"' and "+cls+">="+passengers)
    result=cur.fetchall()
    if len(result)==0:
        box.showinfo("Access denied","No Trains Available")
    else:
        l=list()
        for row in result:
            print(row[0],row[1])
            l.append(row[0])
        
        t=tuple(l)
        
        avail=StringVar()
        avail.set(l[0])
        avail_lab=Label(new_window,text="Available Trains").grid(row=0,column=2)
        avail_train=OptionMenu(new_window,avail,*t).grid(row=1,column=2)

        ticket_btn=Button(new_window,text="BOOK TICKET",command=lambda : book(new_window,avail.get(),result,passengers,cls,sour,dest,date))
        ticket_btn.grid(row=2,column=2)
    
def afterlogin():
    new_window=Tk()
    new_window.title("Train Tickets")
    frame=Frame(new_window)
    
    
    #img=PhotoImage(file="train3.png")
    #image=Label(frame,image=img)
    #image.place(x=10,y=10)
    
    source_lab=Label(new_window,text="Source").grid(row=0,column=0)
    sour=StringVar(new_window)
    sour.set("kurukshetra")
    source=OptionMenu(new_window,sour,"kurukshetra","yamunanagar","delhi","sirsa").grid(row=0,column=1)
    
    destination_lab=Label(new_window,text="Destination").grid(row=1,column=0)
    dest=StringVar(new_window)
    dest.set("kurukshetra")
    l=("kurukshetra","yamunanagar","delhi","sirsa")
    destination=OptionMenu(new_window,dest,*l).grid(row=1,column=1)
    
    
    passengers_lab=Label(new_window,text="Passengers Number").grid(row=2,column=0)
    passengers_var=StringVar()
    passengers=Entry(new_window,textvariable=passengers_var).grid(row=2,column=1)

    date_lab=Label(new_window,text="Date").grid(row=3,column=0)
    date_var=StringVar()
    date=Entry(new_window,textvariable=date_var).grid(row=3,column=1)
    

    class_lab=Label(new_window,text="Class").grid(row=4,column=0)
    cls=StringVar(new_window)
    cls.set("sleeper")
    destination=OptionMenu(new_window,cls,"sleeper","ac").grid(row=4,column=1)

    user="hry"
    search_btn=Button(new_window,text="SEARCH",command=lambda : search(new_window,sour.get(),dest.get(),date_var.get(),passengers_var.get(),cls.get()))
    search_btn.grid(row=6,column=0)
    
    new_window.mainloop()
    
def dialog(status,user):
    if status==1:
        box.showinfo("Greetings","Welcome "+user)
    else:
        box.showinfo("Access Denied","Invalid Username or Password")

def dialog_register(status,user):
    if status==0:
        box.showinfo("Access Denied","Username Already Exists")
    else:
        box.showinfo("Greetings","Successfully Registered")

        
def login():
    user=username.get()
    pswd=password.get()
    cur1=conn.cursor()
    cur.execute("Select username from login")
    result=cur.fetchall()
    status=0
    for row in result:
        if row[0]==user:
            status=1
            print("user "+user)
            cur1.execute("Select password from login where username = '"+user+"'")
            print(user)
            getpswd=cur1.fetchall()
            for j in getpswd:
                if(j[0]==pswd):
                    dialog(status,user)
                    quitwindow()
                    afterlogin()
                else:
                    dialog(0,user)
        if status==1:
            break;
    if status==0:
        dialog(status,user)


def register():
    user=username.get()
    pswd=password.get()
    cur.execute("Select username from login")
    result=cur.fetchall()
    status=1
    for row in result:
        if user==row[0]:
            status=0;
            break;
    if status==0:
        dialog_register(status,user)
    else:
        cur.execute("insert into login values('"+user+"','"+pswd+"')" )
        conn.commit()
        dialog(status,user)
        quitwindow()
        afterlogin()

        
window=Tk()
window.title("Login or Register")
frame=Frame(window)

"""username=Entry(frame)
password=Entry(frame)
login_btn=Button(frame,text="LOGIN",command=login)
register_btn=Button(frame,text="REGISTER",command=register)
username.pack(pady=10,side=TOP)
password.pack(pady=10,side=TOP)
login_btn.pack(pady=10,side=TOP)
register_btn.pack(pady=10,side=TOP)"""

user_lab=Label(window,text="UserName").grid(row=0,column=0)
username=StringVar()
user_entry=Entry(window,textvariable=username).grid(row=0,column=1)

pass_lab=Label(window,text="Password").grid(row=1,column=0)
password=StringVar()
pass_entry=Entry(window,textvariable=password,show='*').grid(row=1,column=1)

login_btn=Button(window,text="LOGIN",command=login).grid(row=2,column=0)
register_btn=Button(window,text="REGISTER",command=register).grid(row=3,column=0)


#frame.pack(padx=20,pady=20)
window.mainloop()






