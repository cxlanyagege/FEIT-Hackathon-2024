from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
import tkinter as tk

# Create main window
root = tk.Tk()
root.title("Consumer")
root.geometry("800x1200")
root.resizable(False, False)
root.attributes("-toolwindow", True)

# Catch close event
def on_closing():
    root.quit()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Add title at the top
title_label = ttk.Label(root, text="consumer 1", font=("Arial", 32))
title_label.pack(pady=10)

# Create a pie chart
def create_pie_chart():
    fig, ax = plt.subplots(figsize=(6, 6))  # Adjust figure size

    # Initialize with 0% PV energy, 100% grid energy
    sizes = [0, 100]
    colors = ['green', 'red']
    wedges, texts = ax.pie(sizes, colors=colors, startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    return fig, ax, wedges

# Update pie chart and labels
def update_pie_chart(pv_capacity):
    # pv_capacity is in kW (float)

    # Calculate daily energy production (kWh)
    average_sun_hours = 4  # Average sun hours per day
    daily_energy = pv_capacity * average_sun_hours  # in kWh

    # Total daily consumption
    total_consumption = 30  # kWh per day

    # Calculate percentages for pie chart
    pv_energy_percentage = (daily_energy / total_consumption) * 100
    if pv_energy_percentage > 100:
        pv_energy_percentage = 100
    grid_energy_percentage = 100 - pv_energy_percentage

    # Update pie chart wedges
    wedges[0].set_theta1(0)
    wedges[0].set_theta2(360 * pv_energy_percentage / 100)
    wedges[1].set_theta1(360 * pv_energy_percentage / 100)
    wedges[1].set_theta2(360)

    canvas.draw()

    # Calculate daily savings in $
    electricity_cost = 0.18  # $ per kWh
    daily_savings = daily_energy * electricity_cost  # in $

    # Calculate total savings over 10 years
    total_savings = daily_savings * 365 * 10  # in $

    # Update savings_value_label
    savings_value_label.config(text=f"${total_savings:,.2f}")

    # Calculate number of trees per year
    trees_per_year = 0.043 * daily_energy * 365

    # Update tree_value_label
    tree_value_label.config(text=f"{trees_per_year:.2f}")

    # Update kw_label
    kw_label.config(text=f"{pv_capacity:.1f} kW PV Install")

# Embed the pie chart into Tkinter interface
fig, ax, wedges = create_pie_chart()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(pady=40)

# Create slider
slider_frame = ttk.Frame(root)
slider_frame.pack(pady=20)

slider_savings = tk.Scale(
    slider_frame,
    from_=0,
    to=5,
    orient='horizontal',
    length=600,
    resolution=0.1,
    command=lambda val: update_pie_chart(float(val))
)
slider_savings.set(2.0)  # Set initial value
slider_savings.pack()

# Display PV install capacity
kw_label = ttk.Label(root, text="2.0 kW PV Install", font=("Arial", 32))
kw_label.pack(pady=10)

# Frame for maximum savings
savings_frame = ttk.Frame(root)
savings_frame.pack(pady=10)

savings_text_label = ttk.Label(savings_frame, text="Maximum $ Save in 10 years: ", font=("Arial", 28))
savings_text_label.pack(side='left')

savings_value_label = ttk.Label(savings_frame, text="$0.00", font=("Arial", 28), foreground='green')
savings_value_label.pack(side='left')

# Frame for equivalent trees planted per year
tree_frame = ttk.Frame(root)
tree_frame.pack(pady=10)

tree_text_label = ttk.Label(tree_frame, text="Equivalent to planting ", font=("Arial", 28))
tree_text_label.pack(side='left')

tree_value_label = ttk.Label(tree_frame, text="0.00", font=("Arial", 28), foreground='green')
tree_value_label.pack(side='left')

tree_unit_label = ttk.Label(tree_frame, text=" trees per year", font=("Arial", 28))
tree_unit_label.pack(side='left')

# Initial update
update_pie_chart(slider_savings.get())

# Run main loop
root.mainloop()
