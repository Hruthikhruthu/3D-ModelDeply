from flask import Flask, Response

app = Flask(__name__)

@app.route("/")
def index():
    html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Python + Three.js 3D Shapes</title>

    <style>
        body {
            margin: 0;
            overflow: hidden;
            background: linear-gradient(135deg, #1e1e2f, #111118);
            font-family: Arial;
        }
        #ui {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.12);
            padding: 20px;
            border-radius: 12px;
            width: 230px;
            color: white;
            backdrop-filter: blur(10px);
        }
        label { margin-top: 12px; display: block; }
        select, input[type=color], input[type=range] {
            width: 100%;
            padding: 6px;
            margin-top: 5px;
            border-radius: 6px;
            border: none;
            outline: none;
        }
    </style>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

</head>
<body>

<div id="ui">
    <h2>3D Shape Controls</h2>

    <label>Shape</label>
    <select id="shapeSelector">
        <option value="cube">Cube</option>
        <option value="sphere">Sphere</option>
        <option value="cone">Cone</option>
        <option value="cylinder">Cylinder</option>
        <option value="torus">Torus</option>
        <option value="pyramid">Pyramid</option>
        <option value="octahedron">Octahedron</option>
    </select>

    <label>Color</label>
    <input type="color" id="colorPicker" value="#ff6600">

    <label>Zoom</label>
    <input type="range" id="zoomSlider" min="10" max="60" value="28">

    <label>Rotation Speed</label>
    <input type="range" id="speedSlider" min="0" max="0.1" step="0.001" value="0.01">
</div>

<script>

const scene = new THREE.Scene();
scene.background = new THREE.Color(0x000000);

const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
);
camera.position.z = 28;

const renderer = new THREE.WebGLRenderer({ antialias:true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const light = new THREE.PointLight(0xffffff, 1.5);
light.position.set(20, 20, 20);
scene.add(light);

let object;
let rotationSpeed = 0.01;

function createShape(type) {
    if (object) scene.remove(object);

    let geo;

    switch (type) {
        case "cube": geo = new THREE.BoxGeometry(8,8,8); break;
        case "sphere": geo = new THREE.SphereGeometry(6,32,32); break;
        case "cone": geo = new THREE.ConeGeometry(5,10,32); break;
        case "cylinder": geo = new THREE.CylinderGeometry(4,4,10,32); break;
        case "torus": geo = new THREE.TorusGeometry(6,2,16,100); break;
        case "pyramid": geo = new THREE.TetrahedronGeometry(6); break;
        case "octahedron": geo = new THREE.OctahedronGeometry(6); break;
    }

    const mat = new THREE.MeshStandardMaterial({ color: 0xff6600 });
    object = new THREE.Mesh(geo, mat);
    scene.add(object);
}

createShape("cube");

document.getElementById("shapeSelector").addEventListener("change", e => {
    createShape(e.target.value);
});

document.getElementById("colorPicker").addEventListener("input", e => {
    object.material.color.set(e.target.value);
});

document.getElementById("zoomSlider").addEventListener("input", e => {
    camera.position.z = e.target.value;
});

document.getElementById("speedSlider").addEventListener("input", e => {
    rotationSpeed = Number(e.target.value);
});

let isDragging = false;
let previousX = 0;
let previousY = 0;

document.addEventListener("mousedown", (e) => {
    isDragging = true;
    previousX = e.clientX;
    previousY = e.clientY;
});

document.addEventListener("mouseup", () => {
    isDragging = false;
});

document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;

    const deltaX = e.clientX - previousX;
    const deltaY = e.clientY - previousY;

    if (object) {
        object.rotation.y += deltaX * 0.01;
        object.rotation.x += deltaY * 0.01;
    }

    previousX = e.clientX;
    previousY = e.clientY;
});

function animate() {
    requestAnimationFrame(animate);

    object.rotation.x += rotationSpeed;
    object.rotation.y += rotationSpeed;

    renderer.render(scene, camera);
}
animate();

window.addEventListener("resize", () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

</script>

</body>
</html>
"""
    return Response(html, mimetype="text/html")

if __name__ == "__main__":
    print("Running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
