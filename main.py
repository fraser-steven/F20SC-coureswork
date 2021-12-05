#!/usr/bin/env python3
# F20SC: Industrial Programming 
# Coursework 2
# Data Analysis of a Document Tracker

# Fraser Steven (fs65)
# Tegan Friedenthal (tf50)

# For issuu_cw2.json these are the top 10 documents with most unique viewers (and their unique view count):
# [('140224101516-e5c074c3404177518bab9d7a65fb578e', 26), 
# ('140228202800-6ef39a241f35301a9a42cd0ed21e5fb0', 25), 
# ('140228101942-d4c9bd33cc299cc53d584ca1a4bf15d9', 24), 
# ('140227185725-ecdfa6bc363a0d30bd64535699f4a069', 17), 
# ('140204115519-f5fa6ce8b288c9f10e0c8bc7e1a456a0', 16), 
# ('140220182246-a781d17fb18fa53a7c0ae34242d71d3d', 13), 
# ('130313161023-ee03f65a89c7406fa097abe281341b42', 11), 
# ('121109150636-bdf13c63b3964e1494a82f6c144024e2', 11), 
# ('131224090853-45a33eba6ddf71f348aef7557a86ca5f', 9), 
# ('140224132818-2a89379e80cb7340d8504ad002fab76d', 8)]
# ...This is irrelevant to the coursework specification but interesting for testing

# Testing commands for command line usage:
# python main.py -t 4 -f issuu_cw2.json
# python main.py -u 232eeca785873d35 -d 131216030921-437624c61000e4b0cfabd4cc13f06ae1 -t 6 -f issuu_cw2.json
# python main.py -d 140228202800-6ef39a241f35301a9a42cd0ed21e5fb0 -t 6 -f issuu_cw2.json
# python main.py -d 140217151103-d89a87d94a00d7b7089338802ecddd65 -t 6 -f issuu_cw2.json
# python main.py -t 7 -f issuu_cw2.json

# ------------Imports------------
import json
from collections import Counter
import matplotlib.pyplot as plt
import pycountry_convert as pc
from tkinter import *
import sys
import pydot
from PIL import ImageTk,Image  

# ------------Variables------------
data = None
filename = None
opened_file = False
opened_also_likes = False
tkinter_open = False
command_line_activated = False
# gui variables
E2 = None
E3 = None
L6 = None
gui2 = None 
gui = None 
E1 = None 
L2 = None 
B = None
B7 = None
B2 = None
B3 = None
B4 = None
B5 = None
B6 = None
B7 = None
B8 = None
B9 = None
B10 = None

# ------------part 2: views by country/continent------------
# part a for countries 
def show_views_by_country_hist(document_uuid=None):
    if (document_uuid):
        count = Counter(entry['visitor_country'] for entry in data if (entry['subject_doc_id'] == document_uuid))
    else:
        count = Counter(visitor['visitor_country'] for visitor in data)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Country')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Country')
    plt.bar(count.keys(), count.values())
    plt.show() 

# part b for continent
def show_views_by_continent_hist(document_uuid=None):
    if (document_uuid):
        count = Counter(entry['visitor_country'] for entry in data if (entry['subject_doc_id'] == document_uuid))
    else:
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
    plt.bar(output.keys(), output.values())
    plt.show()

# ------------part 3: views by browser------------
# part a but we dont use this
def show_views_by_browser_a():
    count = Counter(visitor['visitor_useragent'] for visitor in data)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Browser')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Browser')
    plt.bar(count.keys(), count.values())
    plt.show()

# part b this is what we actually display
def show_views_by_browser_b():
    count = Counter(visitor['visitor_useragent'] for visitor in data)
    browsers = []
    for i in count:
        browser = i.split('/')[0]
        browsers.append(browser)
    output = Counter(browsers)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Browser')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Browser')
    plt.bar(output.keys(), output.values())
    plt.show()

