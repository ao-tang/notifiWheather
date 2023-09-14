import json
from main import data 


# # 将HTML内容保存到文件
# with open('weather.html', 'w', encoding='utf-8') as html_file:
#     html_file.write(data)

# 指定要保存到的文件名
file_name = "test.json"

# 使用 json.dump() 将字典保存到文件
with open(file_name, "w", encoding='GBK') as file:
    json.dump(data, file)

print(f"字典已保存到文件 {file_name}")