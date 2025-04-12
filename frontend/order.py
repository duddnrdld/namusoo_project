from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests

API_ORDER_URL = "http://127.0.0.1:5000/order"

class OrderScreen(BoxLayout):
    def __init__(self, user_id=1, **kwargs):
        super().__init__(orientation='vertical', spacing=15, padding=20, **kwargs)
        self.add_widget(Label(text="📦 배송 정보 입력", font_size=22, size_hint_y=None, height=50))
        self.address_input = TextInput(hint_text="도로명 주소", multiline=False, size_hint_y=None, height=40)
        self.detail_input = TextInput(hint_text="상세 주소", multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.address_input)
        self.add_widget(self.detail_input)
        self.result_label = Label(text="", size_hint_y=None, height=30)
        self.add_widget(self.result_label)
        self.order_button = Button(text="🛍️ 주문하기", size_hint_y=None, height=50)
        self.order_button.bind(on_press=self.place_order)
        self.add_widget(self.order_button)
        self.user_id = user_id

    def place_order(self, instance):
        address = self.address_input.text
        detail = self.detail_input.text
        payload = {"user_id": self.user_id, "address": address, "detail": detail}
        try:
            res = requests.post(API_ORDER_URL, json=payload)
            if res.status_code == 200:
                self.result_label.text = "🎉 주문 완료!"
            else:
                self.result_label.text = "주문 실패! 다시 시도해줘."
        except:
            self.result_label.text = "서버 연결 오류!"

class NamusooOrderApp(App):
    def build(self):
        return OrderScreen()

if __name__ == '__main__':
    NamusooOrderApp().run()