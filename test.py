# 1. Delete all comments in service.py __OR__ insert correct value in urls[]
# 2. Run test.py

from package import *

urls = ["https://www.youtube.com",  
            "https://www.baidu.com",
            "https://www.yahoo.com",
            "https://www.amazon.com",
            "https://www.wikipedia.org",
            "http://www.qq.com",
            "https://www.google.co.in"]


if __name__ == '__main__':
    service = service.TemperatureService()
    print(service.get_temperature_list(urls))