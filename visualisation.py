import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # 引入 Pillow 库
import pandas as pd
import numpy as np
import keras
from datetime import datetime

# 定义并注册自定义函数
@keras.saving.register_keras_serializable()
def mse(y_true, y_pred):
    return keras.losses.mean_squared_error(y_true, y_pred)

# 加载保存的模型
model = keras.models.load_model('model.h5', custom_objects={'mse': mse})

# 读取 CSV 文件
df = pd.read_csv('data/customer_power_data.csv', parse_dates=['timestamp'])

# 提取年、月、日信息
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day

# 获取唯一的年、月、日列表
years = sorted(df['year'].unique())
current_year = datetime.now().year
years = list(range(min(years), current_year + 1))

months = list(range(1, 13))
days = list(range(1, 32))

# 创建主窗口
root = tk.Tk()
root.title("时间选择器")

# 设置窗口大小（可选）
root.geometry("800x600")  # 根据需要调整窗口大小

# 禁用窗口调整大小和最大化
root.resizable(False, False)
root.attributes("-toolwindow", True)

# 创建年份选择框
year_var = tk.StringVar(value=str([0]))
ttk.Label(root, text="年:").grid(row=0, column=0, padx=5, pady=5)
year_combobox = ttk.Combobox(root, textvariable=year_var, values=[str(year) for year in years])
year_combobox.grid(row=0, column=1, padx=5, pady=5)
year_combobox.current(0)  # 默认选择最老的年份

# 创建月份选择框
month_var = tk.StringVar(value="1")
ttk.Label(root, text="月:").grid(row=0, column=2, padx=5, pady=5)
month_combobox = ttk.Combobox(root, textvariable=month_var, values=[str(month) for month in months])
month_combobox.grid(row=0, column=3, padx=5, pady=5)
month_combobox.current(0)  # 默认选择1月

# 创建日期选择框
day_var = tk.StringVar(value="1")
ttk.Label(root, text="日:").grid(row=0, column=4, padx=5, pady=5)
day_combobox = ttk.Combobox(root, textvariable=day_var, values=[str(day) for day in days])
day_combobox.grid(row=0, column=5, padx=5, pady=5)
day_combobox.current(0)  # 默认选择1日

# 创建时间滑动条（0到48，每单位代表30分钟）
time_var = tk.IntVar(value=0)  # 使用整数变量
ttk.Label(root, text="时间:").grid(row=1, column=0, padx=5, pady=5)
time_slider = ttk.Scale(root, from_=0, to=47, orient='horizontal', variable=time_var, command=lambda v: update_time_display())
time_slider.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

# 创建显示当前时间的标签
time_display = tk.StringVar()
time_display.set("00:00")
ttk.Label(root, textvariable=time_display).grid(row=2, column=1, columnspan=5, padx=5, pady=5)

# 创建显示数据的框架
data_frame = ttk.Frame(root, borderwidth=2, relief="sunken")
data_frame.grid(row=3, columnspan=6, padx=10, pady=10, sticky="nsew")

# 配置 grid 以使 data_frame 可扩展
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(5, weight=1)
data_frame.grid_rowconfigure(0, weight=1)
data_frame.grid_columnconfigure(0, weight=1)

# 加载背景图并显示在 data_frame 中
try:
    original_image = Image.open('background.jpg')
    photo = ImageTk.PhotoImage(original_image)
    
    # 创建一个标签用于显示背景图
    background_label = tk.Label(data_frame, image=photo)
    background_label.image = photo  # 保持对图像的引用
    background_label.place(relwidth=1, relheight=1)
    
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        background_label.config(image=photo)
        background_label.image = photo  # 保持对图像的引用

    data_frame.bind("<Configure>", resize_image)
    
    # 定义鼠标点击事件处理函数
    def on_click(event):
        print(f"Mouse clicked at: ({event.x}, {event.y})")
    
    # 绑定鼠标点击事件
    background_label.bind("<Button-1>", on_click)
    
except Exception as e:
    print(f"Error loading background image: {e}")

