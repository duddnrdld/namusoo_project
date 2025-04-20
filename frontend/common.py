# common.py
from kivy.core.window import Window
from kivy.core.text import LabelBase

# 1) 윈도우 배경색: 연한 크림
Window.clearcolor = (1, 0.96, 0.92, 1)

# 2) 한글폰트 등록 (fonts/안에 Pretendard-Regular.ttf 넣어둘 것)
LabelBase.register(name='MyFont', fn_regular='fonts/Pretendard-Regular.ttf')

# 3) 서버 베이스 URL (배포된 주소로 변경)
BASE_URL = "https://namusoo-render-backend.onrender.com"
