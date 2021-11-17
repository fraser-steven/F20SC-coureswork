# F20SC: Industrial Programming 
# Coursework 2
# Data Analysis of a Document Tracker

# Fraser Steven (fs65)
# Tegan Friedenthal (tf50)

# imports
import json
from collections import Counter
import matplotlib.pyplot as plt
import pycountry_convert as pc
from tkinter import *

# ------------part 2: views by country/continent------------
# part a for countries 
def show_views_by_country_hist(data):
    count = Counter(visitor['visitor_country'] for visitor in data)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('country')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.hist(count)
    plt.show() 

# part b for continent
def show_views_by_continent_hist(data):
    count = Counter(visitor['visitor_country'] for visitor in data)
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

# ------------part 3: views by browser------------
def show_views_by_browser(data):
    print("TO DO")

# ------------part 4: reader profiles------------
def show_reader_profile_info(data):
    print("TO DO")

# ------------part 5: also likes functionnality------------
def also_likes(data):
    print("TO DO")

# ------------part 6: also likes graph------------
def show_also_likes_graph(data):
    print("TO DO")

# ------------Helper Functions------------
def make_and_show_buttons(data):

    B2 = Button(gui, text ="Show Views by Country Histogram", command=lambda:show_views_by_country_hist(data))
    B2.pack()

    B3 = Button(gui, text ="Show Views by Continent Histogram", command=lambda:show_views_by_continent_hist(data))
    B3.pack()

    B4 = Button(gui, text ="Show Views by Browser Histogram", command=lambda:show_views_by_browser(data))
    B4.pack()

    B5 = Button(gui, text ="Show Reader Profiles Information", command=lambda:show_reader_profile_info(data))
    B5.pack()

    B6 = Button(gui, text ="Show Also Likes Graph", command=lambda:show_also_likes_graph(data))
    B6.pack()

# ------------file reading stuff------------
# open and read specified file
def openfile():
    print("open file button pressed")
    filename = E1.get()
    if (filename == ""):
        L2.configure(text="Error... No file name was entered")
        print("Error... No file name was entered")
    else:
        labeltext = "Reading file: "+filename
        L2.configure(text=labeltext)
        data = open_file_and_return_data(filename)
        if (data):
            make_and_show_buttons(data)

# opens the file and stores the data
def open_file_and_return_data(fname):
    try:
        data = [json.loads(line) for line in open(fname, 'r')]
        return data
    except (FileNotFoundError):
        print("Error...File not found")
        L2.configure(text="Error...File not found")
        return False

# ------------part 7: GUI using tkinter------------
gui = Tk()
gui.title("Document Tracker Data Analyzer")
gui.geometry("600x400")
L1 = Label(gui, text="File Name:")
L1.pack()
E1 = Entry(gui, bd =2)
E1.pack()
B = Button(gui, text ="Analyze File", command = openfile)
B.pack()
L2 = Label(gui, text="")
L2.pack()
L3 = Label(gui, text="")
L3.pack()
gui.mainloop()
