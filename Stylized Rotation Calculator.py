##
# marc rotation calc
##

## TO DO: 
##
## 1) Add math
## 3) add dropdown menu for comp stands if comp split is checked

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

RecStands =   ["Rec 1", "Rec 2", "Rove 1", "Rec 3", "Rove 2"]
CompStands =  ["Comp 1", "Comp 2", "Comp 3", "Comp 4"]
SlideStands = ["Top Slide", "Bottom Slide"]
FullRotation = []

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
    h, m, s = map(int, shiftTimeDifference.split(':')) # ignores s because we don't need precision at the per-second level
    decimal_shiftTimeDifference = h + (m / 60) # Final formatted amount of time spent at work in hours (eg 4.75)

    shiftStartingStand = startingStand.get()
    if shiftStartingStand not in FullRotation:
        messagebox.showerror("Error", "Starting stand not in rotation list, please pick a valid stand.")
    else:
        totalRotations = int(decimal_shiftTimeDifference / 0.25)
        startIndex = FullRotation.index(shiftStartingStand)
        endIndex = ((startIndex + totalRotations) % len(FullRotation)) - 1
        endStand = (FullRotation[endIndex])
        
    results.config(text=f"""Shift Start: {shiftStart.get()} {shiftStartAMPM.get()}
Shift End: {shiftEnd.get()} {shiftEndAMPM.get()}
Total Shift Length: {decimal_shiftTimeDifference:.2f}
If you go out to {shiftStartingStand} at {shiftStartTime} you'll end on {endStand}""")

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
        recBreaksLabel.grid      (row = 1, column = 0, padx = 6, pady = 6, sticky="e")
        recBreaks.grid           (row = 1, column = 1, padx = 6, pady = 6, sticky="e")
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
        recSplitBreaksLabel.grid (row = 2, column = 0, padx = 6, pady = 6, sticky="e")
        recSplitBreaks.grid      (row = 2, column = 1, padx = 6, pady = 6, sticky="e")
    else:
        recSplitBreaksLabel.grid_remove()
        recSplitBreaks.grid_remove()

def toggleRecExtra(*args):
    rebuildRotation()

def toggleComp(*args):
    if comp_open.get():
        comp_split_checkbox.config(state="normal")
        compBreaksLabel.grid     (row = 1, column = 2, padx = 6, pady = 6, sticky="w")
        compBreaks.grid          (row = 1, column = 3, padx = 6, pady = 6, sticky="w")
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
        comp1_checkbox.grid(row = 1, column = 2, padx=18, pady=6, sticky="w")
        comp2_checkbox.grid(row = 1, column = 2, padx=18, pady=6, sticky="e")
        comp3_checkbox.grid(row = 2, column = 2, padx=18, pady=6, sticky="w")
        comp4_checkbox.grid(row = 2, column = 2, padx=18, pady=6, sticky="e")

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
        slideBreaksLabel.grid    (row = 2, column = 2, padx = 6, pady = 6, sticky="w")
        slideBreaks.grid         (row = 2, column = 3, padx = 6, pady = 6, sticky="w")
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
root.geometry("480x320")

container = ttk.Frame(root)
container.pack(expand=True) 

# Setup Style configurations
style = ttk.Style()
style.configure("Custom.TFrame", background="white", borderwidth=2, relief="groove")
style.configure("Custom.TLabel", background="white", font=("Arial", 18))
style.configure("Bold.TLabel", background="white", font=("Arial", 18, "bold"))
style.configure("SubBold.TLabel", background="white", font=("Arial", 15, "bold"))
style.configure("Custom.TCheckbutton", background="white", font=("Arial", 18))
style.configure("Custom.TRadiobutton", background="white")
style.configure("Calc.TButton", font=("Arial", 18), background="lightgreen")

