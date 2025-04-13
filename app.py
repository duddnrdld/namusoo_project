from flask import Flask, request, send_from_directory
from datetime import date
import random

app = Flask(__name__)

@app.route("/image.png")
def serve_image():
    return send_from_directory(".", "image.png")

@app.route("/", methods=["GET", "POST", "HEAD"])
def home():
    if request.method == "HEAD":
        return '', 200

    today = str(date.today())
    user_data = '''
    <script>
        const saved = JSON.parse(localStorage.getItem("userData"));
        const lastDate = localStorage.getItem("lastFortuneDate");
        const hasVisited = localStorage.getItem("hasVisited") === "true";
        if (saved && hasVisited) {{
            if (lastDate === "{today}") {{
                location.href = "/result?repeat=true";
            }} else {{
                location.href = "/result";
            }}
        }}
    </script>
    '''.replace("{today}", today)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>복토리 운세입력</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; font-family: 'Poor Story', 'Jua', sans-serif; background: #fff7ed; height: 100vh; position: relative; }}
            .fixed-header {{ position: fixed; top: 20px; width: 100%; text-align: center; font-size: 28px; font-weight: bold; z-index: 20; color: #333; }}
            .form-box {{ background: rgba(255,255,255,0.95); padding: 40px 30px; border-radius: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; width: 90%; max-width: 400px; z-index: 10; position: relative; top: 80px; margin: 0 auto; }}
            input, select, button {{ width: 100%; padding: 12px; margin-top: 12px; font-size: 16px; border-radius: 20px; border: none; }}
            button {{ background-color: #ff9caa; color: white; font-weight: bold; cursor: pointer; }}
            .rotating-floating {{ position: absolute; width: 60px; opacity: 0.8; pointer-events: none; animation: floatRotate linear infinite; }}
            @keyframes floatRotate {{ 0% {{ transform: translateY(100vh) rotate(0deg); }} 100% {{ transform: translateY(-150px) rotate(360deg); }} }}
        </style>
    </head>
    <body>
        <div class="fixed-header">복토리</div>
        <div class="form-box">
            <form method="post">
                <input name="name" id="name" placeholder="이름 입력">
                <input type="date" name="birth" id="birth">
                <select name="calendar" id="calendar">
                    <option>양력</option><option>음력</option>
                </select>
                <select name="gender" id="gender">
                    <option>여성</option><option>남성</option>
                </select>
                <button type="submit">입력 완료</button>
            </form>
        </div>
        <script>
            for (let i = 0; i < 30; i++) {{
                const img = document.createElement("img");
                img.src = "/image.png";
                img.className = "rotating-floating";
                img.style.left = Math.random() * 100 + "%";
                img.style.zIndex = 1;
                img.style.animationDuration = (15 + Math.random() * 15) + "s";
                img.style.animationDelay = Math.random() * 10 + "s";
                document.body.appendChild(img);
            }}
            {user_data}
        </script>
    </body>
    </html>
    '''

@app.route("/result")
def result():
    import urllib.parse
    repeat = request.args.get("repeat") == "true"
    script = """
        const saved = JSON.parse(localStorage.getItem("userData"));
        const today = new Date().toISOString().split('T')[0];
        let score;
        if (saved && localStorage.getItem("lastFortuneDate") === today) {{
            score = saved.score;
        }} else {{
            score = Math.floor(Math.random() * 100) + 1;
            saved.score = score;
            localStorage.setItem("userData", JSON.stringify(saved));
            localStorage.setItem("lastFortuneDate", today);
        }}
        let msg = "";
        if (score <= 20) msg = "오늘은 조심이 필요한 날이에요. 무리한 계획보다는 쉬엄쉬엄, 스스로를 돌보는 하루로 만들어봐요.";
        else if (score <= 50) msg = "평범한 하루가 펼쳐질 거예요. 작은 기쁨이나 우연한 행운이 찾아올지도 몰라요! 마음의 여유를 가져보세요.";
        else if (score <= 80) msg = "오늘은 좋은 기운이 가득해요! 새로운 시도를 하거나 중요한 결정을 내리기 딱 좋은 날이에요. 당신을 응원할게요.";
        else msg = "행운이 쏟아지는 날이에요! 하는 일마다 술술 풀리고, 좋은 소식이 들릴 수 있어요. 주위 사람들과 행복을 나눠보는 것도 좋겠어요.";
        document.getElementById("name").innerText = saved.name;
        document.getElementById("score").innerText = score + "점";
        document.getElementById("msg").innerText = msg;
    """

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>오늘의 운세</title>
        <link href="https://fonts.googleapis.com/css2?family=Jua&family=Poor+Story&display=swap" rel="stylesheet">
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; font-family: 'Poor Story', 'Jua', sans-serif; background: #fff7ed; height: 100vh; position: relative; }}
            .fixed-header {{ position: fixed; top: 20px; width: 100%; text-align: center; font-size: 28px; font-weight: bold; z-index: 20; color: #333; }}
            .fortune-box {{ background: rgba(255,255,255,0.95); padding: 40px 30px; border-radius: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); text-align: center; width: 90%; max-width: 400px; z-index: 10; position: relative; top: 100px; margin: 0 auto; }}
            .fortune-box h2 {{ font-size: 20px; color: #999; margin-bottom: 10px; }}
            .fortune-box h3 {{ font-size: 24px; color: #aa5c5c; margin-bottom: 12px; }}
            .fortune-box p {{ font-size: 20px; color: #5c5c5c; margin: 10px 0; line-height: 1.6; }}
            .rotating-floating {{ position: absolute; width: 60px; opacity: 0.8; pointer-events: none; animation: floatRotate linear infinite; }}
            @keyframes floatRotate {{ 0% {{ transform: translateY(100vh) rotate(0deg); }} 100% {{ transform: translateY(-150px) rotate(360deg); }} }}
        </style>
    </head>
    <body>
        <div class="fixed-header">복토리</div>
        <div class="fortune-box">
            <h2>오늘의 운세는 어떨까요?</h2>
            <h3>✨ <span id="name"></span>님의 운세 ✨</h3>
            <p id="score"></p>
            <p id="msg"></p>
        </div>
        <script>
            {script}
            for (let i = 0; i < 30; i++) {{
                const img = document.createElement("img");
                img.src = "/image.png";
                img.className = "rotating-floating";
                img.style.left = Math.random() * 100 + "%";
                img.style.zIndex = 1;
                img.style.animationDuration = (15 + Math.random() * 15) + "s";
                img.style.animationDelay = Math.random() * 10 + "s";
                document.body.appendChild(img);
            }}
        </script>
    </body>
    </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
