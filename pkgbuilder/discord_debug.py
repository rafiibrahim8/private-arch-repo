import datetime
import requests

class DebugDiscord:
    def __init__(self, hook_url, tz=None, time_format='%Y-%m-%d %H:%M:%S'):
        self.__debug_hook = hook_url.strip()

        if not tz:
            tz = datetime.timezone.utc
        self.__timezone = tz
        self.__time_fmt = time_format
    
    def __send_text_hook(self, text, with_time):
        if with_time:
            fmt_time = datetime.datetime.now(self.__timezone).strftime(self.__time_fmt)
            text = f'[{fmt_time}]{text}'
        if not self.__debug_hook:
            print(text)
            return
        try:
            requests.post(self.__debug_hook, json={'content': text})
        except:
            print(text)

    def info(self, message, with_time=True):
        self.__send_text_hook(f'[INFO] {message}', with_time)

    def error(self, message, with_time=True):
        self.__send_text_hook(f'[ERROR] {message}', with_time)
