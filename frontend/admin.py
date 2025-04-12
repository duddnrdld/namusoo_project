from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

API_ADD_PRODUCT_URL = "http://127.0.0.1:5000/add_product"

class AdminScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=20, **kwargs)
        self.add_widget(Label(text="👑 상품 등록", font_size=22, size_hint_y=None, height=50))
        self.name_input = TextInput(hint_text="상품명", multiline=False, size_hint_y=None, height=40)
        self.price_input = TextInput(hint_text="가격", multiline=False, input_filter='int', size_hint_y=None, height=40)
        self.desc_input = TextInput(hint_text="설명", multiline=True, size_hint_y=None, height=80)
        self.image_input = TextInput(hint_text="이미지 URL", multiline=False, size_hint_y=None, height=40)
        self.result_label = Label(text="", size_hint_y=None, height=30)
        submit_btn = Button(text="✅ 상품 등록", size_hint_y=None, height=50)
        submit_btn.bind(on_press=self.register_product)
        for widget in [self.name_input, self.price_input, self.desc_input, self.image_input, submit_btn, self.result_label]:
            self.add_widget(widget)

    def register_product(self, instance):
        data = {
            "name": self.name_input.text,
            "price": int(self.price_input.text),
            "description": self.desc_input.text,
            "image_url": self.image_input.text
        }
        try:
            res = requests.post(API_ADD_PRODUCT_URL, json=data)
            if res.status_code == 200:
                self.result_label.text = "🎉 상품 등록 완료!"
            else:
                self.result_label.text = "등록 실패! 다시 확인해줘."
        except:
            self.result_label.text = "서버 연결 실패!"

class NamusooAdminApp(App):
    def build(self):
        return AdminScreen()

if __name__ == '__main__':
    NamusooAdminApp().run()