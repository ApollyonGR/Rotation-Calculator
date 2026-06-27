##
# Lifeguard Rotation Calculator. 
# Feel free to use and modify this code as you see fit. 
# You don't need to credit me, this isn't that impressive of a script.
##

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

RecStands =   ["Rec 1", "Rec 2", "Rove 1", "Rec 3", "Rove 2"]
CompStands =  ["Comp 1", "Comp 2", "Comp 3", "Comp 4"]
SlideStands = ["Top Slide", "Bottom Slide"]
FullRotation = []

#################
### Functions ###
#################
def calcTime():
    timeFormat = "%I:%M %p"

    shiftStartTime = f"{shiftStart.get()} {shiftStartAMPM.get()}" # string
    try:
        parsed_shiftStartTime = datetime.strptime(shiftStartTime, timeFormat) # datetime object
    except ValueError:
        messagebox.showerror("Error", "Execution failed. Please enter a valid Shift start time.")

    shiftEndTime = f"{shiftEnd.get()} {shiftEndAMPM.get()}" # string
    try: 
        parsed_shiftEndTime = datetime.strptime(shiftEndTime, timeFormat) # datetime object
    except ValueError:
        messagebox.showerror("Error", "Execution failed. Please enter a valid Shift end time.")

    shiftTimeDifference = str(parsed_shiftEndTime - parsed_shiftStartTime)
    try:
        h, m, s = map(int, shiftTimeDifference.split(':')) # ignores s because we don't need precision at the per-second level
    except ValueError:
        messagebox.showerror("Error", "Execution failed. Please enter a valid shift time difference.")

    decimal_shiftTimeDifference = h + (m / 60) # Final formatted amount of time spent at work in hours (eg 4.75)

    shiftStartingStand = startingStand.get()
    if shiftStartingStand not in FullRotation:
        messagebox.showerror("Error", "Starting stand not in rotation list, please pick a valid stand.")
    else:
        totalRotations = int(decimal_shiftTimeDifference / 0.25)
        startIndex = FullRotation.index(shiftStartingStand)
        endIndex = ((startIndex + totalRotations) % len(FullRotation)) - 1
        endStand = (FullRotation[endIndex])

    results = ttk.Label(resultsFrame)
    results.grid(row = 0, column = 0, padx = 6, pady = 6)    
    results.config(style="Arial18.TLabel", text=f"""Shift Start: {shiftStart.get()} {shiftStartAMPM.get()}
Shift End: {shiftEnd.get()} {shiftEndAMPM.get()}
Total Shift Length: {decimal_shiftTimeDifference:.2f}
If you go out to {shiftStartingStand} at {shiftStartTime} you'll end on {endStand}""", justify="left")

def validateTime(timeVar):
    
    if timeVar == "":
        return True
    if len(timeVar) > 5:
        return False
    for char in timeVar:
        if not (char.isdigit() or char == ":"):
            return False
    return True

def toggleRec(*args):
    if rec_open.get(): # If Rec Open is checked
        rec_split_checkbox.config(state="normal") # Open the rec split checkbox
        rec_extra_checkbox.config(state="normal")
        slide_checkbox.config(state="normal")
        recBreaksLabel.grid      (row = 1, column = 0, padx = 6, pady = 0) 
        recBreaks.grid           (row = 1, column = 1, padx = 6, pady = 0)
    else:
        rec_split.set(False) # turn the rec split checkbox to off 
        rec_extra.set(False) 
        slide_open.set(False)
        rec_split_checkbox.config(state="disabled") # and disable it
        rec_extra_checkbox.config(state="disabled")
        slide_checkbox.config(state="disabled")
        recBreaksLabel.grid_remove()
        recBreaks.grid_remove()
    rebuildRotation()

def toggleRecSplit(*args):
    if rec_split.get():
        recSplitBreaksLabel.grid (row = 1, column = 2, padx = 6, pady = 0)
        recSplitBreaks.grid      (row = 1, column = 3, padx = 6, pady = 0)
    else:
        recSplitBreaksLabel.grid_remove()
        recSplitBreaks.grid_remove()

def toggleRecExtra(*args):
    rebuildRotation()

def toggleComp(*args):
    if comp_open.get():
        comp_split_checkbox.config(state="normal")
        compBreaksLabel.grid     (row = 2, column = 0, padx = 6, pady = 6)
        compBreaks.grid          (row = 2, column = 1, padx = 6, pady = 6)
    else:
        comp_split.set(False)
        comp_split_checkbox.config(state="disabled")
        compBreaksLabel.grid_remove()
        compBreaks.grid_remove()
    rebuildRotation()

