import streamlit as st
import streamlit.components.v1 as components
import base64

st.set_page_config(page_title="Trốn Mẹ Đi Chơi", page_icon="🏃", layout="centered")

st.title("🏃 Trốn Mẹ Đi Chơi!")
st.caption("Hãy giúp chàng trai né các chướng ngại vật trên đường phố và chạy thoát khỏi xe của mẹ!")

# Đọc ảnh nền IMG_0299.jpg để chuyển thành chuỗi mã hóa Base64 cho HTML
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

try:
    # Đảm bảo file IMG_0299.jpg nằm cùng thư mục với app.py
    bg_base64 = get_base64_of_bin_file('IMG_0299.jpg')
    bg_image_data = f"data:image/jpeg;base64,{bg_base64}"
except Exception:
    # Nếu chưa có file ảnh thực tế, sử dụng ảnh mẫu/placeholder
    bg_image_data = "https://i.postimg.cc/mD8zS5Q9/IMG-0299.jpg"

# Mã nguồn Game bằng HTML5 / JavaScript
game_html = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            background-color: #1e1e1e;
            font-family: Arial, sans-serif;
            color: white;
        }}
        #gameContainer {{
            position: relative;
            width: 600px;
            height: 400px;
            border: 3px solid #fff;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            background-image: url('{bg_image_data}');
            background-size: cover;
            background-position: center;
        }}
        canvas {{
            position: absolute;
            top: 0;
            left: 0;
        }}
        #uiOverlay {{
            position: absolute;
            top: 10px;
            left: 10px;
            font-size: 18px;
            font-weight: bold;
            color: #fff;
            text-shadow: 2px 2px 4px #000;
            z-index: 10;
        }}
        #gameOverOverlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.75);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 20;
        }}
        button {{
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 15px;
        }}
        button:hover {{
            background-color: #ff2b2b;
        }}
    </style>
</head>
<body>

<div id="gameContainer">
    <div id="uiOverlay">
        <div>📍 Quãng đường còn lại: <span id="distanceText">100</span>m</div>
        <div>🚗 Khoảng cách mẹ rượt: <span id="momDistanceText">30</span>m</div>
    </div>

    <div id="gameOverOverlay">
        <h2 id="gameResultTitle" style="margin: 0; font-size: 28px;">GAME OVER</h2>
        <p id="gameResultDesc" style="margin-top: 10px; font-size: 16px;"></p>
        <button onclick="resetGame()">Chơi Lại 🔄</button>
    </div>

    <canvas id="gameCanvas" width="600" height="400"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let distance = 100; // Quãng đường cần vượt qua (mét)
let momDistance = 25; // Khoảng cách xe mẹ phía sau
let gameOver = false;
let gameWon = false;

// Nhân vật chàng trai
const player = {{
    x: 280,
    y: 300,
    width: 30,
    height: 40,
    speed: 5
}};

// Xe của mẹ (đi phía sau)
const momCar = {{
    x: 270,
    y: 360,
    width: 50,
    height: 30
}};

// Danh sách chướng ngại vật (Thùng rác, Nắp cống, Rào chắn)
let obstacles = [];
let keys = {{}};

document.addEventListener('keydown', (e) => keys[e.key] = true);
document.addEventListener('keyup', (e) => keys[e.key] = false);

function spawnObstacle() {{
    const laneX = [150, 280, 410]; // 3 làn đường
    const randomX = laneX[Math.floor(Math.random() * laneX.length)];
    obstacles.push({{
        x: randomX,
        y: -40,
        width: 40,
        height: 30,
        speed: 4,
        type: Math.random() > 0.5 ? '📦' : '🚧'
    }});
}}

let obstacleTimer = 0;

