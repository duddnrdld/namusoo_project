# order.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests

from common import BASE_URL

API_ORDER_URL = f"{BASE_URL}/order"

class OrderScreen(BoxLayout):
    def __init__(self, user_id=1, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        self.add_widget(Label(text="📦 배송 정보 입력", font_name="MyFont", font_size=24, size_hint_y=None, height=50))

        self.addr = TextInput(hint_text="도로명 주소", font_name="MyFont", multiline=False, size_hint_y=None, height=45)
        self.detail = TextInput(hint_text="상세 주소", font_name="MyFont", multiline=False, size_hint_y=None, height=45)
        self.add_widget(self.addr)
        self.add_widget(self.detail)

        btn = Button(text="🛍️ 주문하기", font_name="MyFont", size_hint_y=None, height=50, background_color=(0.8,1,0.9,1))
        btn.bind(on_press=self.do_order)
        self.add_widget(btn)

        self.status = Label(text="", font_name="MyFont", size_hint_y=None, height=30, color=(1,0,0,1))
        self.add_widget(self.status)

        self.user_id = user_id

    def do_order(self, *args):
        data = {"user_id":self.user_id, "address":self.addr.text, "detail":self.detail.text}
        try:
            res = requests.post(API_ORDER_URL, json=data)
            if res.status_code == 200:
                self.status.text = "주문 완료! 🎉"
            else:
                self.status.text = "주문 실패"
        except:
            self.status.text = "서버 연결 실패"

class OrderApp(App):
    def build(self):
        return OrderScreen()

if __name__=="__main__":
    OrderApp().run()
