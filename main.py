import os
import time
from datetime import datetime
import tkinter as tk
from tkinter import *
from math import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import func
import tksheet
import win32gui
import pyautogui
from PIL import ImageTk, Image
from io import BytesIO
import win32clipboard

t = 0.1  # start time
step = 0.1  # step size
bp = 0
graphlist = []  # array for graphing
colours = ['blue', 'green', 'red', 'magenta', 'yellow', 'black', 'cyan']  # list of colours for graph

def check_entries(*args):
    if r_entry.get() and H_entry.get() and a_entry.get() and C_entry.get() and RTI_entry.get() and Tact_entry.get() and Ti_entry.get():
        calc_button.configure(state=ACTIVE)
    else:
        calc_button.configure(state=DISABLED)


def send_to_clipboard(image):
    output = BytesIO()
    image.convert('RGB').save(output, 'BMP')
    data = output.getvalue()[14:]
    output.close()

    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()


def alphanototext(num):
    alphalist = ['Slow', 'Medium', 'Fast', 'Ultra fast']
    if num == round(1055 / (600 ** 2), 4):
        return alphalist[0]
    elif num == round(1055 / (300 ** 2), 4):
        return alphalist[1]
    elif num == round(1055 / (150 ** 2), 4):
        return alphalist[2]
    elif num == round(1055 / (75 ** 2), 4):
        return alphalist[3]
    else:
        return num


def optionselect(event):
    r_entry.config(state="normal")
    r_entry.delete(0, END)

    H_entry.config(state="normal")
    H_entry.delete(0, END)

    a_entry.config(state="normal")
    a_entry.delete(0, END)

    C_entry.config(state="normal")
    C_entry.delete(0, END)

    RTI_entry.config(state="normal")
    RTI_entry.delete(0, END)

    Tact_entry.config(state="normal")
    Tact_entry.delete(0, END)

    Ti_entry.config(state="normal")
    Ti_entry.delete(0, END)

    if dropdown.get() == "Test":
        r_text.set(2.5)
        r_entry.config(state="disabled")

        H_text.set(2.5)
        H_entry.config(state="disabled")

        a_text.set(round(1000 / (150 * 150), 3))
        a_entry.config(state="disabled")

        C_text.set(0.8)
        C_entry.config(state="disabled")

        RTI_text.set(50)
        RTI_entry.config(state="disabled")

        Tact_text.set(68)
        Tact_entry.config(state="disabled")

        Ti_text.set(20)
        Ti_entry.config(state="disabled")

    elif dropdown.get() == "Test 2":
        r_text.set(4)
        r_entry.config(state="disabled")

        H_text.set(2.5)
        H_entry.config(state="disabled")

        a_text.set(round(1000 / (150 * 150), 3))
        a_entry.config(state="disabled")

        C_text.set(0.8)
        C_entry.config(state="disabled")

        RTI_text.set(50)
        RTI_entry.config(state="disabled")

        Tact_text.set(75)
        Tact_entry.config(state="disabled")

        Ti_text.set(20)
        Ti_entry.config(state="disabled")


def alphaselect(event):
    a_entry.config(state="normal")
    a_entry.delete(0, END)

    if dropdown2.get() == "Slow":
        a_text.set(round(1055 / (600 ** 2), 4))
        a_entry.config(state="disabled")

    elif dropdown2.get() == "Medium":
        a_text.set(round(1055 / (300 ** 2), 4))
        a_entry.config(state="disabled")

    elif dropdown2.get() == "Fast":
        a_text.set(round(1055 / (150 ** 2), 4))
        a_entry.config(state="disabled")

    elif dropdown2.get() == "Ultra fast":
        a_text.set(round(1055 / (75 ** 2), 4))
        a_entry.config(state="disabled")