# ------------part 4: reader profiles------------
def show_reader_profile_info():
    visitors = [i['visitor_uuid'] for i in data]
    #list of visitor uuids
    visitors_2 = list(set(visitors))
    #create a dictionary of the uudis with empty values
    visitor_times = dict([(key, -1) for key in visitors_2])
    time = 0
    for key in visitor_times:
        for x in data:
            if key == x['visitor_uuid']:
                try:
                    #set the time viewing documents 
                    time = x['event_readtime']
                    #set the value of the matching key to the time
                    if visitor_times[key] == -1:
                        visitor_times[key] = time
                    else: # users may have already viewed another document
                        curvalue = visitor_times[key]
                        newvalue = curvalue + time
                        visitor_times[key] = newvalue
                #if there is not a event_readtime for the visitor then handle it
                except Exception:
                    pass
    #sort to have longest reading time to shortest
    sort = sorted(visitor_times.items(), key=lambda kv: kv[1], reverse=True)
    #get the top 10 visitors who spend the longest reading
    top10 = list(sort)[:10]
    keys = []
    values = []
    i=1
    print("\nTop 10 Readers and their Time Spent Reading: ")
    for user in top10:
        keys.append(user[0])
        values.append(user[1])
        print("\nReader Rank #"+str(i))
        print("Reader with ID:"+str(user[0]))
        print("Spent Total Time Reading: "+str(user[1]))
        i = i+1
    # bar chart of times spent by the top 10 viewers
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Viewer ID')
    plt.ylabel('Time Spent Reading Documents')
    plt.title('Bar Chart Showing Reader Profile Info for Top 10 Readers')
    plt.bar(keys, values)
    plt.show()

# ------------part 5: also likes functionnality------------
# part a
def get_readers_of_document(document_uuid):
    if (document_uuid == None):
        print("Error... You did not provide a document UUID.")
        exit(0)
    readers_of_document = [] 
    # event_types  = ['continuation_load', 'impression', 'pageread', 'read', 'share', 'pagereadtime', 'click']
    # cause_types = ['embed', 'archive', 'ad', 'impression', 'related', 'page']
    # subject_types = ['doc', 'infobox', 'link']
    # env_types = ['website', 'reader', 'stream']
    # env_names = ['sidebarmorefromauthor', 'search', 'mysubscriptions', 'stack', 'explore', 'mystackssingle', 'curated', 'related', 'myfeed', 'profile']
    for entry in data:
        try:
            if ((entry['subject_doc_id'] == document_uuid) and (entry["env_type"] == "reader") and (entry["event_type"] == "read")):
                vis_uuid = entry['visitor_uuid']
                if (vis_uuid):
                    readers_of_document.append(vis_uuid)
        # if subject_doc_id or env_doc_id was missing just pass
        except Exception:
            pass
    return list(set(readers_of_document)) # because we don't want to count the same user more than once

# part b
def get_documents_read_by_user(visitor_uuid):
    if (visitor_uuid == None):
        print("Error... You did not provide a visitor UUID.")
        exit(0)
    documents_read = []
    for entry in data:
        try:
            if ((entry['visitor_uuid'] == visitor_uuid) and (entry["env_type"] == "reader") and (entry["event_type"] == "read")):
                doc_id = entry['subject_doc_id']
                if (doc_id):
                    documents_read.append(doc_id)
        # an entry may have a missing value and in the case it does just pass
        except Exception:
            pass
    return list(set(documents_read)) # because we dont want to count the same user reading the document more than once 

# not used but could be used for testing
# LEAST to most views sorting function
def sort_least_to_most_views(documents_list):
    documents_view_counts  = dict([(key, -1) for key in documents_list])
    for document in documents_list:
        readers_count = len(get_readers_of_document(document))
        documents_view_counts[document] = readers_count
    
    # sort documents from least read to most read
    sort = sorted(documents_view_counts.items(), key=lambda kv: kv[1], reverse=False)
    sort = list(sort)
    # make a list of only the document uuids 
    sorted_list = [document[0] for document in sort]
    return sorted_list

# used for part d
# MOST to least views sorting function
def sort_most_to_least_views(documents_list):
    documents_view_counts  = dict([(key, -1) for key in documents_list])
    for document in documents_list:
        readers_count = len(get_readers_of_document(document))
        documents_view_counts[document] = readers_count
    
    # sort documents from most read to least read
    sort = sorted(documents_view_counts.items(), key=lambda kv: kv[1], reverse=True)
    sort = list(sort)
    # make a list of only the document uuids 
    sorted_list = [document[0] for document in sort]
    return sorted_list
    
