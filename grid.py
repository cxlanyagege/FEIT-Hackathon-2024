from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime

import tkinter as tk
import pandas as pd
import numpy as np
import keras

# Register custom mse function
@keras.saving.register_keras_serializable()
def mse(y_true, y_pred):
    return keras.losses.mean_squared_error(y_true, y_pred)

# Load the model
model = keras.models.load_model('model.h5', custom_objects={'mse': mse})
model_r = keras.models.load_model('model_reactive.h5', custom_objects={'mse': mse})

# Read CSV files
df = pd.read_csv('data/customer_power_data.csv', parse_dates=['timestamp'])
df_r = pd.read_csv('data/customer_reactive_power_data.csv', parse_dates=['timestamp'])

# Extract year, month, and day from timestamp
df['year'] = df['timestamp'].dt.year
df['month'] = df['timestamp'].dt.month
df['day'] = df['timestamp'].dt.day

# Generate a list of years, months, and days
years = sorted(df['year'].unique())
current_year = datetime.now().year
years = list(range(min(years), current_year + 1))
months = list(range(1, 13))
days = list(range(1, 32))

# Main window
root = tk.Tk()
root.title("Investor")
root.geometry("800x600")
root.resizable(False, False)
root.attributes("-toolwindow", True)

# Create year combobox
year_var = tk.StringVar(value=str([0]))
ttk.Label(root, text="Year:").grid(row=0, column=0, padx=5, pady=5)
year_combobox = ttk.Combobox(root, textvariable=year_var, values=[str(year) for year in years])
year_combobox.grid(row=0, column=1, padx=5, pady=5)
year_combobox.current(0)

# Create month combobox
month_var = tk.StringVar(value="1")
ttk.Label(root, text="Month:").grid(row=0, column=2, padx=5, pady=5)
month_combobox = ttk.Combobox(root, textvariable=month_var, values=[str(month) for month in months])
month_combobox.grid(row=0, column=3, padx=5, pady=5)
month_combobox.current(0)

# Create day combobox
day_var = tk.StringVar(value="1")
ttk.Label(root, text="Day:").grid(row=0, column=4, padx=5, pady=5)
day_combobox = ttk.Combobox(root, textvariable=day_var, values=[str(day) for day in days])
day_combobox.grid(row=0, column=5, padx=5, pady=5)
day_combobox.current(0)

# Create time slider
time_var = tk.IntVar(value=0)
ttk.Label(root, text="Time:").grid(row=1, column=0, padx=5, pady=5)
time_slider = ttk.Scale(root, from_=0, to=47, orient='horizontal', variable=time_var, command=lambda v: update_time_display())
time_slider.grid(row=1, column=1, columnspan=5, padx=5, pady=5, sticky="ew")

# Create time display
time_display = tk.StringVar()
time_display.set("00:00")
ttk.Label(root, textvariable=time_display).grid(row=2, column=1, columnspan=5, padx=5, pady=5)

# Create a frame to hold the data display
data_frame = ttk.Frame(root, borderwidth=2, relief="sunken")
data_frame.grid(row=3, columnspan=6, padx=10, pady=10, sticky="nsew")

# Configure grid weights
root.grid_rowconfigure(3, weight=1)
root.grid_columnconfigure(5, weight=1)
data_frame.grid_rowconfigure(0, weight=1)
data_frame.grid_columnconfigure(0, weight=1)

# Load visualisation background image
try:
    original_image = Image.open('background.jpg')
    photo = ImageTk.PhotoImage(original_image)
    
    # Label
    background_label = tk.Label(data_frame, image=photo)
    background_label.image = photo
    background_label.place(relwidth=1, relheight=1)
    
    def resize_image(event):
        new_width = event.width
        new_height = event.height
        resized_image = original_image.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(resized_image)
        background_label.config(image=photo)
        background_label.image = photo

    data_frame.bind("<Configure>", resize_image)
    
except Exception as e:
    print(f"Error loading background image: {e}")

# Define positions for data labels
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

# Create data labels for each item
data_labels = {}
for data_item, (x, y) in data_positions.items():
    label = tk.Label(data_frame, text="", bg="white")
    label.place(x=x, y=y)
    data_labels[data_item] = label

# Create total sum label
sum_label = tk.Label(data_frame, text="", bg="white")
sum_label.place(x=26, y=100)

