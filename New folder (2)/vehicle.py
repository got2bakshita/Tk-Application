from tkinter import *
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import json
import time
import pyttsx3
from datetime import date
from datetime import datetime
import re

global main
main = Tk()
main.title('Vehicle Parking Management System')
main.config(bg='#177DDC')
cur = time.localtime()
current_time = time.strftime("%H:%M:%S", cur)
today = date.today()
current_date = today.strftime('%Y-%m-%d')
text_speech = pyttsx3.init()

# Amount
bicycles = 78
bikes = 100
cars = 250

# def inputData


def newWindow():
    b11 = Button(main, text='Please select an action to contiue', state=DISABLED, bg='#49aa19',
                 command=lambda: print("Hello World"), fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=10)
    clicked.set("Select an option :)")

    def handleClick(event):
        with open("data.json", "r") as openfile:
            prevData = json.load(openfile)
        global vehNum, vehType, vehName, vehDet, bikes, cars, bicycles
        vehNum = vehicle_number_entry.get().strip()
        vehDet = owner_name_entry.get().strip()
        vehType = vehicle_type_combo.get()
        vehName = vehicle_name_entry.get().strip()
        dataArr = list(prevData["data"])

        data = {
            "number": vehNum,
            "name": vehName,
            "type": vehType,
            "owner": vehDet,
            "date": current_date,
            "time": current_time
        }

        if data not in dataArr:
            dataArr.append(data)
            with open("data.json", "w") as file:
                json.dump({"data": dataArr}, file)
            messagebox.showinfo("Success", "Data Saved Successfully")
        else:
            messagebox.showinfo("Failure", "Vehicle already registered")

    def onFocus(e):
        print("WORKING")

    details = Toplevel()
    details.title("Enter Details")
    details.config(bg="#177DDC")

    labelField = Label(details, text="Enter the vehicle number: ", font=(
        "Arial Rounded MT Bold", 14), bg="#177DDC", fg="#fff")
    labelField.grid(row=1, column=0)
    vehicle_number_entry = Entry(
        details, width=30, font=("Times New Roman", 15))
    vehicle_number_entry.grid(row=1, column=1)
    vehicle_number_entry.bind("<FocusIn>", onFocus)

    labelField4 = Label(details, text="Enter the owner name: ", font=(
        "Arial Rounded MT Bold", 14), bg="#177DDC", fg="#fff")
    labelField4.grid(row=2, column=0)
    owner_name_entry = Entry(details, width=30, font=("Times New Roman", 15))
    owner_name_entry.grid(row=2, column=1)

    labelField3 = Label(details, text="Enter the vehicle name: ", font=(
        "Arial Rounded MT Bold", 14), bg="#177DDC", fg="#fff")
    labelField3.grid(row=3, column=0)
    vehicle_name_entry = Entry(details, width=30, font=("Times New Roman", 15))
    vehicle_name_entry.grid(row=3, column=1)

    vehicle_type_label = Label(details, text="Select the vehicle type: ", font=(
        "Arial Rounded MT Bold", 14), bg="#177DDC", fg="#fff")
    vehicle_type_label.grid(row=4, column=0)
    vehicle_type_combo = ttk.Combobox(
        details, values=["Bike", "Car", "Bicycle"])
    vehicle_type_combo.current(0)
    vehicle_type_combo.grid(row=4, column=1)

    # but1 = Button(details, text="Submit", command=handleClick, )
    global but1
    but1 = Button(details, text='Submit', bg='#49aa19', fg='#fff')
    but1.grid(row=5, column=0,  columnspan=2, stick=W+E+N+S, padx=10, pady=20)
    but1.bind('<Button-1>', handleClick)
    details.mainloop()


global clicked
clicked = StringVar()
clicked.set('Select an action :)')


def showParkedVehicle():
    with open("data.json", "r") as openfile:
        data = json.load(openfile)
    parked_vehicle_details = ""
    for item in data["data"]:
        parked_vehicle_details += "Vehicle Number: " + item["number"] + "\nVehicle Type: " + item["type"] + \
            "\nVehicle Name: " + item["name"] + "\nOwner Name: " + \
            item["owner"] + "\nDate: " + item["date"] + \
            "\nTime: " + item["time"] + "\n\n"
    show_vehicle = Toplevel()
    show_vehicle.title("Parked Vehicle Details")
    show_vehicle.config(bg="#177DDC")
    label = Label(show_vehicle, text=parked_vehicle_details, font=(
        'Arial Rounded MT Bold', 14), width=30, padx=20, pady=10, bg='#177DDC', fg='#fff')
    label.pack()


