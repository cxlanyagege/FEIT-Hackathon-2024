import os
import zipfile

# 定义文件夹路径
zip_folder = 'DispatchIS_Reports/raw'
extract_folder = os.path.join(zip_folder, 'raw')

# 创建目标解压文件夹，如果不存在的话
os.makedirs(extract_folder, exist_ok=True)

# 遍历zip文件夹中的所有文件
for file_name in os.listdir(zip_folder):
    if file_name.endswith('.zip'):
        zip_path = os.path.join(zip_folder, file_name)
        
        # 解压zip文件
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

print(f"All zip files have been successfully extracted to {extract_folder}")
