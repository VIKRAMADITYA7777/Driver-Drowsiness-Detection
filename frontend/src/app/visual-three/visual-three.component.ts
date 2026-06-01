import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { gsap } from 'gsap';
import * as THREE from 'three';

@Component({
  selector: 'app-visual-three',
  templateUrl: './visual-three.component.html',
  styleUrls: ['./visual-three.component.scss']
})
export class VisualThreeComponent implements AfterViewInit {
  @ViewChild('canvasContainer', { static: true }) canvasContainer!: ElementRef<HTMLDivElement>;

  ngAfterViewInit(): void {
    this.initScene();
  }

  private initScene(): void {
    const container = this.canvasContainer.nativeElement;
    const scene = new THREE.Scene();
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    container.appendChild(renderer.domElement);

    const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
    camera.position.set(0, 1.8, 4);

    const ambient = new THREE.AmbientLight(0xffffff, 0.65);
    scene.add(ambient);
    const pointLight = new THREE.PointLight(0x00ffd5, 1.4, 10);
    pointLight.position.set(2, 3, 4);
    scene.add(pointLight);

    const geometry = new THREE.TorusKnotGeometry(0.8, 0.25, 120, 16);
    const material = new THREE.MeshStandardMaterial({
      color: 0x82f3ff,
      emissive: 0x0c4a6e,
      metalness: 0.4,
      roughness: 0.15
    });
    const knot = new THREE.Mesh(geometry, material);
    scene.add(knot);

    const animate = () => {
      knot.rotation.x += 0.006;
      knot.rotation.y += 0.01;
      renderer.render(scene, camera);
      requestAnimationFrame(animate);
    };
    animate();

    gsap.from(container, { duration: 1.5, opacity: 0, y: 40, ease: 'power3.out' });
  }
}