def loop(r, H, a, C, RTI, T_act, T_i, T_a, t, Te, step):
    Q = a * t ** 2
    Tg = func.deltaTmax(r, H, Q)
    u = func.Umax(r, H, Q)

    dTe = ((sqrt(u) / RTI) * (Tg - (1 + (C / (sqrt(u)))) * (T_i - T_a))) * step
    Te = Te + dTe
    arr1 = np.array([Q, Tg, u, dTe, Te, t])
    t = t + step

    while Te < T_act:
        Q = a * t ** 2
        Tg = func.deltaTmax(r, H, Q)
        u = func.Umax(r, H, Q)

        dTe = ((sqrt(u) / RTI) * (Tg - (1 + (C / (sqrt(u)))) * (Te - T_a))) * step
        Te = Te + dTe
        arrTemp = np.array([(Q/1000), Tg, u, dTe, Te, t])
        arr1 = np.vstack((arr1, arrTemp))
        t = t + step

    return t, Q, arr1


# create tk
root = tk.Tk()
root.title("Thermal detector calculator")
frames = []
for i in range(5):
    for j in range(5):
        Frame = tk.Frame(root, borderwidth=1)
        Frame.grid(row=i, column=j)

        frames.append(Frame)

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Quit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)

# Create title
frames[0].configure(relief=tk.RAISED, borderwidth=5, bg='SystemButtonFace')
frames[0].grid(row=0, column=0, columnspan=2, sticky=EW)
title_label = tk.Label(master=frames[0], text="Thermal detector\ncalculator", font="none 16 bold")
title_label.pack(fill=tk.BOTH, expand=1)

# Create labels for inputs
frames[5].configure(relief=tk.RAISED, borderwidth=5, bg='SystemButtonFace')
frames[5].grid(row=1, column=0, sticky=EW)
r_label = tk.Label(frames[5], text="Enter r:")
r_label.pack()

H_label = tk.Label(frames[5], text="Enter H:")
H_label.pack()

# create alpha list
ALPHA = ["Custom", "Slow", "Medium", "Fast", "Ultra fast"]
dropdown2 = StringVar(root)
dropdown2.set("Enter alpha:")
dd2 = OptionMenu(frames[5], dropdown2, *ALPHA, command=alphaselect)
dd2.config(width=9)
dd2.pack()

C_label = tk.Label(frames[5], text="Enter C:")
C_label.pack()

RTI_label = tk.Label(frames[5], text="Enter RTI:")
RTI_label.pack()

Tact_label = tk.Label(frames[5], text="Enter Tact:")
Tact_label.pack()

Ti_label = tk.Label(frames[5], text="Enter Tinf:")
Ti_label.pack()

# create entry boxes
r_text = tk.StringVar(root)
r_entry = tk.Entry(frames[6], textvariable=r_text)
r_entry.pack(pady=1)
r_text.trace_variable("w", check_entries)

H_text = tk.StringVar(root)
H_entry = tk.Entry(frames[6], textvariable=H_text)
H_entry.pack(pady=1)
H_text.trace_variable("w", check_entries)

a_text = tk.StringVar(root)
a_entry = tk.Entry(frames[6], textvariable=a_text)
a_entry.pack(pady=6)
a_text.trace_variable("w", check_entries)

C_text = tk.StringVar(root)
C_entry = tk.Entry(frames[6], textvariable=C_text)
C_entry.pack(pady=1)
C_text.trace_variable("w", check_entries)

RTI_text = tk.StringVar(root)
RTI_entry = tk.Entry(frames[6], textvariable=RTI_text)
RTI_entry.pack(pady=1)
RTI_text.trace_variable("w", check_entries)

Tact_text = tk.StringVar(root)
Tact_entry = tk.Entry(frames[6], textvariable=Tact_text)
Tact_entry.pack(pady=1)
Tact_text.trace_variable("w", check_entries)

Ti_text = tk.StringVar(root)
Ti_entry = tk.Entry(frames[6], textvariable=Ti_text)
Ti_entry.pack(pady=1)
Ti_text.trace_variable("w", check_entries)

# create options list
OPTIONS = ["Custom", "Test", "Test 2"]
dropdown = StringVar(root)
dropdown.set("Presets")
dd = OptionMenu(frames[0], dropdown, *OPTIONS, command=optionselect)
dd.configure(relief=tk.RAISED, borderwidth=3)
dd.pack()

# create result labels
time_label = tk.Label(frames[2])
frames[2].configure(bg='SystemButtonFace')
time_label.pack()