def toggleCompSplit(*args):
    if comp_split.get():
        comp1_checkbox.config(state="normal")
        comp2_checkbox.config(state="normal")
        comp3_checkbox.config(state="normal")
        comp4_checkbox.config(state="normal")
        comp1_checkbox.grid(row = 3, column = 0, padx=6, pady=6, sticky="w")
        comp2_checkbox.grid(row = 3, column = 0, padx=6, pady=6)
        comp3_checkbox.grid(row = 3, column = 1, padx=6, pady=6, sticky="w")
        comp4_checkbox.grid(row = 3, column = 1, padx=6, pady=6)

    else:
        comp1_checkbox.config(state="disabled")
        comp2_checkbox.config(state="disabled")
        comp3_checkbox.config(state="disabled")
        comp4_checkbox.config(state="disabled")
        comp1_checkbox.grid_remove()
        comp2_checkbox.grid_remove()
        comp3_checkbox.grid_remove()
        comp4_checkbox.grid_remove()

def toggleSlide(*args):
    if slide_open.get():
        slideBreaksLabel.grid    (row = 2, column = 2, padx = 6, pady = 6)
        slideBreaks.grid         (row = 2, column = 3, padx = 6, pady = 6)
    else:
        slideBreaksLabel.grid_remove()
        slideBreaks.grid_remove()

def rebuildRotation(*args):
    global FullRotation
    new_rotation = []
    if comp_open.get():
        if comp_split.get():
            if comp_1.get():
                new_rotation.append("Comp 1")
            if comp_2.get():
                new_rotation.append("Comp 2")
            if comp_3.get():
                new_rotation.append("Comp 3")
            if comp_4.get():
                new_rotation.append("Comp 4")
        else:
            new_rotation.extend(CompStands)
        try:
            compBreaksNum = int(compBreaks.get())
            for i in range(1, (compBreaksNum + 1)): # +1 makes sure it gets the last break too
                new_rotation.append(f"Comp Break {i}")
        except ValueError: 
            pass # Avoids crash if there's no breaks (Spinbox is set to 0)

    if rec_open.get():
        for stand in RecStands:
            new_rotation.append(stand)
            if stand == "Rec 2":
                if rec_extra.get():
                    new_rotation.append("Rec Extra")
                    if rec_split.get():
                        try:
                            split_num = int(recSplitBreaks.get())
                            for i in range(1, split_num + 1):
                                new_rotation.append(f"Rec Split Break {i}")
                        except ValueError:
                            pass
                            
                elif rec_split.get():
                    try:
                        split_num = int(recSplitBreaks.get())
                        for i in range(1, split_num + 1):
                            new_rotation.append(f"Rec Split Break {i}")
                    except ValueError:
                        pass

    try:
        rec_num = int(recBreaks.get())
        for i in range(1, rec_num + 1):
            new_rotation.append(f"Rec Break {i}")
    except ValueError:
        pass

    if slide_open.get():
            new_rotation.extend(SlideStands)
            try:
                slideBreaksNum = int(slideBreaks.get())
                for i in range(1, (slideBreaksNum + 1)): 
                    new_rotation.append(f"Slide Break {i}")
            except ValueError: 
                pass 
    
    FullRotation = new_rotation
    startingStand.config(values=FullRotation) # Just refetches the value of FullRotation

######################
### Initialization ###
######################
root = tk.Tk()
root.title("Test")
root.geometry("753x500")
root.resizable(False, False)
container = tk.Frame(root)
container.pack(expand=True, fill="both", padx=24, pady=24) 

##############
### Styles ###
##############
style = ttk.Style()
style.configure("Standard.TFrame", background="white", borderwidth=5, relief="ridge", width=250, height=200)
style.configure("Arial18.TLabel", background="white", font=("Arial", 18))
style.configure("Arial18B.TLabel", background="white", font=("Arial", 18, "bold"))
style.configure("Arial13B.TLabel", background="white", font=("Arial", 13, "bold"))
style.configure("Standard.TCheckbutton", background="white", font=("Arial", 18))
style.configure("Standard.TRadiobutton", background="white")
style.configure("Calc.TButton", font=("Arial", 18), background="lightgreen")

##############
### Frames ###
##############
whenStartFrame = ttk.Frame  (container, style="Standard.TFrame", padding=(6, 6), width=340, height=120)
breaksFrame = ttk.Frame     (container, style="Standard.TFrame", padding=(6, 6), width=340, height=120)
checkboxesFrame = ttk.Frame (container, style="Standard.TFrame", padding=(6, 6), width=340, height=120)
whereStartFrame = ttk.Frame (container, style="Standard.TFrame", padding=(6, 6), width=340, height=120)

calculateFrame = ttk.Button (container, style="Calc.TButton", text="Calculate", command=calcTime)
resultsFrame = ttk.Frame    (container, style="Standard.TFrame")

