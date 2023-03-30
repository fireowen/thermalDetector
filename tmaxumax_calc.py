from main import *


def tmaxumaxCalcfunc():
    #Create label
    label = tk.Label(root, text="Tmax and Umax Calculator", font="none 16 bold")
    label.grid(row=0, column=1)

    #Create labels for inputs
    r_label = tk.Label(root, text="Enter r:")
    r_label.grid(row=1, column=0)

    H_label = tk.Label(root, text="Enter H:")
    H_label.grid(row=2, column=0)

    Q_label = tk.Label(root, text="Enter Q:")
    Q_label.grid(row=3, column=0)

    Tinf_label = tk.Label(root, text="Enter Tinf:")
    Tinf_label.grid(row=4, column=0)

    #Create entry boxes for inputs
    r_entry = tk.Entry(root, width=10)
    r_entry.grid(row=1, column=1)

    H_entry = tk.Entry(root, width=10)
    H_entry.grid(row=2, column=1)

    Q_entry = tk.Entry(root, width=10)
    Q_entry.grid(row=3, column=1)

    Tinf_entry = tk.Entry(root, width=10)
    Tinf_entry.grid(row=4, column=1)

    #Create calculate button
    calc_button = tk.Button(root, text="Calculate", width=10)
    calc_button.grid(row=5, column=1)

    #Create result labels
    ratio_label = tk.Label(root, text= "r/H = ")
    ratio_label.grid(row=6, column=1)

    result1_label = tk.Label(root, text="Tmax = ")
    result1_label.grid(row=7, column=1)

    result2_label = tk.Label(root, text="Umax = ")
    result2_label.grid(row=8, column=1)

    #Function to calculate results
    def calculate():
        r = float(r_entry.get())
        H = float(H_entry.get())
        Q = float(Q_entry.get())
        Tinf = float(Tinf_entry.get())
        result1 = func.Tmax(r, H, Q)
        result2 = func.Umax(r, H, Q)
        ratio = r / H

        result1_label.configure(text="Tmax = " + str(result1))
        result2_label.configure(text="Umax = " + str(result2))
        ratio_label.configure(text="r/H = " + str(ratio))

    #Connect calculate button to calculate function
    calc_button.configure(command=calculate)

