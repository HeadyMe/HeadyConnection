import * as THREE from "https://unpkg.com/three@0.160.0/build/three.module.js";

export const createInteraction = ({ camera, renderer, getParts, onSelect }) => {
  const raycaster = new THREE.Raycaster();
  const pointer = new THREE.Vector2();
  let hovered = null;

  const setPointer = (event) => {
    const rect = renderer.domElement.getBoundingClientRect();
    pointer.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    pointer.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
  };

  const highlight = (mesh, enabled) => {
    if (!mesh || !mesh.material || !mesh.material.emissive) {
      return;
    }
    mesh.material.emissive.setHex(enabled ? 0x3355ff : 0x000000);
  };

  const handleMove = (event) => {
    setPointer(event);
    raycaster.setFromCamera(pointer, camera);
    const hits = raycaster.intersectObjects(getParts(), false);
    const hit = hits[0]?.object ?? null;
    if (hit !== hovered) {
      highlight(hovered, false);
      highlight(hit, true);
      hovered = hit;
      renderer.domElement.style.cursor = hit ? "pointer" : "grab";
    }
  };

  const handleClick = () => {
    if (hovered) {
      onSelect(hovered.name);
    }
  };

  return {
    handleMove,
    handleClick,
    clearHighlight: () => highlight(hovered, false),
  };
};