def removeParkedVehicle():
    with open("data.json", "r") as openfile:
        data = json.load(openfile)
    remove_vehicle_num = tk.simpledialog.askstring(
        "Remove Vehicle", "Enter the vehicle number:", parent=main)
    dataArr = list(data["data"])

    flag = False
    index = -1
    for item in dataArr:
        if item["number"] == remove_vehicle_num:
            index = dataArr.index(item)
            flag = True

    if flag:
        newDataArr = dataArr.pop(index)
        with open("data.json", "w") as file:
            json.dump({"data": newDataArr}, file)
        messagebox.showinfo("Success", "Vehicle removed successfully")
    else:
        messagebox.showerror("Failure", "Vehicle Number not found")


def viewLeftSpace():
    messagebox.showinfo("Remaining Parking Space", "Bikes: " + str(bikes) +
                        "\nCars: " + str(cars) + "\nBicycles: " + str(bicycles))


def exitcode(exit):
    text_speech.say("Thank you")
    text_speech.runAndWait()
    exit(0)

def amount():
    with open("data.json", "r") as openfile:
        data = json.load(openfile)
    remove_vehicle_num = tk.simpledialog.askstring(
        "Check Amount", "Enter the vehicle number:", parent=main)
    dataArr = list(data["data"])

    flag = False
    days = 0
    amount = 0
    time = 0
    type = ""
    for item in dataArr:
        if item["number"] == remove_vehicle_num:
            flag = True
            userDate = datetime.strptime(item["date"], "%Y-%m-%d")
            current = datetime.strptime(current_date, "%Y-%m-%d")
            userTime = datetime.strptime(item["time"], "%H:%M:%S")
            currentTime = datetime.strptime(current_time, "%H:%M:%S")
            compareDays = current - userDate
            compareTime = currentTime - userTime
            days = compareDays.days
            time = compareTime.total_seconds()
            type = item["type"]

    hours = days*24 + time/3600
    if type == "Bike":
        amount = hours*bikes
    elif type == "Car":
        amount = hours*cars
    elif type == "Bicycle":
        amount = hours*bicycles
    if flag:
        messagebox.showinfo("Success", "Vehicle Amount: " + str(int(amount)))
    else:
        messagebox.showerror("Failure", "Vehicle Number not found")


def checkInput(e):
    global b11
    if e == 'Vehicle Entry':
        b11 = Button(main, text='Continue', command=newWindow, bg='#49aa19',
                     fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=10)
    elif e == 'Remove Entry':
        b11 = Button(main, text='Continue', command=removeParkedVehicle,
                     bg='#49aa19', fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=10)
    elif e == 'View parked vehicles':
        b11 = Button(main, text='Continue', command=showParkedVehicle,
                     bg='#49aa19', fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=10)
    elif e == 'View left parking space':
        b11 = Button(main, text='Continue', command=viewLeftSpace, bg='#49aa19',
                     fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=10)
    elif e == "Bill":
        b11 = Button(main, text='Continue', command=amount, bg='#49aa19', fg='#fff').grid(
            row=3, column=1, stick=W+E+N+S, pady=10)
    elif e == "Close Program":
        b11 = Button(main, text='Continue', command=lambda: exitcode(
            exit), bg='#49aa19', fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=10)
    else:
        b11 = Button(main, text='Please select an action to contiue', state=DISABLED,
                     bg='#49aa19', fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=10)

    text_speech.say(e)
    text_speech.runAndWait()


lab1 = Label(main, text='Vehicle Parking Management System', font=('Arial Rounded MT Bold', 22),
             width=30, padx=20, pady=10, bg='#177DDC', fg='#fff').grid(row=0, column=0, pady=5, columnspan=2)
lab2 = Label(main, text='--Desgined by:- Akshita, Ananya, Akshat', font=('Times New Roman', 10), relief='sunken',
             justify='right', width=35, borderwidth=0, bg='#177DDC', fg='#fff').grid(row=1, column=0, stick=W, columnspan=2)
text_speech.say("Welcome to our service")
text_speech.runAndWait()
drop = OptionMenu(main, clicked, "Vehicle Entry", "Remove Entry", "View parked vehicles",
                  "View left parking space", "Bill", "Close Program", command=checkInput)
drop.config(bg='#49aa19', fg='#fff', borderwidth=0, border=0)
drop.grid(row=2, column=0, columnspan=2, pady=15)
b11 = Button(main, text='Continue', state=DISABLED, bg='#49aa19', command=lambda: print(
    "Hello World"), fg='#fff').grid(row=3, column=1, stick=W+E+N+S, pady=14)
main.mainloop()