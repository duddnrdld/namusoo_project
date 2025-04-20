# login.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

from common import BASE_URL

API_LOGIN_URL = f"{BASE_URL}/login"
API_SIGNUP_URL = f"{BASE_URL}/signup"  # 백엔드에 /signup 엔드포인트 필요

# 테스트용 임시 관리자 계정
#   아이디: admin@namusoo.com
#   비밀번호: admin1234

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=15, **kwargs)
        self.add_widget(Label(text="나무수디자인 로그인", font_name="MyFont", font_size=26, size_hint_y=None, height=60))

        self.email = TextInput(hint_text="이메일", font_name="MyFont", multiline=False, size_hint_y=None, height=45)
        self.password = TextInput(hint_text="비밀번호", font_name="MyFont", multiline=False, password=True, size_hint_y=None, height=45)
        self.add_widget(self.email)
        self.add_widget(self.password)

        btn_login = Button(text="로그인", font_name="MyFont", size_hint_y=None, height=50, background_color=(1,0.8,0.8,1))
        btn_login.bind(on_press=self.do_login)
        self.add_widget(btn_login)

        btn_signup = Button(text="회원가입 하러 가기", font_name="MyFont", size_hint_y=None, height=40, background_color=(0.8,0.9,1,1))
        btn_signup.bind(on_press=self.open_signup)
        self.add_widget(btn_signup)

        self.status = Label(text="", font_name="MyFont", size_hint_y=None, height=30, color=(1,0,0,1))
        self.add_widget(self.status)

    def do_login(self, *args):
        data = {"email": self.email.text, "password": self.password.text}
        try:
            res = requests.post(API_LOGIN_URL, json=data)
            if res.status_code == 200:
                self.status.text = "로그인 성공! 🎉"
                # TODO: 메인 화면으로 넘어가는 로직 추가
            else:
                self.status.text = "로그인 실패: 아이디/비밀번호 확인"
        except:
            self.status.text = "서버 연결 실패"

    def open_signup(self, *args):
        from signup import SignupApp
        SignupApp().run()

class LoginApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    LoginApp().run()