frames[10].configure(relief=tk.RAISED, borderwidth=5, bg='SystemButtonFace')
frames[10].grid(row=2, column=0, columnspan=2, sticky=EW + N)
# create calculate button
calc_button = tk.Button(frames[10], text="Calculate", state=DISABLED)
calc_button.pack(fill=tk.BOTH, expand=1)


# create clear button
clr_button = tk.Button(frames[10], text='Clear')
clr_button.pack(fill=tk.BOTH, expand=1)

# create screenshot button
ss_button = tk.Button(frames[15], text='Screenshot')
ss_button.pack(fill=tk.BOTH, expand=1)

eqns_button = tk.Button(frames[16], text='Background equations')
eqns_button.pack(fill=tk.BOTH, expand=1)

# create result sheet
sheet = tksheet.Sheet(frames[17], width=750, show_row_index=False, show_x_scrollbar=False)
sheet.grid()
sheet.set_options(total_columns=9)
sheet.headers(["FS", "r (m)", "H (m)", "a", "C", "RTI", "Tact (\u2103)", "Q (MW)", "t (s)"])
sheet.set_all_column_widths(80)

sheet.enable_bindings(("single_select",

                       "drag_select",

                       "row_select",

                       "column_width_resize",

                       "arrowkeys",

                       "right_click_popup_menu",

                       "rc_select",

                      # "rc_insert_row",

                      # "rc_delete_row",

                       "copy",

                       #"cut",

                       #"paste",

                       #"delete",

                       #"undo",

                       "edit_cell"
                       ))

frames[17].grid(columnspan=3, rowspan=2)
frames[7].grid(columnspan=3, rowspan=2)

def eqns():
    eqns_window = Toplevel(root)
    eqns_window.title("Equations")
    image = Image.open("eqns.png")
    canvas_for_image = Canvas(eqns_window, width=image.width, height=image.height)
    canvas_for_image.image = ImageTk.PhotoImage(image)
    canvas_for_image.create_image(0, 0, anchor=tk.NW, image=canvas_for_image.image)
    canvas_for_image.pack()

def shot():
    global graphlist
    global sheet
    top = Toplevel(root)
    top.title("Screenshot window")

    figure = Figure(figsize=(6, 4), tight_layout=True)
    graph = FigureCanvasTkAgg(figure, master=top)
    graph.get_tk_widget().pack()

    ax1 = figure.add_subplot()
    for i in range(bp):
        # create pointers
        xpoint = 2 * i
        ypoint = 2 * i + 1

        ax1.plot(graphlist[xpoint], graphlist[ypoint], color=colours[i], label='FS' + str(i + 1))
        ax1.hlines(y=graphlist[ypoint][-1], xmin=graphlist[xpoint][-1], xmax=900, color=colours[i])  # horizontal line

    ax1.set_xlim(0, )
    ax1.set_ylim(0, )

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Q (MW)')

    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc="lower right")

    ## create result sheet
    ssheet = tksheet.Sheet(top, width=750, show_row_index=False, show_x_scrollbar=False)
    ssheet.pack()
    ssheet.set_options(total_columns=9)
    ssheet.headers(["FS", "r (m)", "H (m)", "a", "C", "RTI", "Tact (\u2103)", "Q (MW)", "t (s)"])

    ssheet.set_sheet_data(sheet.get_sheet_data(return_copy=1))
    ssheet.set_all_column_widths(80, redraw=True)
    for i in range(bp):
        ssheet.highlight_cells(row=i, column=0, fg=colours[i], redraw=True)
    ssheet.align(align="center", redraw=True)

    top.update()
    # Get the current active window
    active_window = pyautogui.getActiveWindow()

    # Take a screenshot of the active window
    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    filename = f'screenshot-{current_time}.png'
    screenshot = pyautogui.screenshot(region=(active_window.left+25, active_window.top+42, active_window.width-54, active_window.height-100))
    screenshot.save(filename)
    send_to_clipboard(screenshot)

    top.destroy()