# part c
def also_likes(document_uuid, visitor_uuid=None, sorting_function=None):
    if (visitor_uuid): 
        # check if visitor_uuid viewed document_uuid
        visited_docs = get_readers_of_document(document_uuid)
        if (visited_docs.count(visitor_uuid) == 0):
            print("Error... Invalid parameters, visitor_uuid did not view document_uuid")
            exit(0)
    # get a list of all the readers of document_uuid
    readers_of_document = get_readers_of_document(document_uuid)
    if (visitor_uuid): 
        # we only want documents liked by OTHER users who like this document
        readers_of_document.remove(visitor_uuid)

    # find also liked documents
    liked_documents_list = []
    for reader in readers_of_document:
        # for every reader find all the documents they read and add them to the list
        documents = get_documents_read_by_user(reader)
        for doc in documents:
            liked_documents_list.append(doc)
    # only keep unique documents
    list(set(liked_documents_list))

    # make sure document_uuid is not in the list
    try:
        liked_documents_list.remove(document_uuid) 
    except Exception: # if the document is not in this list this will throw ValueError
        pass

    # coursework spec says "sorted by the sorting function parameter"
    # sort with the sorting_function if one has been provided
    if sorting_function:
        liked_documents_list = sorting_function(liked_documents_list)

    # printing stuff to show results in terminal
    likes_count = len(liked_documents_list)
    if (likes_count>0):
        print("\nAlso Likes List: ")
        for doc_id in liked_documents_list:
            print(" - "+doc_id)
    else:
        print("\nNo Also Liked Documents Found...")
    return liked_documents_list

# part d
def top_10_also_likes(document_uuid, visitor_uuid=None, display_chart=None):
    # using sorting function: sort_most_to_least_views
    # and also using also_likes function from part c
    also_likes_list = also_likes(document_uuid, visitor_uuid, sort_most_to_least_views)
    # return only top 10 results
    return also_likes_list[:10]

# ------------part 6: also likes graph------------
def show_also_likes_graph(document_uuid, visitor_uuid):
    #create the graph
    graph = pydot.Dot("also_likes_graph", graph_type="digraph", bgcolor="white")
    #get data from the part c function, these will be the document nodes
    documents = top_10_also_likes(document_uuid, visitor_uuid, False)
    # then get all of the readers of the input docuemnt, these will be the visitor nodes
    visitors_of_input_document = get_readers_of_document(document_uuid)
    # add the input document to documents because these are also likes documents so dont include the input document yet
    documents.append(document_uuid)
    # make all the document nodes
    for doc in documents:
        #shorten document_uuid to last 4 characters
        doc_uuid = doc[-4:]
        # if the doument uuid is the input document uuid then the node should be green, otherwise it is white
        if (doc == document_uuid):
            graph.add_node(pydot.Node(doc_uuid, shape="circle", fillcolor="green", style="filled"))
        else:
            graph.add_node(pydot.Node(doc_uuid, shape="circle", fillcolor="white", style="filled"))

    # now make the visitor nodes and relationship edges
    for vis_uuid in visitors_of_input_document:
        #shorten the uuid to the last 4 characters 
        uuid = vis_uuid[-4:]

        # to make the relationship edge we need to see which documents this visitor viewed
        documents_viewed_by_visitor = get_documents_read_by_user(vis_uuid)
        only_document_uuid = [document_uuid]
        if (documents_viewed_by_visitor != only_document_uuid):
            # first make the visitor node
            # if the visitor uuid is the input visitor uuid then the node should be green, otherwise it is white
            if (vis_uuid == visitor_uuid):
                graph.add_node(pydot.Node(uuid, shape="box", fillcolor="green", style="filled"))
            else:
                graph.add_node(pydot.Node(uuid, shape="box", fillcolor="white", style="filled"))
            
            for doc in documents_viewed_by_visitor:
                # for each document the visitor has viewed check if it is in the also likes documents
                # if so then make a relationship edge
                if (documents.count(doc) != 0):
                    #shorten document_uuid to last 4 characters
                    doc_uuid = doc[-4:]
                    # add edge from visitor_uuid to document_uuid to show "also_likes" relationship 
                    graph.add_edge(pydot.Edge(uuid, doc_uuid, color="black"))

    #output image of the graph
    img_name = document_uuid + ".png"
    graph.write_png(img_name)
    image = Image.open(img_name)
    image.show()

# ------------Helper Functions------------
# function useful for testing
def get_documents_view_count_by_visitors(visitors_list):
    # make list of all documents 
    # documents = [i['subject_doc_id'] for i in data] <----- makes KeyError because some values must be missing
    documents = get_unique_documents_in_file()
    # make dictionary of documents with all values -1 to initialize
    documents_view_counts  = dict([(key, -1) for key in documents])
    for reader in visitors_list:
        # iterate through the list and for each reader get a list of all the documents they have read
        documents_read_by_user = get_documents_read_by_user(reader)
        for document in documents_read_by_user:
            # iterate through the documents they have read and store the view counts in the dictionary
            if (documents_view_counts[document] == -1): 
                documents_view_counts[document] = 1
            else:
                documents_view_counts[document] = documents_view_counts[document]+1
    # return the unsorted dictionary
    return documents_view_counts

