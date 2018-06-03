"""

Financial Independence GUI

Parses files output by the Financial Independence Console Application, displays
a maximum, minimum and average value for each simulations result set.

Version: 1.0
Author: Wade Casey
Date: 02/06/2018

"""


from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os

maximums = []
minimums = []
averages = []



# =========================================================================== #
#                                 Functions                                   #
# =========================================================================== #

def OpenFileDialog():
    """Extract data from selected file.

    Raises:
        IOError: if unable to locate or open file.
        ValueError: if file cannot be processed, invalid file.
        ZeroDivisionError: if invalid file is partly processed.

    """
    # 'filename' gets the directory of the file selected using filedialog
    filename = filedialog.askopenfilename(
        filetypes = (("Text Documents", "*.txt"), ("All Files", "*.*"))
        )
    try:
        # Open the selected file in 'readonly' mode.
        with open(filename, 'r') as f:
            # Check if file is empty, if true, notify the user, reset widgets,
            # clear lists, disable the combobox, and return.
            if os.stat(filename).st_size == 0:
                txt_message.set("Empty file...")
                txt_maximum.set("")
                txt_minimum.set("")
                txt_average.set("")   
                cbo_results.set("")
                cbo_results['state'] = 'disabled' 
                maximums.clear()  
                minimums.clear()  
                averages.clear()  
                return
            # Declare new list to hold values parsed from opened file.
            values = []
            # For each line in the file, split by spaces and append each value
            # to a list inside 'values'.
            for line in f:
                values.append(line.split(' '))
            # The string 'successful' or 'unsuccessful' is the last value of
            # each line, pop() it from the end of each list in 'values'.
            for i in range(len(values)):
                values[i].pop()
            # For each list in 'values' list.
            for i in range(len(values)):
                # Initial values for maximum, minimum and average variables.
                maximum = 'start'
                minimum = 'start'
                average = 0
                # Iterate over each element in each list in 'values',
                # get maximum, minimum and average values of each simulation.
                for value in values[i]:
                    try:
                        tmp_maximum = float(value)
                        tmp_minimum = float(value)
                        # If starting a new iteration, 'maximum' gets first
                        # value of the list.
                        if maximum == 'start':
                            maximum = tmp_maximum
                        # else, check if 'tmp_maximum' is > 'maximum', if true,
                        # 'maximum' gets tmp_maximum.
                        elif tmp_maximum > maximum:
                            maximum = tmp_maximum
                        # If starting a new iteration, 'minimum' gets first
                        # value of the list.
                        if minimum == 'start':
                            minimum = tmp_minimum
                        # else, check if 'tmp_minimum' is < 'minimum', if true,
                        # 'minimum' gets tmp_minimum.                        
                        elif tmp_minimum < minimum:
                            minimum = tmp_minimum
                        # 'average' gets the sum of all values in the list
                        # being iterated. It is later divided by the number of
                        # list elements to get the 'average' value.
                        average += float(value)
                    # An incorrectly formatted file will throw a ValueError.
                    # Notify the user, reset widgets, clear lists, disable the
                    # combobox, and return.
                    except ValueError:
                        txt_message.set("Invalid file...")
                        txt_maximum.set("")
                        txt_minimum.set("")
                        txt_average.set("")  
                        cbo_results.set("")
                        cbo_results['state'] = 'disabled' 
                        values.clear()
                        maximums.clear()  
                        minimums.clear()  
                        averages.clear()  
                        return                        
                # Append parsed values to their corresponding lists before
                # iterating over the next list in 'values'.
                try:
                    maximums.append(maximum)
                    minimums.append(minimum)
                    averages.append(average/(len(values[i])))
                    txt_message.set("")
                # An incorrectly formatted file will throw a ZeroDivisionError.
                # Notify the user, reset widgets, clear lists, disable the
                # combobox, and return.
                except ZeroDivisionError:
                    txt_message.set("Invalid file...")
                    txt_maximum.set("")
                    txt_minimum.set("")
                    txt_average.set("")   
                    cbo_results.set("")
                    cbo_results['state'] = 'disabled' 
                    values.clear() 
                    maximums.clear()  
                    minimums.clear()  
                    averages.clear()  
                    return
            # Create a menu list for the combobox.
            # For each list in 'values', append a string to 'combobox_menu',
            # set the combobox configuration to use this list as its displayed
            # value, set the combobox state to readonly and display the first
            # element in 'combobox_menu', then, bind an event to be called
            # whenever the user makes a selection in the combobox.
            combobox_menu = []                 
            for i in range(len(values)):
                if (i+1) < 10:
                    combobox_menu.append("Simulation #00" + str(i+1))
                elif (i+1) >= 10 and i < 100:  
                    combobox_menu.append("Simulation #0" + str(i+1))
                else:
                    combobox_menu.append("Simulation #" + str(i+1))                
            cbo_results['values'] = combobox_menu
            cbo_results['state'] = 'readonly' 
            cbo_results.current(0)
            cbo_results.bind('<<ComboboxSelected>>', ComboboxSelectionChanged)
            # Display first element of 'maximums', 'minimums' and 'averages'.
            txt_maximum.set("Maximum balance: {0}".format(
                format(float(maximums[0]), '.2f')
                ))
            txt_minimum.set("Minimum balance: {0}".format(
                format(float(minimums[0]), '.2f')
                ))
            txt_average.set("Average balance: {0}".format(
                format(float(averages[0]), '.2f')
                ))
    except IOError:
        # Prevent error when user closes filedialog without selecting a file.
        if filename == "":
            pass
        # Unable to access the selected file.
        else:
            messagebox.showinfo(message="{0}\n\n{1}\n\n{2}".format(
                "Unable to open file at:", 
                filename, 
                "Check you have permission to access this directory.")
                )


