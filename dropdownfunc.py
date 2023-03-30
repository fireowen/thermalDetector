from main import *

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

        a_text.set((1000 / (150 * 150)))
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
        r_text.set(5)
        r_entry.config(state="disabled")

        H_text.set(2.5)
        H_entry.config(state="disabled")

        a_text.set((1000 / (150 * 150)))
        a_entry.config(state="disabled")

        C_text.set(0.8)
        C_entry.config(state="disabled")

        RTI_text.set(50)
        RTI_entry.config(state="disabled")

        Tact_text.set(100)
        Tact_entry.config(state="disabled")

        Ti_text.set(20)
        Ti_entry.config(state="disabled")