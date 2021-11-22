# F20SC: Industrial Programming 
# Coursework 2
# Data Analysis of a Document Tracker

# Fraser Steven (fs65)
# Tegan Friedenthal (tf50)

# Good Document UUID's for testing part 5:
# - 131216030921-437624c61000e4b0cfabd4cc13f06ae1
# - 140228063757-c3f65672a508185d19b16e1c4049f83d
# - 130520152036-0fc36dda7e7546bdb943026e50690814
# - 130726171426-7e867e41ac7ebc63ffdce78d7cbb2ab8

# ------------Imports------------
import json
from collections import Counter
import matplotlib.pyplot as plt
import pycountry_convert as pc
from tkinter import *
import sys

# ------------Variables------------
data = None
filename = None
E2 = None
E3 = None
L6 = None
gui2 = None 

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
    return readers_of_document
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
    return documents_read
# get_documents_view_count_by_visitors is a helper function for part c and d
def get_documents_view_count_by_visitors(readers_list):
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
    for reader in readers_list:
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
    if (visitor_uuid): # if a visitor uuid has been specified then we only want other documents read by THIS reader
        # check if visitor_uuid viewed document_uuid
        visited_docs = get_readers_of_document(visitor_uuid)
        if (visited_docs.count(document_uuid)>0):
            readers_of_document = [visitor_uuid]
        else:
            raise Exception("Error... Invalid parameters, visitor_uuid did not view document_uuid")
            print("Error... Invalid parameters, visitor_uuid did not view document_uuid")
    else:
        # get a list of all the readers of document_uuid
        readers_of_document = get_readers_of_document(document_uuid)
        readers_of_document = list(set(readers_of_document))
    # use the helper function explained above to get a dictionary of all the documents 
    # with values of how many times they were read by the specified readers
    documents_view_counts = get_documents_view_count_by_visitors(readers_of_document)
    documents_view_counts = list(documents_view_counts.items())
    # make a list of only the document uuids 
    liked_documents_list = [document[0] for document in documents_view_counts if (document[1] != -1)]
    # coursework spec says "sorted by the sorting function parameter"
    #liked_documents_list.sort()
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
        print(liked_documents_list)
    else:
        print("\nNo Also Liked Documents Found...")
    return liked_documents_list
#part d
def top_10_also_likes(document_uuid, visitor_uuid=None):
    if (visitor_uuid): # if a visitor uuid has been specified then we only want other documents read by THIS reader
        # check if visitor_uuid viewed document_uuid
        visited_docs = get_readers_of_document(visitor_uuid)
        if (visited_docs.count(document_uuid)>0):
            readers_of_document = [visitor_uuid]
        else:
            raise Exception("Error... Invalid parameters, visitor_uuid did not view document_uuid")
            print("Error... Invalid parameters, visitor_uuid did not view document_uuid")
    else:
        # get a list of all the readers of document_uuid
        readers_of_document = get_readers_of_document(document_uuid)
        readers_of_document = list(set(readers_of_document))
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
        print("Number of Views: "+str(documents_view_counts[doc]))
        i = i+1
    # bar chart of number of views for the top 10 documents
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Document UUID')
    plt.ylabel('Number of times the document was viewed.')
    plt.title('Bar Chart Showing Also Likes for Top 10 Liked Documents')
    plt.bar(also_likes, values)
    plt.show()
    return also_likes

# ------------part 6: also likes graph------------
def show_also_likes_graph(document_uuid, visitor_uuid):
    print("TO DO")

# ------------Helper Functions------------
def test_also_likes():
    docs = []
    for entry in data:
        try:
            doc_id = entry['subject_doc_id']
            docs.append(doc_id)
        except Exception:
            pass
    docs = list(set(docs))
    for doc in docs:
        top_10_also_likes(doc)
def make_and_show_buttons_also_likes():
    global E2
    global E3
    global L6
    global gui2
    document_uuid = E2.get()
    visitor_uuid = E3.get()
    if (document_uuid == ""):
        L6.configure(text="Error... No document_uuid entered, document_uuid is required.")
        print("Error... No document_uuid entered, document_uuid is required.")
    else:
        L6.configure(text="")
        if (visitor_uuid == ""):
            visitor_uuid = None
        B7 = Button(gui2, text ="Also Likes List", command=lambda:also_likes(document_uuid, visitor_uuid))
        B7.pack()
        B8 = Button(gui2, text ="Also Likes Top 10 Documents", command=lambda:top_10_also_likes(document_uuid, visitor_uuid))
        B8.pack()
        B9 = Button(gui2, text ="Show Also Likes Graph", command=lambda:show_also_likes_graph(document_uuid, visitor_uuid))
        B9.pack()
def open_also_likes_facility():
    global filename
    global E2
    global E3
    global L6
    global gui2
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
    B7 = Button(gui2, text ="Find Also Likes", command=make_and_show_buttons_also_likes)
    B7.pack()
    L6 = Label(gui2, text="")
    L6.pack()
    gui2.mainloop()

def make_and_show_buttons():
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
        if(open_file_and_get_data(filename)):
            make_and_show_buttons()
            # FOR TESTING COMMENT THIS OUT LATER!!!!!
            # test_also_likes()

# opens the file and stores the data
def open_file_and_get_data(fname):
    try:
        global data
        data = [json.loads(line) for line in open(fname, 'r')]
        return True
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

# ------------part 8: Command line usage------------

#make sure that the correct amount of arguments have been given in the CLI
if len(sys.argv) != 9:
    raise ValueError('Please provide enough args.')

#parse the input and save to variables
visitor_uuid = sys.argv[2]
document_uuid = sys.argv[4]
task_id = sys.argv[6]
file_name = sys.argv[8]
fname = file_name

#testing
#print(f'args are {visitor_uuid} {document_uuid} {task_id} {file_name}')

#test the functions are working with the arguments 
open_file_and_get_data(fname)
get_readers_of_document(document_uuid)
get_documents_read_by_user(visitor_uuid)
top_10_also_likes(document_uuid, visitor_uuid=None)
#display after implimented
show_also_likes_graph(document_uuid, visitor_uuid)

# ---------------------------------------------------
