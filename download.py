import requests
from bs4 import BeautifulSoup
import os

# 设置目标URL
base_url = "https://nemweb.com.au/Reports/Archive/DispatchIS_Reports/"
base_download_url = "https://nemweb.com.au/"

# 请求页面内容
response = requests.get(base_url)

# 如果请求成功，继续解析页面
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # 找到所有链接
    links = soup.find_all("a")
    
    # 创建保存文件的目录
    download_dir = "DispatchIS_Reports"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    # 遍历所有链接
    for link in links:
        file_name = link.get("href")
        if file_name and file_name.endswith(".zip"):  # 确认只下载zip文件
            # 拼接文件完整的 URL
            file_url = base_download_url + file_name.lstrip('/')  # 确保 URL 拼接正确
            print(f"Downloading {file_name} from {file_url}...")
            
            # 下载文件
            file_response = requests.get(file_url)
            
            # 确定保存路径
            file_path = os.path.join(download_dir, os.path.basename(file_name))  # 提取文件名
            print(f"Saving {file_name} to {file_path}...")
            
            # 保存文件
            with open(file_path, "wb") as f:
                f.write(file_response.content)
                
            print(f"Saved {file_name} to {file_path}")
else:
    print(f"Failed to access the website. Status code: {response.status_code}")
