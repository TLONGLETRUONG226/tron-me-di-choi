import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Trốn Mẹ Đi Chơi - 3D Minecraft Street", page_icon="🏃", layout="centered")

st.markdown("""
    <h2 style='text-align: center; color: #ff4b4b; text-shadow: 1px 1px 2px black;'>🏃 TRỐN MẸ ĐI CHƠI - 3D MINECRAFT RUNNER 🚗</h2>
    <p style='text-align: center; color: #333; font-weight: bold;'>Sử dụng phím <b>A / D</b> hoặc <b>Mũi tên Trái / Phải</b> để né chướng ngại vật!</p>
""", unsafe_allow_html=True)

# Sử dụng trực tiếp ảnh nền phong cách Minecraft khối hộp chất lượng cao trùng khớp với cảnh quan bạn cung cấp
bg_image_url = "https://images.unsplash.com/photo-1627856013091-fed6e4e304ca?auto=format&fit=crop&w=1200&q=80"

# Mã nguồn Game 3D chân thực trên nền Minecraft
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
            background-color: #1a1a1a;
            font-family: 'Courier New', Courier, monospace;
        }}
        #gameContainer {{
            position: relative;
            width: 750px;
            height: 480px;
            border: 4px solid #222;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 12px 30px rgba(0,0,0,0.7);
            background-image: url('{bg_image_url}');
            background-size: cover;
            background-position: center;
        }}
        /* Lớp phủ tinh chỉnh ánh sáng để hòa hợp cảnh nền và không gian 3D */
        #gameContainer::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background: linear-gradient(to bottom, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.5) 100%);
            z-index: 1;
            pointer-events: none;
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
            left: 20px;
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
            box-shadow: 0 4px 10px rgba(255, 75, 75, 0.5);
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
        <div>🏁 Khoảng cách về đích: <span id="distanceText">150</span>m</div>
        <div>⚠️ Khoảng cách xe mẹ đuổi: <span id="momDistanceText" style="color: #ff4b4b;">30</span>m</div>
    </div>

    <div id="gameOverOverlay">
        <h2 id="gameResultTitle" style="margin: 0; font-size: 32px;">GAME OVER</h2>
        <p id="gameResultDesc" style="margin-top: 10px; font-size: 16px; text-align: center; padding: 0 20px;"></p>
        <button onclick="resetGame()">Chơi Lại 🔄</button>
    </div>

    <canvas id="gameCanvas" width="750" height="480"></canvas>
</div>

<script>
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let distance = 150; 
let momDistance = 25; 
let gameOver = false;
let gameWon = false;
let gameSpeed = 4.5;

// Thiết lập 3 làn đường 3D có chiều sâu phối cảnh
const lanes = [260, 375, 490]; 
let playerLaneIndex = 1; 

let player = {{
    x: lanes[playerLaneIndex],
    y: 400,
    width: 45,
    height: 60
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
        z: 0.05, 
        type: chosenType
    }});
}

let obstacleTimer = 0;

function update() {{
    if (gameOver || gameWon) return;

    let targetX = lanes[playerLaneIndex];
    player.x += (targetX - player.x) * 0.25;

    distance -= 0.04;
    if (distance <= 0) {{
        distance = 0;
        gameWon = true;
        endGame(true);
    }}

    obstacleTimer++;
    if (obstacleTimer > 40) {{
        spawnObstacle();
        obstacleTimer = 0;
    }}

    for (let i = 0; i < obstacles.length; i++) {{
        let obs = obstacles[i];
        obs.z += 0.02 * (gameSpeed / 3.5);

        if (obs.z > 0.78 && obs.z < 0.95 && obs.lane === playerLaneIndex) {{
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

        if (obs.z > 1.25) {{
            obstacles.splice(i, 1);
            i--;
        }}
    }}

    document.getElementById('distanceText').innerText = Math.ceil(distance);
    document.getElementById('momDistanceText').innerText = Math.ceil(momDistance);
}}

function draw() {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.strokeStyle = "rgba(255, 235, 59, 0.7)";
    ctx.lineWidth = 4;
    
    let horizonX = 375;
    let horizonY = 220;

    ctx.beginPath();
    ctx.moveTo(horizonX, horizonY); ctx.lineTo(80, 480);
    ctx.moveTo(horizonX, horizonY); ctx.lineTo(670, 480);
    ctx.stroke();

    ctx.strokeStyle = "rgba(255, 255, 255, 0.5)";
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(horizonX, horizonY); ctx.lineTo(300, 480);
    ctx.moveTo(horizonX, horizonY); ctx.lineTo(450, 480);
    ctx.stroke();

    obstacles.sort((a, b) => a.z - b.z);

    obstacles.forEach(obs => {{
        let screenY = horizonY + obs.z * 260;
        let baseLaneX = lanes[obs.lane];
        let screenX = horizonX + (baseLaneX - horizonX) * obs.z;
        let size =
