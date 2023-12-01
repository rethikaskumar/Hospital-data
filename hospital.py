# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:17:33 2022

@author: maana
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 10:02:43 2022

@author: DELL
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 10:43:51 2022

@author: maana
"""


import json
from tkinter import *
from tkinter import ttk
from tkinter.tix import * 
from PIL import ImageTk, Image
import requests
from bs4 import BeautifulSoup


with open("docdata.json", "r") as file:
    Hlist=json.load(file)



def getCommonSpl():
    allSpl=[]
    for i in range(2):
        hosSpl=Hlist[i].keys()
        for j in hosSpl:
            allSpl.append(j)
    allSpl=set(allSpl)
    return allSpl

def printDetails(varList, name):
    wind=Tk()
    wind.title(name)
    wind.geometry("1800x2000+10+20")
    sLb=Label(wind, text=name, fg="Black",font="Garamond")
    sLb.place(x=100,y=100)
    
    
    my_canvas = Canvas(wind)
    my_canvas.pack(side=LEFT,fill=BOTH,expand=1)
    y_scrollbar = ttk.Scrollbar(wind,orient=VERTICAL,command=my_canvas.yview)
    y_scrollbar.pack(side=RIGHT,fill=Y)
    my_canvas.configure(yscrollcommand=y_scrollbar.set)
    my_canvas.bind("<Configure>",lambda e: my_canvas.config(scrollregion= my_canvas.bbox(ALL)))
    second_frame = Frame(my_canvas)
    my_canvas.create_window((0,0),window= second_frame, anchor="w")
    a=Label(second_frame, text="List Of Doctors In "+ name, anchor='nw', font=('Garamond', 30) )
    a.grid(row=0, pady=100)
    for i in range(len(varList)):
        Label(second_frame ,text=varList[i]).grid(sticky="w", row=i+100,column=0, pady=10)
        #a.pack(anchor="w")
    wind.mainloop()

def getSpl(splCh):
    splprint=[]
    for i in range (2):
        hoslist=Hlist[i]
        docList=list(hoslist.values())
        splList=list(hoslist.keys())
        
        for j in splList:
            if j==splCh:
                ind=splList.index(j)
                for k in docList[ind]:
                    #print(k)
                    splprint.append(k)

    printDetails(splprint, splCh)

def getdoclist(ind):
    
    hoslist=Hlist[ind]
    doclist=hoslist.values()
    hosprint=[]
    for i in doclist:
        for j in i:
            hosprint.append(j)
    
    if ind==0:
        hName='KMCH'
    elif ind==1:
        hName='Sheela Hospitals'
    elif ind==2:
        hName='Sri Ramakrishna'
    printDetails(hosprint, hName)
    

window=Tk()
    
def hospital(hName):
    if hName=="KMCH":
        getdoclist(0)
    elif hName=="Sheela Hospital":
        getdoclist(1)
    elif hName=="Sri Ramakrishna":
        getdoclist(2)
    
def searchBySpl():
    def retrieve():
        splCh=cb.get()
        getSpl(splCh)
        #speciality(splCh, CSplList)
    searchBy=Label(window,text="Search By Speciality : ",fg="Black",font=("Garamond",30))
    searchBy.place(relx=0.35, rely=0.5)
    splList=tuple(getCommonSpl())
    #splList=('Anaesthesiology', 'Cardiac - Anaesthesiology', 'Cardiology', 'Cardio-Thoracic Surgery', 'Cosmetic Surgery', 'Critical Care Medicine', 'COMPREHENSIVE CANCER CENTER', 'DENTAL SURGERY', 'Dentistry  & Facio maxillary Surgery', 'Dermatology', 'Diabetology', 'Emergency Medicine', 'Endocrionology', 'ENT', 'GENERAL SURGERY', 'Gastroenterology', 'HEALTH CHECK UP CENTER / MHC', 'HEPATOLOGY', 'Infectious Diseases', 'Internal Medicine', 'LABORATORY MEDICINE', 'LIVER TRANSPLANT UNIT', 'Medical Genetics', 'Neonatology', 'Nephrology', 'Neurology', 'Neuro Surgery', 'OBSTETRICS & GYNAECOLOGY AND FERTILITY MEDICINE', 'Ophthalmology', 'Orthopaedic Surgery', 'Paediatrics', 'Paediatric Surgery', 'Physical & Rehabilitation Medicine', 'Plastic Surgery', 'Psychological Medicine', 'Pulmonology', 'RADIOLOGY', 'Rheumatology', 'Urology', 'Fetal Medicine', 'Pain Management')
    cb=ttk.Combobox(window,values=splList,width=100)
    
    cb.place(relx=0.5, rely=0.6,anchor="center")
    okBtn=Button(window,text="Ok", fg="Black",font="Garamond" , command=retrieve)
    okBtn.place(relx=0.5, rely=0.7)
    
def searchByHosp():
    def hide_widget():
        okBtn.pack_forget()
    def retrieve():
        hospCh=cb.get()
        hospital(hospCh)
    searchBy=Label(window,text="Search By Hospitals : ",fg="Black",font=("Garamond",30))
    searchBy.place(relx=0.35, rely=0.5)
    var=StringVar()
    var.set("PSG Hospital")
    hospList=("KMCH","Sheela Hospital", "Sri Ramakrishna")
    cb=ttk.Combobox(window,values=hospList, width=100)
    cb.place(relx=0.5, rely=0.6,anchor="center")
    okBtn=Button(window,text="Ok", fg="Black",font="Garamond",command=retrieve)
    okBtn.pack(pady=20)
    okBtn.place(relx=0.5, rely=0.7)
    
#make a window

#get wigth & height of screen
width= window.winfo_screenwidth()
height= window.winfo_screenheight()


window.title('Hospital Directory ')
window.geometry("%dx%d" % (width, height))

#set screensize as fullscreen and not resizable
#window.geometry("%dx%d" % (width, height))
window.resizable(False, False)

# put image in a label and place label as background
imgTemp = Image.open("1.jpg")
img2 = imgTemp.resize((width,height))
img = ImageTk.PhotoImage(img2)

label = Label(window,image=img)
label.pack(side='top',fill=Y,expand=True)
hospitalBtn=Button(window,text="Hospitals ",fg="Black",command=searchByHosp)
hospitalBtn.place(relx=0.35,rely=0.4, height=50, width=100)
splBtn=Button(window,text="Speciality ",fg="Black",command=searchBySpl)
splBtn.place(relx=0.55,rely=0.4, height=50, width=100)


lb0=Label(window, text="Hospital Directory ", fg="Black", font=("Garamond",50))
lb0.place(relx=0.5,rely=0.2, anchor="center")
lbl=Label(window, text="Search By : ", fg='Black', font=("Garamond", 30))
lbl.place(relx=0.3, rely=0.3)


window.mainloop()