# Recursive prediction function
def recursive_predict(model, input_data, steps):
    predictions = []
    for _ in range(steps):
        prediction = model.predict(input_data)
        prediction = np.expand_dims(prediction, axis=1)
        input_data = np.append(input_data[:, 1:, :], prediction, axis=1)
        predictions.append(prediction)
    return predictions

# Update time display
def update_time_display():
    time_value = time_var.get()
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
        sum_label.config(text="N/A")
        return
    
    # 获取 df 中的最后一条记录的 timestamp
    last_timestamp = df['timestamp'].max()
    
    # 查找对应时间的数据
    if selected_time in df['timestamp'].values:
        row = df[df['timestamp'] == selected_time]
        row_r = df_r[df_r['timestamp'] == selected_time]
        total_sum = 0  # 初始化总和
        total_sum_r = 0  # 初始化无功功率总和
        for i, column in enumerate(df.columns[1:32]):  # 只取前31列数据
            value = row[column].values[0]
            value_r = row_r[column].values[0]
            formatted_value = f"P: {value:.2f}\nQ: {value_r:.2f}"  # 保留两位小数，并在第二行显示 df_r 的数值
            data_labels[f'data{i+1}'].config(text=formatted_value)
            total_sum += value  # 累加每个居民的用电量
            total_sum_r += value_r  # 累加每个居民的无功功率
        sum_label.config(text=f"P: {total_sum:.2f}\nQ: {total_sum_r:.2f}")  # 更新总和显示
    elif selected_time > last_timestamp:
        # 获取最新的输入数据
        latest_data = df.iloc[-48:, 1:32].values.astype(np.float32)  # 获取最后48行数据，去掉时间戳列，并转换为 float32
        latest_data_r = df_r.iloc[-48:, 1:32].values.astype(np.float32)  # 获取最后48行数据，去掉时间戳列，并转换为 float32
        
        # 如果数据不足48行，用零填充
        if latest_data.shape[0] < 48:
            padding = np.zeros((48 - latest_data.shape[0], latest_data.shape[1]), dtype=np.float32)
            latest_data = np.vstack((padding, latest_data))
        if latest_data_r.shape[0] < 48:
            padding_r = np.zeros((48 - latest_data_r.shape[0], latest_data_r.shape[1]), dtype=np.float32)
            latest_data_r = np.vstack((padding_r, latest_data_r))
        
        # 构建输入数据，形状为 (1, 48, 31)
        input_data = np.expand_dims(latest_data, axis=0)
        input_data_r = np.expand_dims(latest_data_r, axis=0)

        # 计算时间步数
        time_diff = selected_time - last_timestamp
        steps = int(time_diff.total_seconds() // 1800)  # 每30分钟一个时间步
        
        # 预测未来的时间步数据
        predictions = recursive_predict(model, input_data, steps)
        predictions_r = recursive_predict(model_r, input_data_r, steps)
        
        # 检查 predictions 列表是否为空
        if predictions and predictions_r:
            # 获取最新的预测结果
            latest_prediction = predictions[-1][0][0]  # 获取最后一个预测结果，并去掉外层的列表
            latest_prediction_r = predictions_r[-1][0][0]
            total_sum = 0
            total_sum_r = 0
            
            # 将最新的预测结果展示到界面上
            for i, (value, value_r) in enumerate(zip(latest_prediction, latest_prediction_r)):
                formatted_value = f"P: {value:.2f}\nQ: {value_r:.2f}"  # 保留两位小数，并在第二行显示 df_r 的数值
                data_labels[f'data{i+1}'].config(text=formatted_value)
                total_sum += value  # 累加每个居民的用电量
                total_sum_r += value_r  # 累加每个居民的无功功率
            sum_label.config(text=f"P: {total_sum:.2f}\nQ: {total_sum_r:.2f}")  # 更新总和显示
        else:
            for label in data_labels.values():
                label.config(text="N/A")
            sum_label.config(text="N/A")
    else:
        for label in data_labels.values():
            label.config(text="N/A")
        sum_label.config(text="N/A")

# 绑定更新数据显示的事件
year_combobox.bind("<<ComboboxSelected>>", lambda e: update_data_display())
month_combobox.bind("<<ComboboxSelected>>", lambda e: update_data_display())
day_combobox.bind("<<ComboboxSelected>>", lambda e: update_data_display())

# 初始化数据展示
update_time_display()

# 运行主循环
root.mainloop()