# Frames
checkboxesFrame = ttk.Frame (container, style="Custom.TFrame")
whenStartFrame = ttk.Frame  (container, style="Custom.TFrame")
whereStartFrame = ttk.Frame (container, style="Custom.TFrame")
breaksFrame = ttk.Frame     (container, style="Custom.TFrame")
calculateFrame = ttk.Button (container,
                    style="Calc.TButton",
                    text="Calculate",
                    command=calcTime)
resultsFrame = ttk.Frame (container, style="Custom.TFrame")

# Frame grid
whenStartFrame.grid  (row = 0, column = 0, padx = 6, pady = 6)
checkboxesFrame.grid (row = 1, column = 0, padx = 6, pady = 6)
breaksFrame.grid     (row = 2, column = 0, padx = 6, pady = 6)
whereStartFrame.grid (row = 3, column = 0, padx = 6, pady = 6)
calculateFrame.grid  (row = 4, column = 0, padx = 6, pady = 6)
resultsFrame.grid    (row = 1, column = 1, padx = 6, pady = 6, rowspan=2)

rotationTime = tk.IntVar(value=15)
shiftStart = tk.StringVar()
shiftEnd = tk.StringVar()
shiftLength = tk.DoubleVar() # in hours

compBreakCount = tk.StringVar(value="0")
recBreakCount = tk.StringVar(value="0")
recSplitBreakCount = tk.StringVar(value="0")
slideBreakCount = tk.StringVar(value="0")

vmcd = root.register(validateTime) # Sets up command for implementing max characters on Shift start/end entry boxes

rec_open = tk.BooleanVar(value=True)
rec_split = tk.BooleanVar(value=False)
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

########################
### Shift Time Entry ###
########################

# Shift time entry boxes
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
                        style="Bold.TLabel")
shiftEndLabel = ttk.Label   (whenStartFrame,
                        text = "Shift end: ",
                        style="Bold.TLabel")

shiftStartAMPM = tk.StringVar(value="AM")
shiftEndAMPM =   tk.StringVar(value="PM")

# AM/PM radio buttons
rb1am = ttk.Radiobutton(
    whenStartFrame,
    text = "AM",
    variable = shiftStartAMPM,
    value = "AM",
    style="Custom.TRadiobutton")
rb1pm = ttk.Radiobutton(
    whenStartFrame,
    text = "PM",
    variable = shiftStartAMPM,
    value = "PM",
    style="Custom.TRadiobutton")
rb2am = ttk.Radiobutton(
    whenStartFrame,
    text = "AM",
    variable = shiftEndAMPM,
    value = "AM",
    style="Custom.TRadiobutton")
rb2pm = ttk.Radiobutton(
    whenStartFrame,
    text = "PM",
    variable = shiftEndAMPM,
    value = "PM",
    style="Custom.TRadiobutton")

# Shift grid
shiftStart.grid(        row = 0, column = 1, padx = 6, pady = 6)
shiftEnd.grid(          row = 1, column = 1, padx = 6, pady = 6)
shiftStartLabel.grid(   row = 0, column = 0, padx = 6, pady = 6)
shiftEndLabel.grid(     row = 1, column = 0, padx = 6, pady = 6)
rb1am.grid(             row = 0, column = 2, padx = 6, pady = 6)
rb1pm.grid(             row = 0, column = 3, padx = 6, pady = 6)
rb2am.grid(             row = 1, column = 2, padx = 6, pady = 6)
rb2pm.grid(             row = 1, column = 3, padx = 6, pady = 6)

########################
### Stand Checkboxes ###
########################

rec_checkbox = ttk.Checkbutton        (checkboxesFrame,
                         text="Rec open?",
                         style="Custom.TCheckbutton",
                         variable=rec_open)
rec_split_checkbox = ttk.Checkbutton  (checkboxesFrame,
                         text="Rec split?  ",
                         style="Custom.TCheckbutton",
                         variable=rec_split)
rec_extra_checkbox = ttk.Checkbutton  (checkboxesFrame,
                         text="Rec extra?",
                         style="Custom.TCheckbutton",
                         variable=rec_extra)
