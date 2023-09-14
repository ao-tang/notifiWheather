import yagmail
import requests
import configparser
import json

# 获取 config 中 set city 对应的城市代码
# 创建配置文件解析器
config = configparser.ConfigParser()
config.read('config.ini')  # 指定配置文件的路径

# 从配置文件中获取值
city = config.get('set','city')
sendToAdd = config.get('set','sendToAdd')
cityCode = config.get('set','cityCodefile')
user = config.get('yagmail','user')
host = config.get('yagmail','host')
psw = config.get('yagmail','psw')

# 指定要加载的文件名
file_name = f"{cityCode}"

# 使用 json.load() 从文件加载字典
with open(file_name, "r") as file:
    loaded_city_data = json.load(file)

city_code = loaded_city_data[city]

# 使用 requests 获取 JSON 数据
url = f'http://t.weather.sojson.com/api/weather/city/{city_code}'  # 替换为实际的 API 地址
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:

    # json_data = response.json()  # 将响应的 JSON 数据解析为字典
    # # 将 JSON 数据转换为 HTML 格式的邮件正文
    # html_body = "<html><body>"
    # for key, value in json_data.items():
    #     html_body += f"<p><strong>{key}:</strong> {value}</p>"
    # html_body += "</body></html>"

    data = response.json()

    # 构建HTML内容
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>天气信息</title>
    </head>
    <body>
        <h1>天气信息</h1>
        <p><strong>城市:</strong> {data['cityInfo']['city']}</p>
        <p><strong>日期:</strong> {data['date']}</p>
        <p><strong>时间:</strong> {data['time']}</p>
        <p><strong>温度:</strong> {data['data']['wendu']} ℃</p>
        <p><strong>湿度:</strong> {data['data']['shidu']}</p>
        <p><strong>空气质量:</strong> {data['data']['quality']}</p>
        <p><strong>感冒指数:</strong> {data['data']['ganmao']}</p>

        <h2>未来天气预报</h2>
        <ul>
    '''

    # 添加未来天气预报数据
    for forecast in data['data']['forecast']:
        html_content += f'''
            <li>
                <strong>{forecast['ymd']} ({forecast['week']}):</strong>
                {forecast['high']} / {forecast['low']}, {forecast['type']}
            </li>
        '''

    # 添加昨天天气数据
    yesterday = data['data']['yesterday']
    html_content += f'''
        </ul>

        <h2>昨天天气</h2>
        <p><strong>日期:</strong> {yesterday['ymd']}</p>
        <p><strong>最高温度:</strong> {yesterday['high']}</p>
        <p><strong>最低温度:</strong> {yesterday['low']}</p>
        <p><strong>天气类型:</strong> {yesterday['type']}</p>
    </body>
    </html>
    '''
    
    #发送邮件
    yagmail.register(f'{user}',f'{psw}')
    yag = yagmail.SMTP(user = f'{user}',host = f'{host}',encoding='GBK')
    yag.send(
        to = f'{sendToAdd}', 
        subject='天气信息',
        contents=html_content
    )
    yag.close()
else:
    print('无法获取 JSON 数据')