##################
### Frame Grid ###
##################
whenStartFrame.grid  (row = 0, column = 0, padx = 6, pady = 6)
breaksFrame.grid     (row = 0, column = 1, padx = 6, pady = 6)
checkboxesFrame.grid (row = 1, column = 0, padx = 6, pady = 6)
whereStartFrame.grid (row = 1, column = 1, padx = 6, pady = 6)

whenStartFrame.grid_propagate(0)
breaksFrame.grid_propagate(0)
checkboxesFrame.grid_propagate(0)
whereStartFrame.grid_propagate(0)

whenStartFrame.grid_columnconfigure([0,1,2,3], weight=1)
whenStartFrame.grid_rowconfigure([0,1], weight=1)
breaksFrame.grid_columnconfigure([0,1,2,3], weight=1)
breaksFrame.grid_rowconfigure([0,1,2], weight=1)
checkboxesFrame.grid_columnconfigure([0,1,2,3], weight=1)
checkboxesFrame.grid_rowconfigure([0,1,2], weight=1)
whereStartFrame.grid_columnconfigure([0], weight=1)
whereStartFrame.grid_rowconfigure([0,1], weight=1)

calculateFrame.grid  (row = 2, column = 0, padx = 6, pady = 6, columnspan=2)
resultsFrame.grid    (row = 3, column = 0, padx = 6, pady = 6, columnspan=2)

############################
### Variables and Traces ###
############################
rotationTime = tk.IntVar(value=15)
shiftStart = tk.StringVar()
shiftEnd = tk.StringVar()
shiftLength = tk.DoubleVar() # in hours

compBreakCount = tk.StringVar(value="2")
recBreakCount = tk.StringVar(value="2")
recSplitBreakCount = tk.StringVar(value="2")
slideBreakCount = tk.StringVar(value="1") # What I feel is the average break distrobution on a regulqar, kinda shortstaffed day.

rec_open = tk.BooleanVar(value=True)
rec_split = tk.BooleanVar(value=True)
rec_extra = tk.BooleanVar(value=False)
comp_open = tk.BooleanVar(value=True)
comp_split = tk.BooleanVar(value=False)
slide_open = tk.BooleanVar(value=True)
comp_1 = tk.BooleanVar(value=False)
comp_2 = tk.BooleanVar(value=False)
comp_3 = tk.BooleanVar(value=False)
comp_4 = tk.BooleanVar(value=False)

rec_open.trace_add("write", toggleRec)
rec_split.trace_add("write", toggleRecSplit)
rec_extra.trace_add("write", toggleRecExtra)
comp_open.trace_add("write", toggleComp)
comp_split.trace_add("write", toggleCompSplit)
slide_open.trace_add("write", toggleSlide)

vmcd = root.register(validateTime) # Sets up command for implementing max characters on Shift start/end entry boxes

########################
### Shift Time Entry ###
########################
shiftStart = ttk.Entry      (whenStartFrame,
                        textvariable = shiftStart,
                        font = ("Arial", 18),
                        width=5,
                        validate="key",
                        validatecommand=(vmcd, "%P"))
shiftEnd = ttk.Entry        (whenStartFrame,
                        textvariable = shiftEnd,
                        font = ("Arial", 18),
                        width=5,
                        validate="key",
                        validatecommand=(vmcd, "%P"))
shiftStartLabel = ttk.Label (whenStartFrame,
                        text = "Shift start: ",
                        style="Arial18B.TLabel")
shiftEndLabel = ttk.Label   (whenStartFrame,
                        text = "Shift end: ",
                        style="Arial18B.TLabel")

shiftStartAMPM = tk.StringVar(value="AM")
shiftEndAMPM =   tk.StringVar(value="PM")

# AM/PM radio buttons
rb1am = ttk.Radiobutton(
    whenStartFrame,
    text = "AM",
    variable = shiftStartAMPM,
    value = "AM",
    style="Standard.TRadiobutton")
rb1pm = ttk.Radiobutton(
    whenStartFrame,
    text = "PM",
    variable = shiftStartAMPM,
    value = "PM",
    style="Standard.TRadiobutton")
rb2am = ttk.Radiobutton(
    whenStartFrame,
    text = "AM",
    variable = shiftEndAMPM,
    value = "AM",
    style="Standard.TRadiobutton")
rb2pm = ttk.Radiobutton(
    whenStartFrame,
    text = "PM",
    variable = shiftEndAMPM,
    value = "PM",
    style="Standard.TRadiobutton")