comp_checkbox = ttk.Checkbutton       (checkboxesFrame,
                         text="Comp open?",
                         style="Custom.TCheckbutton",
                         variable=comp_open)
comp_split_checkbox = ttk.Checkbutton (checkboxesFrame,
                         text="Comp split?  ",
                         style="Custom.TCheckbutton",
                         variable=comp_split)
slide_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="Slide open?",
                         style="Custom.TCheckbutton",
                         variable=slide_open)
comp1_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="1  ",
                         style="Custom.TCheckbutton",
                         variable=comp_1)
comp2_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="2  ",
                         style="Custom.TCheckbutton",
                         variable=comp_2)
comp3_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="3  ",
                         style="Custom.TCheckbutton",
                         variable=comp_3)
comp4_checkbox = ttk.Checkbutton      (checkboxesFrame,
                         text="4  ",
                         style="Custom.TCheckbutton",
                         variable=comp_4)

# Checkboxes packing
rec_checkbox.grid        (row = 0, column = 0, padx=6, pady=6, sticky="w")
rec_split_checkbox.grid  (row = 1, column = 0, padx=6, pady=6, sticky="w")
rec_extra_checkbox.grid  (row = 2, column = 0, padx=6, pady=6, sticky="w")
comp_checkbox.grid       (row = 0, column = 1, padx=6, pady=6, sticky="w")
comp_split_checkbox.grid (row = 1, column = 1, padx=6, pady=6, sticky="w") 
slide_checkbox.grid      (row = 0, column = 2, padx=6, pady=6, sticky="w")

########################
### "Breaks after X" ###
########################

breaksFrameLabel = ttk.Label(breaksFrame, 
                            text="How many breaks after X?", 
                            style="Custom.TLabel", 
                            padding=(6, 6))
recBreaksLabel = ttk.Label(breaksFrame, 
                          text="Rec",
                          style="SubBold.TLabel")
recSplitBreaksLabel = ttk.Label(breaksFrame, 
                          text="Split",
                          style="SubBold.TLabel")
compBreaksLabel = ttk.Label(breaksFrame, 
                          text="Comp",
                          style="SubBold.TLabel")
slideBreaksLabel = ttk.Label(breaksFrame, 
                          text="Slide",
                          style="SubBold.TLabel")

breaksFrameLabel.grid        (row = 0, column = 0, padx = 6, pady = 6, columnspan=4, sticky="nesw")
recBreaks = ttk.Spinbox      (breaksFrame, from_=0, to=4, width=5, font=("Arial", 12), textvariable=recBreakCount)
recSplitBreaks = ttk.Spinbox (breaksFrame, from_=0, to=4, width=5, font=("Arial", 12), textvariable=recSplitBreakCount)
compBreaks = ttk.Spinbox     (breaksFrame, from_=0, to=4, width=5, font=("Arial", 12), textvariable=compBreakCount)
slideBreaks = ttk.Spinbox    (breaksFrame, from_=0, to=4, width=5, font=("Arial", 12), textvariable=slideBreakCount)

#########################
### Starting location ###
#########################

startingStandLabel = ttk.Label(whereStartFrame,
                              text = "Where do you start?",
                              style="Custom.TLabel")
startingStand = ttk.Combobox(whereStartFrame, values=FullRotation, postcommand=rebuildRotation)
startingStandLabel.pack(padx = 6, pady = 6)
startingStand.pack(padx = 6, pady = 12)

#######################
### Viewing Results ###
#######################

results = ttk.Label(resultsFrame, 
                   text=f""" """,
                   style="Custom.TLabel",
                   justify="left")
results.grid(row = 0, column = 0, padx = 6, pady = 6)

###################
### Run Program ###
###################

toggleRec()
toggleRecSplit()
toggleRecExtra()
toggleComp()
toggleCompSplit()
toggleSlide()

root.mainloop()