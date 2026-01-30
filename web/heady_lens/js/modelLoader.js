import * as THREE from "https://unpkg.com/three@0.160.0/build/three.module.js";
import { GLTFLoader } from "https://unpkg.com/three@0.160.0/examples/jsm/loaders/GLTFLoader.js";

const createMaterial = (color) =>
  new THREE.MeshStandardMaterial({ color, metalness: 0.1, roughness: 0.6, emissive: 0x000000 });

const addPart = (group, name, geometry, material, position) => {
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = name;
  mesh.position.copy(position);
  group.add(mesh);
  return mesh;
};

export const buildBodyModel = () => {
  const group = new THREE.Group();
  group.name = "HeadyLensBody";

  const skin = createMaterial(0xb08a6a);
  const organ = createMaterial(0xb83232);
  const neural = createMaterial(0x8a7bd1);
  const optic = createMaterial(0x6dcff6);

  addPart(group, "torso", new THREE.CapsuleGeometry(0.6, 1.3, 8, 16), skin, new THREE.Vector3(0, 0.4, 0));
  addPart(group, "head", new THREE.SphereGeometry(0.45, 24, 24), skin, new THREE.Vector3(0, 1.8, 0));
  addPart(group, "brain", new THREE.SphereGeometry(0.25, 20, 20), neural, new THREE.Vector3(0, 1.85, 0.1));
  addPart(group, "eyes", new THREE.SphereGeometry(0.08, 16, 16), optic, new THREE.Vector3(0.18, 1.8, 0.35));
  addPart(group, "eyes", new THREE.SphereGeometry(0.08, 16, 16), optic, new THREE.Vector3(-0.18, 1.8, 0.35));
  addPart(group, "heart", new THREE.SphereGeometry(0.18, 20, 20), organ, new THREE.Vector3(-0.15, 0.8, 0.35));
  addPart(group, "left_arm", new THREE.CylinderGeometry(0.12, 0.14, 1.0, 16), skin, new THREE.Vector3(-0.9, 0.6, 0));
  addPart(group, "right_arm", new THREE.CylinderGeometry(0.12, 0.14, 1.0, 16), skin, new THREE.Vector3(0.9, 0.6, 0));
  addPart(group, "legs", new THREE.CylinderGeometry(0.18, 0.2, 1.2, 16), skin, new THREE.Vector3(-0.3, -0.8, 0));
  addPart(group, "legs", new THREE.CylinderGeometry(0.18, 0.2, 1.2, 16), skin, new THREE.Vector3(0.3, -0.8, 0));

  return group;
};

const createHotspot = (name, position) => {
  const geometry = new THREE.SphereGeometry(0.08, 16, 16);
  const material = new THREE.MeshStandardMaterial({
    color: 0x60a5fa,
    emissive: 0x000000,
    transparent: true,
    opacity: 0.4,
  });
  const hotspot = new THREE.Mesh(geometry, material);
  hotspot.name = name;
  hotspot.position.copy(position);
  return hotspot;
};

const HOTSPOTS = [
  { name: "heart", position: new THREE.Vector3(-0.15, 0.8, 0.35) },
  { name: "brain", position: new THREE.Vector3(0, 1.85, 0.1) },
  { name: "left_arm", position: new THREE.Vector3(-0.9, 0.6, 0) },
  { name: "right_arm", position: new THREE.Vector3(0.9, 0.6, 0) },
  { name: "lungs", position: new THREE.Vector3(0.2, 0.95, 0.25) },
  { name: "eyes", position: new THREE.Vector3(0.18, 1.8, 0.35) },
  { name: "heady_make", position: new THREE.Vector3(0.55, 0.3, 0.4) },
  { name: "heady_field", position: new THREE.Vector3(0, 0.1, 0.55) },
  { name: "heady_legacy", position: new THREE.Vector3(-0.5, 0.25, 0.4) },
];

export const loadBodyModel = async () => {
  const group = new THREE.Group();
  group.name = "HeadyLensBodyRoot";
  const loader = new GLTFLoader();

  try {
    const gltf = await loader.loadAsync("./assets/body.gltf");
    gltf.scene.name = "HeadyLensBody";
    group.add(gltf.scene);
  } catch (error) {
    console.warn("GLTF load failed, falling back to primitive model.", error);
    group.add(buildBodyModel());
  }

  HOTSPOTS.forEach((hotspot) => {
    group.add(createHotspot(hotspot.name, hotspot.position));
  });

  return group;
};

export const collectInteractiveParts = (group) =>
  group.children.filter((child) =>
    [
      "heart",
      "brain",
      "left_arm",
      "right_arm",
      "lungs",
      "eyes",
      "heady_make",
      "heady_field",
      "heady_legacy",
    ].includes(child.name),
  );