# clear function
def clear():
    global bp
    global graphlist
    bp -= 1

    del graphlist[-2:]

    for widget in frames[7].winfo_children():
        widget.destroy()

    figure = Figure(figsize=(6, 4), tight_layout=True)
    graph = FigureCanvasTkAgg(figure, master=frames[7])
    graph.get_tk_widget().pack()

    ax1 = figure.add_subplot()
    for i in range(bp):
        # create pointers
        xpoint = 2 * i
        ypoint = 2 * i + 1

        ax1.plot(graphlist[xpoint], graphlist[ypoint], color=colours[i], label='FS' + str(i + 1))
        ax1.hlines(y=graphlist[ypoint][-1], xmin=graphlist[xpoint][-1], xmax=900, color=colours[i])  # horizontal line
        sheet.highlight_cells(row=i, column=0, fg=colours[i])

    ax1.set_xlim(0, )
    ax1.set_ylim(0, )

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Q (MW)')

    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc="lower right")

    sheet.delete_row(idx=bp, redraw=True)
    sheet.align(align="center", redraw=True)

    time_label.configure(font="none 12 bold", relief=tk.GROOVE,
                         text="Time until activation in s / min is: - \nValue of Q at activation in MW is: - ")
    if bp == 0:
        clr_button.configure(state=DISABLED)
    else:
        clr_button.configure(state=ACTIVE)


# function to calculate results and print figure
def calculate():
    global bp
    global graphlist
    bp += 1
    root.geometry("")
    dropdown2.set("Enter alpha:")
    dropdown.set("Presets")

    for widget in frames[7].winfo_children():
        widget.destroy()

    r = float(r_entry.get())
    H = float(H_entry.get())
    a = float(a_entry.get())
    C = float(C_entry.get())
    RTI = float(RTI_entry.get())
    T_act = float(Tact_entry.get())
    T_i = float(Ti_entry.get())
    T_a = float(Ti_entry.get())

    time_result, q_result, result_arr = loop(r, H, a, C, RTI, T_act, T_i, T_a, t, T_i, step)
    q_result = q_result /1000
    q_result = round(q_result, 3)
    time_result = round(time_result, 3)
    time_label.configure(font="none 12 bold", relief=tk.GROOVE,
                         text="Time until activation in s / min is: " + str(time_result) + " / " + str(
                             round(time_result / 60, 3)) + "\nValue of Q at activation in MW is: " + str(
                             q_result))

    # plotting
    Qypoints = np.array(result_arr[:, 0])
    xpoints = np.array(result_arr[:, 5])

    graphlist.append(xpoints)
    graphlist.append(Qypoints)

    figure = Figure(figsize=(6, 4), tight_layout=True)
    graph = FigureCanvasTkAgg(figure, master=frames[7])
    graph.get_tk_widget().pack()

    ax1 = figure.add_subplot()
    for i in range(bp):
        # create pointers
        xpoint = 2 * i
        ypoint = 2 * i + 1

        ax1.plot(graphlist[xpoint], graphlist[ypoint], color=colours[i], label='FS' + str(i + 1))
        ax1.hlines(y=graphlist[ypoint][-1], xmin=graphlist[xpoint][-1], xmax=900, color=colours[i])  # horizontal line
        sheet.highlight_cells(row=i, column=0, fg=colours[i])

    ax1.set_xlim(0, )
    ax1.set_ylim(0, )

    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Q (MW)')

    lines, labels = ax1.get_legend_handles_labels()
    ax1.legend(lines, labels, loc="lower right")

    # create result sheet
    a = alphanototext(a)
    rowindex = 'FS' + str(bp)
    sheet.insert_row([rowindex,r, H, a, C, RTI, T_act, q_result, time_result], redraw=True)
    sheet.align(align="center", redraw=True)

    if bp == 0:
        clr_button.configure(state=DISABLED)
    else:
        clr_button.configure(state=ACTIVE)


calc_button.configure(command=calculate)

clr_button.configure(command=clear)

ss_button.configure(command=shot)

eqns_button.configure(command=eqns)

if bp == 0:
    clr_button.configure(state=DISABLED)
else:
    clr_button.configure(state=ACTIVE)

root.mainloop()

