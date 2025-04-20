# admin.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

from common import BASE_URL

API_ADD_URL = f"{BASE_URL}/add_product"

class AdminScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        self.add_widget(Label(text="👑 상품 등록(Admin)", font_name="MyFont", font_size=24, size_hint_y=None, height=50))

        self.name = TextInput(hint_text="상품명", font_name="MyFont", multiline=False, size_hint_y=None, height=45)
        self.price = TextInput(hint_text="가격", font_name="MyFont", multiline=False, input_filter='int', size_hint_y=None, height=45)
        self.desc = TextInput(hint_text="설명", font_name="MyFont", multiline=True, size_hint_y=None, height=80)
        self.img  = TextInput(hint_text="이미지 URL", font_name="MyFont", multiline=False, size_hint_y=None, height=45)

        for w in (self.name, self.price, self.desc, self.img):
            self.add_widget(w)

        btn = Button(text="상품 등록", font_name="MyFont", size_hint_y=None, height=50, background_color=(1,0.8,0.9,1))
        btn.bind(on_press=self.add_product)
        self.add_widget(btn)

        self.status = Label(text="", font_name="MyFont", size_hint_y=None, height=30, color=(1,0,0,1))
        self.add_widget(self.status)

    def add_product(self, *args):
        data = {
            "name": self.name.text,
            "price": int(self.price.text or 0),
            "description": self.desc.text,
            "image_url": self.img.text
        }
        try:
            res = requests.post(API_ADD_URL, json=data)
            if res.status_code == 200:
                self.status.text = "등록 성공! 🎉"
            else:
                self.status.text = "등록 실패"
        except:
            self.status.text = "서버 연결 실패"

class AdminApp(App):
    def build(self):
        return AdminScreen()

if __name__=="__main__":
    AdminApp().run()
