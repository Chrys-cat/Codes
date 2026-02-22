#Test

import csv
import tkinter as tk

#gui
root = tk.Tk()
root.geometry("800x500")
root.title("tittle")
root.mainloop()


#open "colleges.csv" file
with open('colleges.csv', mode='r', newline='') as file:
    csv_reader = csv.reader(file)
    #store "csv_reader" in a list called "lines"
    colleges_list = list(csv_reader) 


   #for loop printing every line
    
    print("for line loop")
    for line in colleges_list:
        print(line)  # line is a list of strings  
    

    print("for row loop")
    for row in colleges_list:
        print(row)  # row is a list of strings    
    
    print(colleges_list)

"""
#create or overwrites "new_names.csv" file
with open('new_names.csv', mode='w') as new_file:
    csv_writer = csv.writer(new_file, delimiter=',')
"""



 