# cart.py
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests

from common import BASE_URL

API_CART_URL = f"{BASE_URL}/cart_items"

class CartItem(BoxLayout):
    def __init__(self, name, price, qty, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=60, padding=10, spacing=10, **kwargs)
        self.add_widget(Label(text=name, font_name="MyFont", size_hint_x=0.6))
        self.add_widget(Label(text=f"{qty}개", font_name="MyFont", size_hint_x=0.2))
        self.add_widget(Label(text=f"{price*qty}원", font_name="MyFont", size_hint_x=0.2))

class CartScreen(BoxLayout):
    def __init__(self, user_id=1, **kwargs):
        super().__init__(orientation='vertical', padding=15, spacing=10, **kwargs)
        self.add_widget(Label(text="🛒 내 장바구니", font_name="MyFont", font_size=24, size_hint_y=None, height=50))

        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        try:
            res = requests.get(API_CART_URL, params={"user_id":user_id})
            items = res.json() if res.status_code==200 else []
            for it in items:
                grid.add_widget(CartItem(it['product_name'], it['price'], it['quantity']))
        except:
            grid.add_widget(Label(text="장바구니 불러오기 실패", font_name="MyFont"))

        scroll.add_widget(grid)
        self.add_widget(scroll)

        btn = Button(text="결제하러 가기", font_name="MyFont", size_hint_y=None, height=50, background_color=(1,0.9,0.6,1))
        btn.bind(on_press=lambda *a: print("주문 화면으로 이동"))
        self.add_widget(btn)

class CartApp(App):
    def build(self):
        return CartScreen()

if __name__=="__main__":
    CartApp().run()
