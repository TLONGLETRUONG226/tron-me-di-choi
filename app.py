import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trốn Mẹ Đi Chơi 3D", page_icon="🏃", layout="centered")

st.markdown("""
    <h2 style='text-align: center; color: #ff4b4b;'>🏃 TRỐN MẸ ĐI CHƠI - 3D STREET RUNNER 🚗</h2>
    <p style='text-align: center; color: #555;'>Dùng phím <b>A / D</b> hoặc <b>Mũi tên Trái / Phải</b> để né chướng ngại vật. Đừng để xe mẹ tông trúng!</p>
""", unsafe_allow_html=True)

# Sử dụng hình ảnh nền đường phố chất lượng cao thay thế trực tiếp, loại bỏ hoàn toàn lỗi "Image not found"
bg_image_url = "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1200&q=80"

# Mã nguồn Game 3D phong cách Street Perspective
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
            background-color: #0e1117;
            font-family: 'Courier New', Courier, monospace;
        }}
        #gameContainer {{
            position: relative;
            width: 700px;
            height: 450px;
            border: 4px solid #333;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.6);
            background-image: url('{bg_image_url}');
            background-size: cover;
            background-position: center;
        }}
        /* Lớp phủ làm tối nhẹ nền để làm nổi bật đường chạy */
        #gameContainer::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.45);
            z-index: 1;
        }}
        canvas {{
            position: absolute;
            top: 0;
            left: 0;
            z-index: 2;
        }}
        #uiOverlay {{
            position: absolute;
            top: 15px;
            left: 15px;
            font-size: 16px;
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
            background: rgba(0, 0, 0, 0.85);
            display: none;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 20;
            color: white;
        }}
        button {{
            padding: 12px 25px;
            font-size: 16px;
            font-weight: bold;
            background-color: #ff4b4b;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            margin-top: 15px;
            box-shadow: 0 4px 10px rgba(255, 75, 75, 0.4);
            transition: 0.2s;
        }}
        button:hover {{
            background-color: #ff2b2b;
            transform: scale(1.05);
        }}
    </style>
</head>
<body>

<div id="gameContainer">
    <div id="uiOverlay">
        <div>🏁 Về đích: <span id="distanceText">150</span>m</div>
        <div>⚠️ Khoảng cách mẹ đuổi: <span id="momDistanceText" style="color: #ff4b4b;">30</span>m</div>
    </div>

    <div id="gameOverOverlay">
        <h2 id="gameResultTitle" style="margin: 0; font-size: 32px;">GAME OVER</h2>
        <p id="gameResultDesc" style="margin-top: 10px; font-size: 16px; text-align: center; padding: 0 20px;"></p>
        <button onclick="resetGame()">Chơi Lại 🔄</button>
    </div>

    <canvas id="gameCanvas" width="700" height="450"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let distance = 150; 
let momDistance = 25; 
let gameOver = false;
let gameWon = false;
let gameSpeed = 4;

const lanes = [240, 350, 460]; 
let playerLaneIndex = 1; 

let player = {{
    x: lanes[playerLaneIndex],
    y: 380,
    width: 35,
    height: 50
}};

let obstacles = [];
let keys = {{}};

document.addEventListener('keydown', (e) => {{
    keys[e.key] = true;
    if ((e.key === 'ArrowLeft' || e.key === 'a' || e.key === 'A') && playerLaneIndex > 0) {{
        playerLaneIndex--;
    }}
    if ((e.key === 'ArrowRight' || e.key === 'd' || e.key === 'D') && playerLaneIndex < lanes.length - 1) {{
        playerLaneIndex++;
    }}
}});
document.addEventListener('keyup', (e) => keys[e.key] = false);

function spawnObstacle() {{
    const randomLane = Math.floor(Math.random() * lanes.length);
    const types = ['🚧', '📦', '🕳️'];
    const chosenType = types[Math.floor(Math.random() * types.length)];
    
    obstacles.push({{
        lane: randomLane,
        z: 0.1, 
        type: chosenType
    }});
}}

let obstacleTimer = 0;

function update() {{
    if (gameOver || gameWon) return;

    let targetX = lanes[playerLaneIndex];
    player.x += (targetX - player.x) * 0.2;

    distance -= 0.04;
    if (distance <= 0) {{
        distance = 0;
        gameWon = true;
        endGame(true);
    }}

    obstacleTimer++;
    if (obstacleTimer > 45) {{
        spawnObstacle();
        obstacleTimer = 0;
    }}

    for (let i = 0; i < obstacles.length; i++) {{
        let obs = obstacles[i];
        obs.z += 0.018 * (gameSpeed / 3);

        if (obs.z > 0.75 && obs.z < 0.95 && obs.lane === playerLaneIndex) {{
            momDistance -= 7;
            obstacles.splice(i, 1);
            i--;
            if (momDistance <= 0) {{
                momDistance = 0;
                gameOver = true;
                endGame(false);
            }}
            continue;
        }}

        if (obs.z > 1.2) {{
            obstacles.splice(i, 1);
            i--;
        }}
    }}

    document.getElementById('distanceText').innerText = Math.ceil(distance);
    document.getElementById('momDistanceText').innerText = Math.ceil(momDistance);
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "rgba(255, 255, 0, 0.6)";
    ctx.lineWidth = 3;
    
    ctx.beginPath();
    ctx.moveTo(350, 200); ctx.lineTo(100, 450);
    ctx.moveTo(350, 200); ctx.lineTo(600, 450);
    ctx.stroke();

    ctx.strokeStyle = "rgba(255, 255, 255, 0.4)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(350, 200); ctx.lineTo(275, 450);
    ctx.moveTo(350, 200); ctx.lineTo(425, 450);
    ctx.stroke();

    obstacles.sort((a, b) => a.z - b.z);

    obstacles.forEach(obs => {{
        let screenY = 200 + obs.z * 250;
        let baseLaneX = lanes[obs.lane];
        let screenX = 350 + (baseLaneX - 350) * obs.z;
        let size = Math.max(15, obs.z * 55);

        ctx.font = `${{size}}px Arial`;
        ctx.textAlign = "center";
        ctx.fillText(obs.type, screenX, screenY);
    }});

    ctx.font = "42px Arial";
    ctx.textAlign = "center";
    ctx.fillText("🏃", player.x, player.y);

    ctx.font = "38px Arial";
    let momVisualX = player.x + Math.sin(Date.now() / 150) * 5; 
    ctx.fillText("🚘", momVisualX, 435);
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
        title.innerText = "🎉 THOÁT THÀNH CÔNG!";
        title.style.color = "#4CAF50";
        desc.innerText = "Tuyệt vời! Bạn đã về đích an toàn trước khi bị mẹ tóm gọn!";
    }} else {{
        title.innerText = "💥 XE CỦA MẸ ĐÃ BẮT KỊP!";
        title.style.color = "#FF5252";
        desc.innerText = "Bùm! Bạn va phải quá nhiều chướng ngại vật nên đã bị mẹ lái xe đuổi kịp!";
    }}
}}

function resetGame() {{
    distance = 150;
    momDistance = 25;
    gameOver = false;
    gameWon = false;
    obstacles = [];
    playerLaneIndex = 1;
    player.x = lanes[playerLaneIndex];
    document.getElementById('gameOverOverlay').style.display = 'none';
    requestAnimationFrame(loop);
}}

requestAnimationFrame(loop);
</script>
</body>
</html>
"""

components.html(game_html, height=480)
