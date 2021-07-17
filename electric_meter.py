#electricity meter
import tkinter as tk 
from tkcalendar import Calendar
import datetime

window = tk.Tk()
window.title('Electricity Calculator')
window.geometry('350x370')
window.resizable(0,0)
units = []

frame = tk.Frame(window)
frame.pack(side = "right", fill='y')
scroll_bar = tk.Scrollbar(frame, orient='vertical')
scroll_bar.pack(side = 'right', fill='y')
listbox = tk.Listbox(frame, yscrollcommand=scroll_bar.set)
listbox.pack(side='left', fill='y')

EC = tk.StringVar()
DG = tk.StringVar()
current_time = datetime.datetime.now() 

#functions 
def fetch():
    units.clear()
    initialise()
    f = open('data.txt', 'r')
    for line in f: 
      if line: 
        date, ec, dg = line.split(',')
        date = str(date)
        ec = str(ec)
        dg = str(dg)
        units.append([date,ec,dg])
    initialise()
    avg_calculate()
    
def initialise():
    count = 0 
    listbox.delete(0, tk.END)
    for date, ec, dg in units: 
        listbox.insert(count, [str(date), str(ec), str(dg)])
        count = count+1
    EC.set('EC Units') 
    DG.set('DG Units') 
    
def add(event=None):
    units.append([calendar.get_date(), ecinput.get(), dginput.get()])
    initialise()
    avg_calculate()
    save()
    
def selection(): 
    if listbox.curselection(): 
      return listbox.curselection()[0]
      
def edit(): 
    if listbox.curselection():
      units[selection()] = [ecinput.get(), dginput.get()]
      initialise()

def delete(): 
    if listbox.curselection(): 
        del units[selection()]
        initialise()
        avg_calculate()
    save()
    
def avg_calculate(): 
    total_ec = 0
    total_dg = 0 
    count = 0 
    for date, ec, dg in units: 
        count = count+1 
        total_ec = total_ec + float(ec)
        total_dg = total_dg + float(dg)
    avg_ec = total_ec/count 
    avg_dg = total_dg/count
    label1['text'] = "Total Spent: "+str(round((total_ec*6.25 + total_dg*21.5), 2))
    label2['text'] = "Predicted Bill: "+str(round(((avg_ec*6.25 + avg_dg*21.5)*30),2))

def save(): 
    f = open('data.txt', 'w')
    for date, ec, dg in units:
        f.write(date+','+ec+','+dg+'\n')
    f.close()

def reset(): 
    units.clear()
    f = open('data.txt', 'w')
    f.close()
    initialise()
    label1['text'] = ""
    label2['text'] = ""   

initialise()    
#widgets 
calendar = Calendar(window, selectmode = 'day',
               year = current_time.year, month = current_time.month,
               day = current_time.day)
ecinput = tk.Entry(window, textvariable = EC)
dginput = tk.Entry(window, textvariable = DG)
frame1 = tk.Frame(window)
window.bind('<Return>', add)
btn1 = tk.Button(frame1, text='Add', command=add)
btn1.grid(row=0, column=1) 
btn2 = tk.Button(frame1, text='Update', command=edit)
btn2.grid(row=0, column=0) 
btn3 = tk.Button(frame1, text='Delete', command=delete)
btn3.grid(row=0, column=2)
btn4 = tk.Button(frame1, text='Load', command=fetch)
btn4.grid(row=0, column=3)
btn5 = tk.Button(frame1, text='Reset', command=reset)
btn5.grid(row=0, column=4)
label1 = tk.Label(window, text="")
label2 = tk.Label(window, text="")
#pack
calendar.pack(pady=10)
ecinput.pack(pady=10)
dginput.pack(pady=10)
frame1.pack(side = 'bottom')
label1.pack()
label2.pack()
#mainloop
window.mainloop()