# F20SC: Industrial Programming 
# Coursework 2
# Data Analysis of a Document Tracker

# Fraser Steven (fs65)
# Tegan Friedenthal (tf50)
import json
from collections import Counter
import matplotlib.pyplot as plt
import pycountry_convert as pc

# part 7: GUI using tkinter
filename = ""
def openfile():
    print("open file button pressed")
    filename = E1.get()
    if (filename == ""):
        L2.configure(text="Error... No file name was entered")
        print("Error... No file name was entered")
    else:
        labeltext = "Opening file: "+filename
        L2.configure(text=labeltext)

from tkinter import *
gui = Tk()
gui.title("Document Tracker Data Analyzer")
gui.geometry("1200x600")
L1 = Label(gui, text="File Name:")
L1.pack(side=LEFT, anchor=N)
E1 = Entry(gui, bd =2)
E1.pack(fill = X,side=LEFT, anchor=N)
B = Button(gui, text ="Analyze File", command = openfile)
B.pack(side=LEFT, anchor=N)

L2 = Label(gui, text="")
L2.pack(side=LEFT, anchor=N)

gui.mainloop()

# open and read specified file
#opens the file and stores the data
data = [json.loads(line) for line in open(filename, 'r')]

# part 2: views by country/continent 

#part a for countries 
count = Counter(visitor['visitor_country'] for visitor in data)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('country')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.hist(count)
plt.show() 

#part b for continent
continents = []
for i in count:
	try:
		count
		country_code = (i)
		r = pc.country_alpha2_to_continent_code(country_code)
		continents.append(r)
	except Exception:
		pass
output = Counter(continents)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('continent')
plt.ylabel('Frequency')
plt.title('Histogram')
plt.hist(output)
plt.show()

# part 3: views by browser


# part 4: reader profiles


# part 5: also likes functionnality


# part 6: also likes graph


