import * as THREE from "https://unpkg.com/three@0.160.0/build/three.module.js";
import { OrbitControls } from "https://unpkg.com/three@0.160.0/examples/jsm/controls/OrbitControls.js";
import { collectInteractiveParts, loadBodyModel } from "./js/modelLoader.js";
import { createInteraction } from "./js/interaction.js";
import { createOverlay } from "./js/overlay.js";
import { loadBodyPartData, getPartInfo } from "./js/dataStore.js";

const canvas = document.querySelector("#headylens-canvas");
const controlsPanel = document.querySelector("#headylens-controls");
const overlayToggle = document.querySelector("[data-action=toggle-overlay]");
const resetButton = document.querySelector("[data-action=reset]");

const scene = new THREE.Scene();
scene.background = new THREE.Color("#0b1120");

const camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 100);
camera.position.set(0, 1.8, 4.2);

const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(window.devicePixelRatio || 1);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.target.set(0, 1, 0);

const ambient = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambient);
const keyLight = new THREE.DirectionalLight(0xffffff, 0.9);
keyLight.position.set(2, 4, 3);
scene.add(keyLight);

const overlay = createOverlay();
let bodyData = {};

let interactiveParts = [];

const attachBody = async () => {
  const bodyGroup = await loadBodyModel();
  scene.add(bodyGroup);
  interactiveParts = collectInteractiveParts(bodyGroup);
};

const focusOnPart = (partName) => {
  const part = interactiveParts.find((mesh) => mesh.name === partName);
  if (!part) return;

  const box = new THREE.Box3().setFromObject(part);
  const center = box.getCenter(new THREE.Vector3());
  const size = box.getSize(new THREE.Vector3()).length();
  const distance = Math.max(2.4, size * 4);

  const targetPosition = center.clone().add(new THREE.Vector3(0, 0.2, distance));
  animateCamera(targetPosition, center);

  overlay.update(getPartInfo(bodyData, partName));
  overlay.setVisible(true);
};

const animateCamera = (targetPosition, targetLookAt) => {
  const startPosition = camera.position.clone();
  const startTarget = controls.target.clone();
  const duration = 800;
  const start = performance.now();

  const tick = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    const ease = progress * (2 - progress);

    camera.position.lerpVectors(startPosition, targetPosition, ease);
    controls.target.lerpVectors(startTarget, targetLookAt, ease);
    controls.update();

    if (progress < 1) {
      requestAnimationFrame(tick);
    }
  };
  requestAnimationFrame(tick);
};

const interaction = createInteraction({
  camera,
  renderer,
  getParts: () => interactiveParts,
  onSelect: focusOnPart,
});

const bindInteraction = () => {
  renderer.domElement.addEventListener("pointermove", interaction.handleMove);
  renderer.domElement.addEventListener("click", interaction.handleClick);
};

resetButton.addEventListener("click", () => {
  overlay.update(null);
  overlay.setVisible(false);
  animateCamera(new THREE.Vector3(0, 1.8, 4.2), new THREE.Vector3(0, 1, 0));
});

overlayToggle.addEventListener("click", () => {
  const isVisible = document.querySelector("#overlay-panel").getAttribute("data-visible") === "true";
  document.querySelector("#overlay-panel").setAttribute("data-visible", (!isVisible).toString());
});

controlsPanel.addEventListener("click", (event) => {
  const button = event.target.closest("button[data-part]");
  if (!button) return;
  focusOnPart(button.dataset.part);
});

controlsPanel.addEventListener("keydown", (event) => {
  if (event.key !== "Enter" && event.key !== " ") return;
  const button = event.target.closest("button[data-part]");
  if (!button) return;
  event.preventDefault();
  focusOnPart(button.dataset.part);
});

const resize = () => {
  const { innerWidth, innerHeight } = window;
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
};
window.addEventListener("resize", resize);

const animate = () => {
  controls.update();
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
};

Promise.all([attachBody(), loadBodyPartData()])
  .then(([, data]) => {
    bodyData = data;
    overlay.update(null);
    bindInteraction();
  })
  .catch((error) => {
    console.error(error);
    overlay.update({
      name: "Data unavailable",
      description: "Body part data could not be loaded.",
      logic: "Check the JSON feed and reload.",
      ip: "",
    });
    bindInteraction();
  })
  .finally(() => {
    overlay.setVisible(true);
    animate();
  });
