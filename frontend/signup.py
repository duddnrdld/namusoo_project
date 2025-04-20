# signup.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

from common import BASE_URL
API_SIGNUP_URL = f"{BASE_URL}/signup"

class SignupScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        self.add_widget(Label(text="회원가입", font_name="MyFont", font_size=26, size_hint_y=None, height=60))

        self.email = TextInput(hint_text="이메일", font_name="MyFont", multiline=False, size_hint_y=None, height=45)
        self.pw1   = TextInput(hint_text="비밀번호", font_name="MyFont", multiline=False, password=True, size_hint_y=None, height=45)
        self.pw2   = TextInput(hint_text="비밀번호 확인", font_name="MyFont", multiline=False, password=True, size_hint_y=None, height=45)
        self.add_widget(self.email)
        self.add_widget(self.pw1)
        self.add_widget(self.pw2)

        btn = Button(text="회원가입 완료", font_name="MyFont", size_hint_y=None, height=50, background_color=(0.8,1,0.8,1))
        btn.bind(on_press=self.do_signup)
        self.add_widget(btn)

        self.status = Label(text="", font_name="MyFont", size_hint_y=None, height=30, color=(1,0,0,1))
        self.add_widget(self.status)

    def do_signup(self, *args):
        if self.pw1.text != self.pw2.text:
            self.status.text = "비밀번호가 일치하지 않습니다"
            return
        data = {"email": self.email.text, "password": self.pw1.text}
        try:
            res = requests.post(API_SIGNUP_URL, json=data)
            if res.status_code == 201:
                self.status.text = "회원가입 완료! 로그인해 주세요"
            else:
                self.status.text = f"실패: {res.json().get('message','?')}"
        except:
            self.status.text = "서버 연결 실패"

class SignupApp(App):
    def build(self):
        return SignupScreen()

if __name__ == "__main__":
    SignupApp().run()
