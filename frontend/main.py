import os
# Disable Windows pen/touch providers
os.environ["KIVY_NO_INPUT"] = "wm_pen,wm_touch"
os.environ["KIVY_WINDOW"] = "sdl2"

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from kivy.core.text import LabelBase
import requests

# UI settings
Window.clearcolor = (1, 0.96, 0.92, 1)
# Windows 테스트용 한글폰트 등록 (맑은 고딕)
LabelBase.register(
    name="MyFont",
    fn_regular="C:/Windows/Fonts/malgun.ttf"
)
BASE_URL = "https://namusoo-render-backend.onrender.com"

class LoginScreen(Screen):
    def do_login(self):
        e = self.ids.email.text
        p = self.ids.password.text
        try:
            r = requests.post(f"{BASE_URL}/login", json={"email": e, "password": p})
            if r.status_code == 200:
                self.manager.current = "cart"
            else:
                self.ids.status.text = "로그인 실패"
        except:
            self.ids.status.text = "서버 오류"
    def go_signup(self):
        self.manager.current = "signup"

class SignupScreen(Screen):
    def do_signup(self):
        e = self.ids.email.text
        p1 = self.ids.pw1.text
        p2 = self.ids.pw2.text
        if p1 != p2:
            self.ids.status.text = "비밀번호 불일치"
            return
        try:
            r = requests.post(f"{BASE_URL}/signup", json={"email": e, "password": p1})
            if r.status_code == 201:
                self.manager.current = "login"
            else:
                self.ids.status.text = "가입 실패"
        except:
            self.ids.status.text = "서버 오류"

class CartScreen(Screen):
    pass

class OrderScreen(Screen):
    pass

class AdminScreen(Screen):
    pass

class NamusooApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(SignupScreen(name="signup"))
        sm.add_widget(CartScreen(name="cart"))
        sm.add_widget(OrderScreen(name="order"))
        sm.add_widget(AdminScreen(name="admin"))
        return sm

if __name__ == "__main__":
    NamusooApp().run()