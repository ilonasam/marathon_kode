import signal
import logging
import asyncio
import aiohttp
import json

class TemperatureService:  
    _sensorsTemp = {}
    # example_json = '{ "sensorId": "5d316ee8-a785-4e87-91d8-06f901c98a88","temperatureC": 23.4 }'

    def __exit_gracefully(signal, frame):
        raise KeyboardInterrupt

    def __raise_timeout(signum, frame):
        raise TimeoutError

    def __setup_signals(self):
        signal.signal(signal.SIGINT, self.__exit_gracefully)
        signal.signal(signal.SIGALRM, self.__raise_timeout) 
        signal.alarm(10)
            
    def __handler_urls_list(self, urls):
        if not urls:
            raise ValueError
        asyncio.run(self.__handler_connection_urls(urls))

    def __setup_logging(self):
        logging.basicConfig(level=logging.DEBUG, filename="py_log.log",filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")

    def get_temperature_list(self, urls):
        self.__setup_logging()
        self.__setup_signals()
        try:
            self.__handler_urls_list(urls)
            return self._sensorsTemp
        except TimeoutError:
            logging.debug("Превышено время выполнения программы")
        except KeyboardInterrupt:
            logging.debug("Прерывание программы")
        except ValueError:
            logging.debug("Передан пустой список")
        finally:
            signal.alarm(0)  
            
    async def __get(self, url, session):
        try:
            async with session.get(url=url) as response:
                resp = await response.read()
                # resp = self.example_json
                json_parse = json.loads(resp)
                sensor_id = json_parse["sensorId"]
                temperature = json_parse["temperatureC"]
                self._sensorsTemp[sensor_id] = temperature  
        except Exception as e:
            logging.debug(f"Не удалось получить данные по url: {url}")


    async def __handler_connection_urls(self, urls):
        async with aiohttp.ClientSession() as session:
            ret = await asyncio.gather(*(self.__get(url, session) for url in urls))

     
