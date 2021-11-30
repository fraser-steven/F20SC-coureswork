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

# ------------part 2: views by country/continent------------
# part a for countries 
def show_views_by_country_hist():
    count = Counter(visitor['visitor_country'] for visitor in data)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Country')
    plt.ylabel('Frequency')
    plt.title('Histogram Showing Views by Country')
    plt.bar(count.keys(), count.values())
    plt.show() 

# part b for continent
def show_views_by_continent_hist():
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
        browser = i.split(' ')[0]
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
    readers_of_document = [] 
    for entry in data:
        try:
            if (entry['subject_doc_id'] == document_uuid):
                readers_of_document.append(entry['visitor_uuid'])
        # if subject_doc_id or env_doc_id was missing just pass
        except Exception:
            pass
    return list(set(readers_of_document)) # because we don't want to count the same user more than once

# part b
def get_documents_read_by_user(visitor_uuid):
    documents_read = []
    for entry in data:
        try:
            if (entry['visitor_uuid'] == visitor_uuid):
                doc_id = entry['subject_doc_id']
                if (doc_id):
                    documents_read.append(doc_id)
        # an entry may have a missing value and in the case it does just pass
        except Exception:
            pass
    return list(set(documents_read)) # because we dont want to count the same user reading the document more than once 

# get_documents_view_count_by_visitors is a helper function for part c and d
def get_documents_view_count_by_visitors(visitors_list):
    # make list of all documents 
    # documents = [i['subject_doc_id'] for i in data] <----- makes KeyError because some values must be missing
    documents = []
    for entry in data:
        try:
            documents.append(entry['subject_doc_id'])
        except Exception:
            pass
    documents = list(set(documents))
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

# part c
def also_likes(document_uuid, visitor_uuid=None):
    if (visitor_uuid): 
        # check if visitor_uuid viewed document_uuid
        visited_docs = get_readers_of_document(document_uuid)
        if (visited_docs.count(visitor_uuid) == 0):
            raise Exception("Error... Invalid parameters, visitor_uuid did not view document_uuid")
            print("Error... Invalid parameters, visitor_uuid did not view document_uuid")
    # get a list of all the readers of document_uuid
    readers_of_document = get_readers_of_document(document_uuid)
    # use the helper function explained above to get a dictionary of all the documents 
    # with values of how many times they were read by the specified readers
    documents_view_counts = get_documents_view_count_by_visitors(readers_of_document)
    documents_view_counts = list(documents_view_counts.items())
    # make a list of only the document uuids 
    liked_documents_list = [document[0] for document in documents_view_counts if (document[1] != -1)]
    # coursework spec says "sorted by the sorting function parameter"
    liked_documents_list.sort()
    # make sure document_uuid is not in the list
    try:
        liked_documents_list.remove(document_uuid) 
    except Exception: # if the document is not in this list this will throw ValueError
        pass
    # printing stuff to show results in terminal
    likes_count = len(liked_documents_list)
    if (likes_count>0):
        print("\nAlso Likes List: ")
        for doc_id in liked_documents_list:
            print(" - "+doc_id)
    else:
        print("\nNo Also Liked Documents Found...")
    return liked_documents_list

#part d
def top_10_also_likes(document_uuid, visitor_uuid=None):
    if (visitor_uuid): 
        # check if visitor_uuid viewed document_uuid
        visited_docs = get_readers_of_document(document_uuid)
        if (visited_docs.count(visitor_uuid) == 0):
            raise Exception("Error... Invalid parameters, visitor_uuid did not view document_uuid")
            print("Error... Invalid parameters, visitor_uuid did not view document_uuid")

    # get a list of all the readers of document_uuid
    readers_of_document = get_readers_of_document(document_uuid)
    # use the helper function explained above to get a dictionary of all the documents 
    # with values of how many times they were read by the specified readers
    readers_of_document = list(set(readers_of_document))
    documents_view_counts = get_documents_view_count_by_visitors(readers_of_document)
    # sort documents from most read to least read
    sort = sorted(documents_view_counts.items(), key=lambda kv: kv[1], reverse=True)
    sort = list(sort)
    # make a list of only the document uuids 
    liked_documents_list = [document[0] for document in sort if (document[1] != -1)]
    # make sure document_uuid is not in the list
    try:
        liked_documents_list.remove(document_uuid)
    except Exception: # if the document is not in this list this will throw ValueError
        pass
    # get the top 10
    also_likes = liked_documents_list[:10]
    no_also_likes = len(also_likes)
    # printing stuff to show results in terminal
    if (no_also_likes == 10): 
        print("\nTop 10 Documents and their Number of Views: ")
    elif (no_also_likes>0): 
        print("\nOnly "+str(no_also_likes)+" Also Likes documents were found.")
        print("Top "+str(no_also_likes)+" Documents and their Number of Views: ")
    else: # no results
        print("\nNo Also Liked Documents Found...")
    i=1
    values = []
    for doc in also_likes:
        values.append(documents_view_counts[doc])
        print("\nDocument Rank #"+str(i))
        print("Document with ID:"+str(doc))
        print("Number of Views by Unique Viewers: "+str(documents_view_counts[doc]))
        i = i+1
    # bar chart of number of views for the top 10 documents
    also_likes_shortened = [d[-4:] for d in also_likes]
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Document UUID')
    plt.ylabel('Number of times the document was viewed.')
    plt.title('Bar Chart Showing Also Likes for Top 10 Liked Documents')
    plt.bar(also_likes_shortened, values)
    plt.show()
    return also_likes

