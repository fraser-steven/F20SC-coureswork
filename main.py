# F20SC: Industrial Programming 
# Coursework 2
# Data Analysis of a Document Tracker

# Fraser Steven (fs65)
# Tegan Friedenthal (tf50)

# part 7: GUI using tkinter
filename = ""
def openfile():
    print("open file button pressed")
    filename = E1.get()
    if (filename == ""):
        print("Error... No file name was entered")
    else:
        print(filename)

from tkinter import *
gui = Tk()
gui.geometry("1200x600")
L1 = Label(gui, text="File Name:")
L1.pack()
E1 = Entry(gui, bd =2)
E1.pack(fill = X)
B = Button(gui, text ="Analyse File", command = openfile)
B.pack()
gui.mainloop()

# open and read specified file


# part 2: views by country/continent 


# part 3: views by browser


# part 4: reader profiles


# part 5: also likes functionnality


# part 6: also likes graph