function update() {{
    if (gameOver || gameWon) return;

    // Điều khiển chàng trai
    if ((keys['ArrowLeft'] || keys['a']) && player.x > 100) player.x -= player.speed;
    if ((keys['ArrowRight'] || keys['d']) && player.x < 470) player.x += player.speed;
    if ((keys['ArrowUp'] || keys['w']) && player.y > 100) player.y -= player.speed;
    if ((keys['ArrowDown'] || keys['s']) && player.y < 320) player.y += player.speed;

    // Giảm dần quãng đường về đích
    distance -= 0.05;
    if (distance <= 0) {{
        distance = 0;
        gameWon = true;
        endGame(true);
    }}

    // Sinh chướng ngại vật
    obstacleTimer++;
    if (obstacleTimer > 40) {{
        spawnObstacle();
        obstacleTimer = 0;
    }}

    // Cập nhật chướng ngại vật
    for (let i = 0; i < obstacles.length; i++) {{
        let obs = obstacles[i];
        obs.y += obs.speed;

        // Va chạm giữa Chàng trai và Chướng ngại vật
        if (player.x < obs.x + obs.width &&
            player.x + player.width > obs.x &&
            player.y < obs.y + obs.height &&
            player.y + player.height > obs.y) {{
            
            // Tông phải chướng ngại vật -> Bị làm chậm & Mẹ tiến lại gần!
            momDistance -= 8;
            obstacles.splice(i, 1);
            i--;
            continue;
        }}

        // Xóa chướng ngại vật ra khỏi màn hình
        if (obs.y > canvas.height) {{
            obstacles.splice(i, 1);
            i--;
        }}
    }}

    // Kiểm tra xe mẹ bắt kịp
    if (momDistance <= 0) {{
        gameOver = true;
        endGame(false);
    }}

    // Cập nhật UI
    document.getElementById('distanceText').innerText = Math.ceil(distance);
    document.getElementById('momDistanceText').innerText = Math.ceil(momDistance);
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Vẽ làn đường giả định
    ctx.strokeStyle = "rgba(255, 255, 255, 0.3)";
    ctx.setLineDash([20, 15]);
    ctx.beginPath();
    ctx.moveTo(220, 0); ctx.lineTo(220, 400);
    ctx.moveTo(370, 0); ctx.lineTo(370, 400);
    ctx.stroke();

    // Vẽ chàng trai 🏃
    ctx.font = "32px Arial";
    ctx.fillText("🏃", player.x, player.y + 30);

    // Vẽ xe của Mẹ 🚘
    ctx.fillText("🚘", player.x - 10, player.y + momDistance * 4);

    // Vẽ các chướng ngại vật
    obstacles.forEach(obs => {{
        ctx.font = "28px Arial";
        ctx.fillText(obs.type, obs.x, obs.y + 25);
    }});
}}

function loop() {{
    update();
    draw();
    if (!gameOver && !gameWon) {{
        requestAnimationFrame(loop);
    }}
}}

function endGame(isWin) {{
    const overlay = document.getElementById('gameOverOverlay');
    const title = document.getElementById('gameResultTitle');
    const desc = document.getElementById('gameResultDesc');
    overlay.style.display = 'flex';

    if (isWin) {{
        title.innerText = "🎉 BẠN ĐÃ THOÁT!";
        title.style.color = "#4CAF50";
        desc.innerText = "Chàng trai đã về đích an toàn và đi chơi cùng bạn bè!";
    }} else {{
        title.innerText = "💥 MẸ ĐÃ BẮT ĐƯỢC!";
        title.style.color = "#FF5252";
        desc.innerText = "Mẹ đã lái xe đuổi kịp và bắt bạn về nhà học bài!";
    }}
}}

function resetGame() {{
    distance = 100;
    momDistance = 25;
    gameOver = false;
    gameWon = false;
    obstacles = [];
    player.x = 280;
    player.y = 200;
    document.getElementById('gameOverOverlay').style.display = 'none';
    requestAnimationFrame(loop);
}}

requestAnimationFrame(loop);
</script>
</body>
</html>
"""

# Hiển thị game vào Streamlit
components.html(game_html, height=430)

st.subheader("🎮 Hướng dẫn điều khiển:")
st.markdown("""
- Sử dụng các phím **A / D** hoặc **Phím mũi tên Trái / Phải** để di chuyển tránh né chướng ngại vật (📦, 🚧).
- Sử dụng phím **W / S** hoặc **Mũi tên Lên / Xuống** để tăng tốc hoặc giảm tốc.
- Về đích (0m) trước khi xe Mẹ (🚘) phía sau bắt kịp bạn!
""")