# ------------part 6: also likes graph------------
def show_also_likes_graph(document_uuid, visitor_uuid):
    #create the graph
    graph = pydot.Dot("also_likes_graph", graph_type="digraph", bgcolor="white")
    #get data from the part c function, these will be the document nodes
    documents = also_likes(document_uuid, visitor_uuid)
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
        # first make the visitor node
        # if the visitor uuid is the input visitor uuid then the node should be green, otherwise it is white
        if (vis_uuid == visitor_uuid):
            graph.add_node(pydot.Node(uuid, shape="box", fillcolor="green", style="filled"))
        else:
            graph.add_node(pydot.Node(uuid, shape="box", fillcolor="white", style="filled"))
        
        # to make the relationship edge we need to see which documents this visitor viewed
        documents_viewed_by_visitor = get_documents_read_by_user(vis_uuid)
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

# this function generates buttons to show the graphs for part 5 and 6 once the user has input a document uuid (and visitor uuid if desired)
# the function also checks that the information inputted by the user is correct
def make_and_show_buttons_also_likes():
    global E2
    global E3
    global L6
    global gui2
    global opened_also_likes
    document_uuid = E2.get()
    visitor_uuid = E3.get()
    if (document_uuid == ""):
        L6.configure(text="Error... No document_uuid entered, document_uuid is required.")
        print("Error... No document_uuid entered, document_uuid is required.")
    else:
        L6.configure(text="")
        if (visitor_uuid == ""):
            visitor_uuid = None
        if (opened_also_likes == False):
            B7 = Button(gui2, text ="Also Likes List", command=lambda:also_likes(document_uuid, visitor_uuid))
            B7.pack()
            B8 = Button(gui2, text ="Also Likes Top 10 Documents", command=lambda:top_10_also_likes(document_uuid, visitor_uuid))
            B8.pack()
            B9 = Button(gui2, text ="Show Also Likes Graph", command=lambda:show_also_likes_graph(document_uuid, visitor_uuid))
            B9.pack()
            opened_also_likes = True

# this function opens the also likes facility
def open_also_likes_facility():
    global filename
    global E2
    global E3
    global L6
    global gui2
    global opened_also_likes
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
    gui2.mainloop()

# this function generates the buttons for parts 1 to 4 once a file has been entered by the user using the gui
def make_and_show_buttons():
    global opened_file
    global B7
    if (opened_file == False):
        B7.configure(text = "Update")
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

# ------------file reading stuff------------
# open and read specified file
def openfile():
    print("open file button pressed")
    global filename
    filename = E1.get()
    if (filename == ""):
        L2.configure(text="Error... No file name was entered")
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
        global data
        global tkinter_open
        data = [json.loads(line) for line in open(fname, 'r')]
        return True
    except (FileNotFoundError):
        if tkinter_open: 
            print("Error...File not found")
            L2.configure(text="Error...File not found")
        else:
            raise Exception("Error...File not found")
        return False

# ------------part 8: Command line usage------------
def run_task(task_id, document_uuid=None, visitor_uuid=None):
    global data
    if task_id == "2a":
        show_views_by_country_hist()
    elif task_id == "2b":
        show_views_by_continent_hist()
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
        top_10_also_likes(document_uuid, visitor_uuid)
    elif task_id == "6":
        show_also_likes_graph(document_uuid, visitor_uuid)
    elif task_id == "7":
        # task id 7 should run Task 6 and automatically launch a GUI with fields to input document and 
        # (optionally user ids and show the resulting also-likes graph).
        if data:
            open_also_likes_facility()

# if arguments have been entered then application uses command line interface and wont load the gui
# so need to check if there is more than one argument
# one argument is the file name
if (len(sys.argv) != 1):
    command_line_activated = True
    document_uuid = None
    visitor_uuid = None
    task_id = None
    arg_count = len(sys.argv)-1
    # there should be an even number of arguments exclusing the name of the python file
    if ((arg_count%2) != 0):
        raise Exception('A problem has been detected with the arguments you have input. \nPlease try again...')
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
            print(option)
            raise Exception('A problem has been detected with the arguments you have input. \nPlease try again...')
    # we need to read the file
    if (open_file_and_set_data(filename)):
        # now run the task that was specified
        run_task(task_id, document_uuid, visitor_uuid)

# ------------part 7: GUI using tkinter------------
def generate_gui():
    global gui
    global E1
    global L2
    global B
    global tkinter_open
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
