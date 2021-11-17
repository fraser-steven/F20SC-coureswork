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
    plt.xlabel('Country')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Country')
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
    plt.xlabel('Continent')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Continent')
    plt.hist(output)
    plt.show()

# ------------part 3: views by browser------------
# part a but we dont use this
def show_views_by_browser_a(data):
    count = Counter(visitor['visitor_useragent'] for visitor in data)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Browser')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Browser')
    plt.hist(count)
    plt.show()
# part b this is what we actually display
def show_views_by_browser_b(data):
    count = Counter(visitor['visitor_useragent'] for visitor in data)
    browsers = []
    for i in count:
        browser = i.split(' ')[0]
        browsers.append(browser)
    output = Counter(browsers)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Browser')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Browser')
    plt.hist(output)
    plt.show()

# ------------part 4: reader profiles------------
def show_reader_profile_info(data):
    
    
    visitors = [i['visitor_uuid'] for i in data]
    #list of visitor uuids
    visitors_2 = list(set(visitors))
    #create a dictionary of the uudis with empty values
    visitor_times = dict([(key, []) for key in visitors_2])
    time = 0
    for key in visitor_times:
        for x in data:
            if key == x['visitor_uuid']:
                try:
                    #set the time viewing documents 
                    time = x['event_readtime']
                    #set the value of the matching key to the time
                    visitor_times[key] = time
                    #if there is not a event_readtime for the visitor then handle it
                except Exception:
                    pass
    #sort to have longest reading time to shortest
    sort = sorted(visitor_times, key=lambda kv: kv[1], reverse=True)
    #get the top 10 visitors who spend the longest reading
    top10 = list(sort)[:10]
    print(top10)
    
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
    B4 = Button(gui, text ="Show Views by Browser Histogram", command=lambda:show_views_by_browser_b(data))
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