def ComboboxSelectionChanged(event):
    # Set labels text to display the value stored in the maximums, minimums and
    # averages lists at the index corresponding combobox selection.
    txt_maximum.set("Maximum balance: {0}".format(
        format(maximums[cbo_results.current()], '.2f')
        ))
    txt_minimum.set("Minimum balance: {0}".format(
        format(minimums[cbo_results.current()], '.2f')
        ))
    txt_average.set("Average balance: {0}".format(
        format(averages[cbo_results.current()], '.2f')
        ))



# =========================================================================== #
#                             Window and Widgets                              #
# =========================================================================== #

# Root window and title.
root = Tk()
root.title('Financial Independence GUI')

# Tkinter Variables
txt_maximum = StringVar()
txt_minimum = StringVar()
txt_average = StringVar()
txt_message = StringVar()

# Create 'content' frame to contain all widgets, child of 'root'.
content = ttk.Frame(root,padding=(10,10,10,30),borderwidth=1,relief='raised')
# Create various widgets, children of 'content' frame.
btn_open = ttk.Button(content, text="Open...", command=OpenFileDialog)
lbl_spacer1 = ttk.Label(content)
lbl_select = ttk.Label(content, text="Select:")
cbo_results = ttk.Combobox(content, state='readonly')
lbl_spacer2 = ttk.Label(content)
lbl_maximum = ttk.Label(content, textvariable=txt_maximum)
lbl_minimum = ttk.Label(content, textvariable=txt_minimum)
lbl_average = ttk.Label(content, textvariable=txt_average)
lbl_message = ttk.Label(content, textvariable=txt_message)
# Draw 'content' frame with grid and stick to N, S, E &  W of the 'root'.
content.grid(sticky=(N,S,E,W))
# Draw widgets to specified column/rows, apply padding and sticky attributes,
# combobox widget get a default set() and state.
btn_open.grid(column=1, row=1, sticky=(N,W))
lbl_spacer1.grid(column=2, row=1, padx=125)
lbl_select.grid(column=3, row=1, sticky=(N,E), pady=2, padx=6)
cbo_results.grid(column=4, row=1, sticky=(N,E), pady=2)
cbo_results.set("")
cbo_results['state'] = 'disabled'
lbl_spacer2.grid(column=1, row=2, columnspan=4, pady=3)
lbl_maximum.grid(column=1, row=3, columnspan=4)
lbl_minimum.grid(column=1, row=4, columnspan=4, pady=25)
lbl_average.grid(column=1, row=5, columnspan=4)
lbl_message.grid(column=1, row=2, sticky=N)
# Configure column/row growth weights to give the application a responsive 
# feel when window is being resized. 
content.columnconfigure(1, weight=1)
content.columnconfigure(2, weight=1)
content.columnconfigure(3, weight=1920)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)
content.rowconfigure(2, weight=100)
content.rowconfigure(3, weight=20)
content.rowconfigure(4, weight=20)
content.rowconfigure(5, weight=20)
content.rowconfigure(6, weight=400)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# Get the windows width/height after widgets are drawn.
root.update()
# Set the windows minimum width/height to the windows size after widgets have
# been initialized and drawn.
root.minsize(root.winfo_width(), root.winfo_height())
# Start tkinter mainloop.
root.mainloop()