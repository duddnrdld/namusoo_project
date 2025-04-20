from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import requests

API_LOGIN_URL = "https://namusoo-backend.onrender.com/login"

class LoginScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', padding=20, spacing=10, **kwargs)
        self.email_input = TextInput(hint_text="이메일", multiline=False, size_hint_y=None, height=40)
        self.password_input = TextInput(hint_text="비밀번호", multiline=False, password=True, size_hint_y=None, height=40)
        self.add_widget(Label(text="나무수디자인 로그인", font_size=24, size_hint_y=None, height=60))
        self.add_widget(self.email_input)
        self.add_widget(self.password_input)
        login_btn = Button(text="로그인", size_hint_y=None, height=50)
        login_btn.bind(on_press=self.login)
        self.add_widget(login_btn)
        self.status_label = Label(text="", size_hint_y=None, height=30)
        self.add_widget(self.status_label)

    def login(self, instance):
        email = self.email_input.text
        password = self.password_input.text
        payload = {"email": email, "password": password}
        try:
            response = requests.post(API_LOGIN_URL, json=payload)
            if response.status_code == 200:
                self.status_label.text = "로그인 성공! 🎉"
            else:
                self.status_label.text = "로그인 실패 😢"
        except:
            self.status_label.text = "서버 오류!"

class NamusooLoginApp(App):
    def build(self):
        return LoginScreen()

if __name__ == "__main__":
    NamusooLoginApp().run()