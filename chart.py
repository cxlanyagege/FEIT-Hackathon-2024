import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 创建主窗口
root = tk.Tk()
root.title("Consumer")
root.geometry("400x600")

# 捕捉关闭事件，自动结束程序
def on_closing():
    root.quit()  # 结束主循环
    root.destroy()  # 销毁窗口

# 绑定关闭事件
root.protocol("WM_DELETE_WINDOW", on_closing)

# 创建一个饼图
def create_pie_chart(savings=10, expenses=90):
    fig, ax = plt.subplots(figsize=(3, 3))
    
    # 假设数据，绿色代表节约，红色代表普通开销
    labels = ['Savings', 'Other Expenses']
    sizes = [savings, expenses]  # 这里的值可以调整
    colors = ['green', 'red']
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    
    ax.axis('equal')  # 保持饼图为圆形
    return fig, ax

# 更新饼图
def update(val):
    savings = slider_savings.val
    expenses = 100 - savings
    ax.clear()
    fig, ax = create_pie_chart(savings, expenses)
    canvas.draw()

# 将饼图嵌入到Tkinter界面中
fig, ax = create_pie_chart()
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(pady=20)

# 创建滑块
slider_frame = ttk.Frame(root)
slider_frame.pack(pady=10)

slider_savings = Slider(plt.axes([0.25, 0.1, 0.65, 0.03]), 'Savings', 0, 100, valinit=10)
slider_savings.on_changed(update)

# 显示用户的PV安装容量和储蓄信息
kw_label = ttk.Label(root, text="0.5 kW PV Install")
kw_label.pack(pady=5)

# 输入最大节约金额
savings_entry = ttk.Entry(root)
savings_entry.insert(0, "Maximum $ Save in 10 years")
savings_entry.pack(pady=5)

# 输入种树数量等效
tree_entry = ttk.Entry(root)
tree_entry.insert(0, "Equivalent to planting ___ trees")
tree_entry.pack(pady=5)

# 运行主循环
root.mainloop()