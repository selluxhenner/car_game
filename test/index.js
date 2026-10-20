var comBlock, borderLeft, borderRight;
var comBlocks = [];

let xAx = 0
let speed = 20
let acc = 1
const maxAcc = 300
const accStep = 0.2
const deAccStep = 0.1
let accConstant = 0.01
let setInternal = 20
let showSpeed

document.addEventListener('DOMContentLoaded', () => {
  showSpeed = document.getElementById('test')
})

document.addEventListener('keydown', (event) => {
  if (event.key === 'a') {
    if (xAx > -100) {
      xAx -= 2
    }

    updateAll();
  } else if (event.key === 'd') {
    if (xAx < 100) {
      xAx += 2
    }

    updateAll();
  } else if (event.key === 'e') {
    gameArea.clear()
  } else if (event.key === 'w') {
    if (acc < maxAcc) {
      acc += accStep * accConstant

      speed += acc * accConstant
    
      acc += accStep * acc * accConstant

      if (accConstant < 0.1) {
        accConstant += 0.1
        console.log('accConstant', accConstant)
      }
    }

    showSpeed.innerHTML = acc
    updateAll();
  } else if (event.key === 's') {
    if (acc > 1) {
      acc -= deAccStep * acc * accConstant
    }

    showSpeed.innerHTML = acc

    updateAll();
  }
})

document.addEventListener('keyup', function(event) {
  if (event.key !== 'w') {
    if (accConstant > 0) {
      accConstant -= 0.05
      console.log(accConstant)
    }
  }
})

function startGame() {
  comBlock = new component(30, 30, "red", 450, 500);
  borderLeft = new component(10, 900, 'black', 300, 0);
  borderRight = new component(10, 900, 'black', 600, 0);
  gameArea.start();
}

var gameArea = {
  canvas: document.createElement("canvas"),
  frameNo: 0,
  start: function () {
    this.canvas.width = 1000;
    this.canvas.height = 900;
    this.context = this.canvas.getContext("2d");
    var screenElement = document.querySelector('.screen');
    screenElement.insertBefore(this.canvas, screenElement.firstChild);
    this.interval = setInterval(updateGameArea, 60); //15);
  },
  clear: function () {
    this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }
}


function component(width, height, color, x, y) {
  this.width = width;
  this.height = height;
  this.x = x;
  this.y = y;
  this.update = function () {
    ctx = gameArea.context;
    ctx.fillStyle = color;
    ctx.fillRect(this.x, this.y, this.width, this.height)
  }
}

speed = acc + 50
let loopStarted = false;
function updateGameArea() {
  for (let i = 0; i < comBlocks.length; i++) {
    comBlocks[i].y += speed / 10;
    comBlocks[i].x = 450 + xAx;
  }

  setInternal = 1600 * speed / 100; //200 - 800

  console.log(setInternal, acc, speed);


  updateAll()
  gameArea.frameNo += 1;

  if (!loopStarted) { // Check if the loop hasn't started yet
    loopStarted = true; // Set the flag to indicate the loop has started
    loopSpawn(); // Start the loop initially
  }
}


function loopSpawn() {
  setTimeout(() => {
    comBlocks.push(new component(6, setInternal / 20, 'green', 450 + xAx, 0));
    if (comBlocks.length > 60) {
      comBlocks.shift();
    }
    console.log(comBlocks);
    loopSpawn()
  }, (setInternal))
  console.log(comBlocks)
}

loopSpawn()

function updateAll() {
  gameArea.clear();

  borderLeft.x = 300 + xAx
  borderRight.x = 600 + xAx


  for (let i = 0; i < comBlocks.length; i++) {
    comBlocks[i].update();
  }

  borderLeft.update();
  borderRight.update();
  comBlock.update();
}