# 定义数据项的位置（占位符）
data_positions = {
    'data1': (99, 74),
    'data2': (167, 73),
    'data3': (241, 73),
    'data4': (318, 78),
    'data5': (387, 65),
    'data6': (465, 72),
    'data7': (543, 73),
    'data8': (619, 81),
    'data9': (73, 222),
    'data10': (108, 278),
    'data11': (143, 221),
    'data12': (182, 273),
    'data13': (216, 219),
    'data14': (257, 266),
    'data15': (282, 216),
    'data16': (330, 273),
    'data17': (354, 215),
    'data18': (397, 269),
    'data19': (429, 222),
    'data20': (470, 266),
    'data21': (499, 222),
    'data22': (554, 204),
    'data23': (554, 256),
    'data24': (556, 311),
    'data25': (622, 234),
    'data26': (621, 292),
    'data27': (681, 206),
    'data28': (683, 260),
    'data29': (682, 314),
    'data30': (682, 368),
    'data31': (685, 426)
}

# 创建用于显示数据的 Label 小部件
data_labels = {}
for data_item, (x, y) in data_positions.items():
    label = tk.Label(data_frame, text="", bg="white")  # 设置背景为白色以便于查看
    label.place(x=x, y=y)
    data_labels[data_item] = label

# 定义递归预测函数
def recursive_predict(model, input_data, steps):
    if steps == 0:
        return []
    
    prediction = model.predict(input_data)
    predictions = [prediction]
    next_input_data = np.expand_dims(prediction, axis=0)
    predictions += recursive_predict(model, next_input_data, steps - 1)
    
    return predictions

# 更新时间显示的函数
def update_time_display():
    time_value = time_var.get()
    # 确保 time_value 为整数
    rounded_time_value = int(round(time_value))
    if rounded_time_value != time_value:
        time_var.set(rounded_time_value)
    hour = int(rounded_time_value // 2)
    minute = int((rounded_time_value % 2) * 30)
    time_display.set(f"{hour:02d}:{minute:02d}")
    update_data_display()

# 更新数据显示的函数
def update_data_display():
    year = int(year_var.get())
    month = int(month_var.get())
    day = int(day_var.get())
    time_value = time_var.get()
    hour = int(time_value // 2)
    minute = int((time_value % 2) * 30)
    try:
        selected_time = pd.Timestamp(year, month, day, hour, minute)
    except ValueError:
        # Handle invalid date
        for label in data_labels.values():
            label.config(text="N/A")
        return
    
    # 获取 df 中的最后一条记录的 timestamp
    last_timestamp = df['timestamp'].max()
    
    # 查找对应时间的数据
    if selected_time in df['timestamp'].values:
        row = df[df['timestamp'] == selected_time]
        for i, column in enumerate(df.columns[1:32]):  # 只取前31列数据
            value = row[column].values[0]
            formatted_value = f"{value:.2f}"  # 保留两位小数
            data_labels[f'data{i+1}'].config(text=formatted_value)
    elif selected_time > last_timestamp:
        # 获取最新的输入数据
        latest_data = df.iloc[-1, 1:32].values.astype(np.float32)  # 获取最后一行数据，去掉时间戳列，并转换为 float32
        
        # 构建输入数据，形状为 (1, 1, 31)
        input_data = np.expand_dims(np.expand_dims(latest_data, axis=0), axis=0)

        # 计算时间步数
        time_diff = selected_time - last_timestamp
        steps = int(time_diff.total_seconds() // 1800)  # 每30分钟一个时间步
        
        # 预测未来2个时间步的数据
        predictions = recursive_predict(model, input_data, steps)

        # 获取最新的预测结果
        latest_prediction = predictions[-1][0]  # 获取最后一个预测结果，并去掉外层的列表
        
        # 将最新的预测结果展示到界面上
        for i, value in enumerate(latest_prediction):
            formatted_value = f"{value:.2f}"  # 保留两位小数
            data_labels[f'data{i+1}'].config(text=formatted_value)
        
    else:
        for label in data_labels.values():
            label.config(text="N/A")

# 绑定更新数据显示的事件
year_combobox.bind("<<ComboboxSelected>>", lambda e: update_data_display())
month_combobox.bind("<<ComboboxSelected>>", lambda e: update_data_display())
day_combobox.bind("<<ComboboxSelected>>", lambda e: update_data_display())

# 初始化数据展示
update_time_display()

# 运行主循环
root.mainloop()
