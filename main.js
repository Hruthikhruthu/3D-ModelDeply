import * as THREE from "https://unpkg.com/three/build/three.module.js";
import { OrbitControls } from "https://unpkg.com/three/examples/jsm/controls/OrbitControls.js";

// DOM
const container = document.getElementById("scene-container");
const selector = document.getElementById("timeSelector");

// THREE.js Setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x111111);

const camera = new THREE.PerspectiveCamera(
  60,
  container.clientWidth / container.clientHeight,
  0.1,
  1000
);
camera.position.set(10, 10, 20);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Lights
const light = new THREE.PointLight(0xffffff, 2);
light.position.set(20, 20, 20);
scene.add(light);

// Data Variables
let config = {};
let sensors = [];
let readings = [];
let bars = [];

// Load Data
async function loadData() {
  config = await (await fetch("/config")).json();
  sensors = await (await fetch("/sensors")).json();
  readings = await (await fetch("/readings")).json();

  setupTimeSelector();
}

function setupTimeSelector() {
  readings.forEach((r, i) => {
    const option = document.createElement("option");
    option.value = i;
    option.textContent = r.timestamp;
    selector.appendChild(option);
  });

  selector.onchange = () => drawBars(readings[selector.value].values);

  drawBars(readings[0].values);
}

// Draw Bars
function drawBars(values) {
  bars.forEach(b => scene.remove(b));
  bars = [];

  let x = -5;

  sensors.forEach(sensor => {
    const val = values[sensor.id];
    const height = val / 10;

    const geom = new THREE.BoxGeometry(1, height, 1);

    // Color Logic
    let color = 0x00ff00;
    const rule = config[sensor.type];

    if (rule.warn_above && val > rule.warn_above) color = 0xff0000;
    if (rule.warn_below && val < rule.warn_below) color = 0xffaa00;

    const mat = new THREE.MeshPhongMaterial({ color });
    const bar = new THREE.Mesh(geom, mat);

    bar.position.set(x, height / 2, 0);

    scene.add(bar);
    bars.push(bar);
    x += 2.5;
  });
}

// Animation Loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

loadData();