# Shift grid
shiftStart.grid(        row = 0, column = 1, padx = 6, pady = 0)
shiftEnd.grid(          row = 1, column = 1, padx = 6, pady = 0)
shiftStartLabel.grid(   row = 0, column = 0, padx = 6, pady = 0)
shiftEndLabel.grid(     row = 1, column = 0, padx = 6, pady = 0)
rb1am.grid(             row = 0, column = 2, padx = 6, pady = 0)
rb1pm.grid(             row = 0, column = 3, padx = 6, pady = 0)
rb2am.grid(             row = 1, column = 2, padx = 6, pady = 0)
rb2pm.grid(             row = 1, column = 3, padx = 6, pady = 0)

########################
### Stand Checkboxes ###
########################
rec_checkbox = ttk.Checkbutton        (checkboxesFrame,
                         text="Rec open? ",
                         style="Standard.TCheckbutton",
                         variable=rec_open)
rec_split_checkbox = ttk.Checkbutton  (checkboxesFrame,
                         text="Rec split? ",
                         style="Standard.TCheckbutton",
                         variable=rec_split)
rec_extra_checkbox = ttk.Checkbutton  (checkboxesFrame,
                         text="Rec extra? ",
                         style="Standard.TCheckbutton",
                         variable=rec_extra)
comp_checkbox = ttk.Checkbutton       (checkboxesFrame,
                         text="Comp open?",
                         style="Standard.TCheckbutton",
                         variable=comp_open)
comp_split_checkbox = ttk.Checkbutton (checkboxesFrame,
                         text="Comp split?",
                         style="Standard.TCheckbutton",
                         variable=comp_split)
slide_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="Slide open?",
                         style="Standard.TCheckbutton",
                         variable=slide_open)
comp1_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="1  ",
                         style="Standard.TCheckbutton",
                         variable=comp_1)
comp2_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="2  ",
                         style="Standard.TCheckbutton",
                         variable=comp_2)
comp3_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="3  ",
                         style="Standard.TCheckbutton",
                         variable=comp_3)
comp4_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="4  ",
                         style="Standard.TCheckbutton",
                         variable=comp_4)

# Checkboxes packing
rec_checkbox.grid        (row = 0, column = 0, padx=3, pady=2, sticky="w")
rec_split_checkbox.grid  (row = 1, column = 0, padx=3, pady=2, sticky="w")
rec_extra_checkbox.grid  (row = 2, column = 0, padx=3, pady=2, sticky="w")
comp_checkbox.grid       (row = 0, column = 1, padx=3, pady=2, sticky="w")
comp_split_checkbox.grid (row = 1, column = 1, padx=3, pady=2, sticky="w") 
slide_checkbox.grid      (row = 2, column = 1, padx=3, pady=2, sticky="w")

########################
### "Breaks after X" ###
########################
breaksFrameLabel = ttk.Label(breaksFrame, 
                            text="  How many breaks after X?", 
                            style="Arial18.TLabel",
                            padding=(6, 3))
recBreaksLabel = ttk.Label(breaksFrame, 
                          text="Rec",
                          style="Arial13B.TLabel")
recSplitBreaksLabel = ttk.Label(breaksFrame, 
                          text="Split",
                          style="Arial13B.TLabel")
compBreaksLabel = ttk.Label(breaksFrame, 
                          text="Comp",
                          style="Arial13B.TLabel")
slideBreaksLabel = ttk.Label(breaksFrame, 
                          text="Slide",
                          style="Arial13B.TLabel")

breaksFrameLabel.grid        (row = 0, column = 0, padx = 3, pady = 1, columnspan=4, sticky="nesw")
recBreaks = ttk.Spinbox      (breaksFrame, from_=0, to=4, width=5, font=("Arial", 13), textvariable=recBreakCount)
recSplitBreaks = ttk.Spinbox (breaksFrame, from_=0, to=4, width=5, font=("Arial", 13), textvariable=recSplitBreakCount)
compBreaks = ttk.Spinbox     (breaksFrame, from_=0, to=4, width=5, font=("Arial", 13), textvariable=compBreakCount)
slideBreaks = ttk.Spinbox    (breaksFrame, from_=0, to=4, width=5, font=("Arial", 13), textvariable=slideBreakCount)

#########################
### Starting location ###
#########################
startingStandLabel = ttk.Label(whereStartFrame,
                              text = "Which stand are you\n" \
                              "       starting on?",
                              style="Arial18.TLabel")
startingStand = ttk.Combobox(whereStartFrame, values=FullRotation, postcommand=rebuildRotation, font=("Arial", 13))
startingStandLabel.grid(row=0, column=0, padx = 6, pady = 6)
startingStand.grid(row=1, column=0, padx = 6, pady = 6)

#######################
### Viewing Results ###
#######################


###################
### Run Program ###
###################

toggleRec()
toggleRecSplit()
toggleRecExtra()
toggleComp()
toggleCompSplit()
toggleSlide()

root.bind("<Configure>", onresize)
root.mainloop()