# This function gets the top 10 documents from the opened file and their number of unique viewers and prints them
def test_also_likes(): 
    all_readers = []
    for entry in data:
        try:
            user_id = entry['visitor_uuid']
            all_readers.append(user_id)
        except Exception:
            pass
    all_readers = list(set(all_readers))
    documents_view_counts = get_documents_view_count_by_visitors(all_readers)
    sort = sorted(documents_view_counts.items(), key=lambda kv: kv[1], reverse=True)
    sort = list(sort)
    print(sort[:10])

# also likes page generates buttons after user inputs valid document uuid
# if they re enter bad data eg. empty string we need to remove the buttons
def hide_also_likes_buttons():
    global B10, B8, B9, opened_also_likes
    if (opened_also_likes):
        B8.pack_forget()
        B9.pack_forget()
        B10.pack_forget()
        opened_also_likes = False

# this function gets a list of all unique document uuids in the file
def get_unique_documents_in_file():
    documents = []
    for entry in data:
        try:
            documents.append(entry['subject_doc_id'])
        except Exception:
            pass
    documents = list(set(documents))
    return documents

# this function generates buttons to show the graphs for part 5 and 6 once the user has input a document uuid (and visitor uuid if desired)
# the function also checks that the information inputted by the user is correct
def make_and_show_buttons_also_likes():
    global E2, E3, L6, gui2, opened_also_likes, B7, B8, B9, B10
    B7.configure(text="Update Document UUID/ User UUID")
    document_uuid = E2.get()
    visitor_uuid = E3.get()
    documents = get_unique_documents_in_file()
    approved = True

    # check document uuid is valid
    # check if a document uuid was entered
    if (document_uuid == ""):
        approved = False
        hide_also_likes_buttons()
        L6.configure(text="Error... No document_uuid entered, document_uuid is required.")
        print("Error... No document_uuid entered, document_uuid is required.")
    # check if the document exists in the file
    elif (documents.count(document_uuid) == 0):
        approved = False
        hide_also_likes_buttons()
        L6.configure(text="Error... The document uuid entered does not exist in the file you have choosen.")
        print("Error... The document uuid entered does not exist in the file you have choosen.")
    
    # check visitor uuid is valid
    # check if a visitor uuid was entered
    if (visitor_uuid == ""):
        visitor_uuid = None
    elif (visitor_uuid != ""): # visitor uuid not empty therefore the user has given an input for this field
        # check if the user exists in the file and if they have viewed the specified document
        user_viewed_docs = get_documents_read_by_user(visitor_uuid)
        if (user_viewed_docs.count(document_uuid) == 0):
            approved = False
            hide_also_likes_buttons()
            L6.configure(text="Error... The visitor specified did not view the document you have specified.")
            print("Error... The visitor specified did not view the document you have specified.")

    # all user input checks complete now proceed to generate buttons if the buttons have not already been generated
    if (approved):
        L6.configure(text="Input(s) approved!")
    
    if (approved and (opened_also_likes==False)):
        B10 = Button(gui2, text ="Also Likes List", command=lambda:also_likes(document_uuid, visitor_uuid))
        B10.pack()
        B8 = Button(gui2, text ="Also Likes Top 10 Documents", command=lambda:top_10_also_likes(document_uuid, visitor_uuid, true))
        B8.pack()
        B9 = Button(gui2, text ="Show Also Likes Graph", command=lambda:show_also_likes_graph(document_uuid, visitor_uuid))
        B9.pack()
        opened_also_likes = True

# this function opens the also likes facility
def open_also_likes_facility():
    global filename,E2,E3,L6,B7,gui2,opened_also_likes
    opened_also_likes = False
    gui2 = Tk()
    gui2.title("Also Likes Facility for file: "+filename)
    gui2.geometry("600x400")
    L4 = Label(gui2, text="Enter document_uuid:")
    L4.pack()
    E2 = Entry(gui2, bd =2)
    E2.pack()
    L5 = Label(gui2, text="Enter visitor_uuid (optional):")
    L5.pack()
    E3 = Entry(gui2, bd =2)
    E3.pack()
    B7 = Button(gui2, text ="Enter", command=make_and_show_buttons_also_likes)
    B7.pack()
    L6 = Label(gui2, text="")
    L6.pack()
    L7 = Label(gui2, text="")
    L7.pack()
    gui2.mainloop()

