const canvas = document.getElementById('game');
const ctx = canvas.getContext('2d');
const scoreEl = document.getElementById('score');
const highScoreEl = document.getElementById('highScore');
const overlay = document.getElementById('overlay');
const startBtn = document.getElementById('startBtn');

const GRID = 20, CELL = canvas.width / GRID;

let snake, food, dir, nextDir, score, highScore, running, gameOver, interval;

function initGame() {
  snake = [{x: 10, y: 10}, {x: 9, y: 10}, {x: 8, y: 10}];
  dir = {x: 1, y: 0};
  nextDir = {x: 1, y: 0};
  score = 0;
  gameOver = false;
  scoreEl.textContent = '0';
  spawnFood();
}

function spawnFood() {
  const occupied = new Set(snake.map(s => `${s.x},${s.y}`));
  let pos;
  do {
    pos = {x: Math.floor(Math.random() * GRID), y: Math.floor(Math.random() * GRID)};
  } while (occupied.has(`${pos.x},${pos.y}`));
  food = pos;
}

function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  // Grid lines
  ctx.strokeStyle = 'rgba(255,255,255,.03)';
  ctx.lineWidth = 1;
  for (let i = 0; i <= GRID; i++) {
    ctx.beginPath(); ctx.moveTo(i * CELL, 0); ctx.lineTo(i * CELL, canvas.height); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i * CELL); ctx.lineTo(canvas.width, i * CELL); ctx.stroke();
  }

  // Food glow
  ctx.shadowColor = '#e94560';
  ctx.shadowBlur = 12;
  ctx.fillStyle = '#e94560';
  ctx.beginPath();
  ctx.arc(food.x * CELL + CELL/2, food.y * CELL + CELL/2, CELL/2 - 2, 0, Math.PI * 2);
  ctx.fill();
  ctx.shadowBlur = 0;

  // Snake body
  for (let i = 0; i < snake.length; i++) {
    const s = snake[i];
    const t = i / (snake.length - 1 || 1);
    const r = Math.round(30 + t * 25);
    const g = Math.round(180 + t * 40);
    const b = Math.round(100 - t * 30);
    ctx.fillStyle = `rgb(${r},${g},${b})`;

    const pad = i === 0 ? 2 : 3;
    const size = CELL - pad * 2;
    const x = s.x * CELL + pad;
    const y = s.y * CELL + pad;

    if (i === 0) {
      ctx.shadowColor = 'rgba(30,200,100,.3)';
      ctx.shadowBlur = 8;
      ctx.beginPath();
      ctx.roundRect(x, y, size, size, 4);
      ctx.fill();
      ctx.shadowBlur = 0;

      // Eyes
      ctx.fillStyle = '#fff';
      ctx.beginPath();
      ctx.arc(x + size * .35 - (dir.x || 0) * 2, y + size * .35 - (dir.y || 0) * 2, 3, 0, Math.PI * 2);
      ctx.arc(x + size * .65 - (dir.x || 0) * 2, y + size * .35 - (dir.y || 0) * 2, 3, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = '#1a1a2e';
      ctx.beginPath();
      ctx.arc(x + size * .35 - (dir.x || 0) * 3, y + size * .35 - (dir.y || 0) * 3, 1.5, 0, Math.PI * 2);
      ctx.arc(x + size * .65 - (dir.x || 0) * 3, y + size * .35 - (dir.y || 0) * 3, 1.5, 0, Math.PI * 2);
      ctx.fill();
    } else {
      ctx.beginPath();
      ctx.roundRect(x, y, size, size, 3);
      ctx.fill();
    }
  }
}

function step() {
  dir = {...nextDir};
  const head = {x: snake[0].x + dir.x, y: snake[0].y + dir.y};

  // Wall wrap
  if (head.x < 0) head.x = GRID - 1;
  if (head.x >= GRID) head.x = 0;
  if (head.y < 0) head.y = GRID - 1;
  if (head.y >= GRID) head.y = 0;

  // Self collision
  for (let i = 0; i < snake.length; i++) {
    if (snake[i].x === head.x && snake[i].y === head.y) {
      endGame();
      return;
    }
  }

  snake.unshift(head);

  if (head.x === food.x && head.y === food.y) {
    score += 10;
    scoreEl.textContent = score;
    if (score > highScore) {
      highScore = score;
      highScoreEl.textContent = highScore;
      try { localStorage.setItem('snakeHighScore', highScore); } catch(e) {}
    }
    spawnFood();
  } else {
    snake.pop();
  }

  draw();
}

function endGame() {
  gameOver = true;
  clearInterval(interval);
  document.getElementById('overlay').classList.add('show');
  document.querySelector('#overlay h2').textContent = '馃拃 娓告垙缁撴潫';
  document.querySelector('.final-score')?.remove();
  const fs = document.createElement('div');
  fs.className = 'final-score';
  fs.textContent = score;
  document.querySelector('#overlay h2').insertAdjacentElement('afterend', fs);
  const p = document.querySelector('#overlay p');
  p.textContent = score >= highScore && score > 0 ? '馃弳 鏂扮邯褰曪紒' : '鍐嶈瘯涓€娆★紵';
  startBtn.textContent = '閲嶆柊寮€濮?;
}

function startGame() {
  highScore = parseInt(localStorage.getItem('snakeHighScore') || '0', 10);
  highScoreEl.textContent = highScore;
  overlay.classList.remove('show');
  initGame();
  draw();
  if (interval) clearInterval(interval);
  interval = setInterval(step, 120);
}

// Events
document.addEventListener('keydown', e => {
  const key = e.key;
  if (['ArrowUp','ArrowDown','ArrowLeft','ArrowRight','w','W','s','S','a','A','d','D'].includes(key)) e.preventDefault();

  if (gameOver || !running) return;

  let nd = null;
  if (key === 'ArrowUp' || key === 'w' || key === 'W') nd = {x: 0, y: -1};
  if (key === 'ArrowDown' || key === 's' || key === 'S') nd = {x: 0, y: 1};
  if (key === 'ArrowLeft' || key === 'a' || key === 'A') nd = {x: -1, y: 0};
  if (key === 'ArrowRight' || key === 'd' || key === 'D') nd = {x: 1, y: 0};
  if (key === ' ') { if (!gameOver) startGame(); return; }

  if (nd && (nd.x !== -dir.x || nd.y !== -dir.y)) {
    nextDir = nd;
  }
});

startBtn.addEventListener('click', () => {
  running = true;
  startGame();
});

// Init display
highScore = parseInt(localStorage.getItem('snakeHighScore') || '0', 10);
highScoreEl.textContent = highScore;
initGame();
draw();
