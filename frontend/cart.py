from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import requests

API_CART_URL = "http://127.0.0.1:5000/cart_items"

class CartItem(BoxLayout):
    def __init__(self, name, price, quantity, **kwargs):
        super().__init__(orientation='horizontal', size_hint_y=None, height=50, padding=10, spacing=10, **kwargs)
        self.add_widget(Label(text=name, size_hint_x=0.5))
        self.add_widget(Label(text=f"{quantity}개", size_hint_x=0.25))
        self.add_widget(Label(text=f"{price * quantity}원", size_hint_x=0.25))

class CartScreen(BoxLayout):
    def __init__(self, user_id=1, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.add_widget(Label(text="🛒 내 장바구니", font_size=22, size_hint_y=None, height=50))
        scroll = ScrollView()
        grid = GridLayout(cols=1, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))
        try:
            res = requests.get(f"{API_CART_URL}?user_id={user_id}")
            if res.status_code == 200:
                cart_items = res.json()
                for item in cart_items:
                    grid.add_widget(CartItem(
                        name=item['product_name'],
                        price=item['price'],
                        quantity=item['quantity']
                    ))
            else:
                grid.add_widget(Label(text="장바구니를 불러올 수 없습니다"))
        except:
            grid.add_widget(Label(text="서버 연결 오류"))
        scroll.add_widget(grid)
        self.add_widget(scroll)
        self.add_widget(Button(text="👉 결제하러 가기", size_hint_y=None, height=50))

class NamusooCartApp(App):
    def build(self):
        return CartScreen(user_id=1)

if __name__ == '__main__':
    NamusooCartApp().run()