# this function generates the buttons for parts 1 to 4 once a file has been entered by the user using the gui
def make_and_show_buttons():
    global opened_file, B2, B3, B4, B5, B6
    if (opened_file == False):
        B2 = Button(gui, text ="Show Views by Country Histogram", command=show_views_by_country_hist)
        B2.pack()
        B3 = Button(gui, text ="Show Views by Continent Histogram", command=show_views_by_continent_hist)
        B3.pack()
        B4 = Button(gui, text ="Show Views by Browser Histogram", command=show_views_by_browser_b)
        B4.pack()
        B5 = Button(gui, text ="Show Reader Profiles Information", command=show_reader_profile_info)
        B5.pack()
        B6 = Button(gui, text ="Open Also Likes Facility", command=open_also_likes_facility)
        B6.pack()
        opened_file = True

# main page generates buttons after user inputs valid file name
# if they re enter bad data eg. empty string  or file does not exist we need to remove the buttons
def hide_file_page_buttons():
    global opened_file, B2, B3, B4, B5, B6
    if (opened_file):
        B2.pack_forget()
        B3.pack_forget()
        B4.pack_forget()
        B5.pack_forget()
        B6.pack_forget()
        opened_file = False

# ------------file reading stuff------------
# open and read specified file
def openfile():
    print("open file button pressed")
    global filename
    filename = E1.get()
    if (filename == ""):
        hide_file_page_buttons()
        L2.configure(text="Error... No file name was entered.")
        print("Error... No file name was entered")
    else:
        labeltext = "Reading file: "+filename
        L2.configure(text=labeltext)
        B.configure(text="Update File")
        if(open_file_and_set_data(filename)):
            make_and_show_buttons()

# opens the file and stores the data
def open_file_and_set_data(fname):
    try:
        global data, tkinter_open
        data = [json.loads(line) for line in open(fname, 'r')]
        return True
    except (FileNotFoundError):
        if tkinter_open: 
            print("Error...File not found")
            hide_file_page_buttons()
            L2.configure(text="Error...File not found")
        else:
            print("Error...File not found")
            exit(0)
        return False

# ------------part 8: Command line usage------------
def run_task(task_id, document_uuid=None, visitor_uuid=None):
    global data
    if task_id == "2a":
        show_views_by_country_hist(document_uuid)
    elif task_id == "2b":
        show_views_by_continent_hist(document_uuid)
    elif task_id == "3a":
        show_views_by_browser_a()
    elif task_id == "3b":
        show_views_by_browser_b()
    elif task_id == "4":
        show_reader_profile_info()
    elif task_id == "5a":
        get_readers_of_document(document_uuid)
    elif task_id == "5b":
        get_documents_read_by_user(visitor_uuid)
    elif task_id == "5c":
        also_likes(document_uuid, visitor_uuid)
    elif task_id == "5d":
        top_10_also_likes(document_uuid, True, visitor_uuid)
    elif task_id == "6":
        show_also_likes_graph(document_uuid, visitor_uuid)
    elif task_id == "7":
        # task id 7 should run Task 6 and automatically launch a GUI with fields to input document and 
        # (optionally user ids and show the resulting also-likes graph).
        if data:
            open_also_likes_facility()
    else:
        print("Error... You did not enter a valid task ID. \nPlease try again...")

# if arguments have been entered then application uses command line interface and wont load the gui
# so need to check if there are arguments
if (len(sys.argv) != 1):
    command_line_activated = True
    document_uuid = None
    visitor_uuid = None
    task_id = None
    arg_count = len(sys.argv) -1
    # there should be an even number of arguments exclusing the name of the python file
    if ((arg_count%2) != 0):
        print('A problem has been detected with the arguments you have input. \nPlease try again...')
        exit(0)
    index = 0
    while (index < arg_count): # set the variable values
        # possibilities: be -u -d -t -f
        index = index + 1
        option = sys.argv[index]
        index = index + 1 # increment the index
        if (option == "-u"):
            visitor_uuid = sys.argv[index]
        elif (option == "-d"):
            document_uuid = sys.argv[index]
        elif (option == "-t"):
            task_id = sys.argv[index]
        elif (option == "-f"):
            filename = sys.argv[index]
        else:
            print('A problem has been detected with the arguments you have input. \nPlease try again...')
            exit(0)
    # we need to read the file
    if (filename): # if a file has been specified
        if (open_file_and_set_data(filename)):
            # now run the task that was specified
            run_task(task_id, document_uuid, visitor_uuid)
    else:
        print('Error... You did not enter a filename to specify a file. \nA filename is needed to run any task. \nUse -f followed by the filename to specify a file. \nPlease try again...')
        exit(0)

# ------------part 7: GUI using tkinter------------
def generate_gui():
    global gui, E1, L2, B, tkinter_open
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
    tkinter_open = True
    gui.mainloop()
if (command_line_activated == False):
    generate_gui()
# ---------------------------------------------------
