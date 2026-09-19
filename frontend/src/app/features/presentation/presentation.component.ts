import { Component, inject, signal, OnInit, OnDestroy } from '@angular/core';
import { CrudService } from '../../core/services/crud.service';

interface ModCard { key: string; icon: string; title: string; desc: string; }

@Component({
  selector: 'app-presentation',
  standalone: true,
  templateUrl: './presentation.component.html',
  styleUrls: ['./presentation.component.css'],
})
export class PresentationComponent implements OnInit, OnDestroy {
  crud = inject(CrudService);

  currentSlide = signal(0);
  readonly totalSlides = 6;

  private observer?: IntersectionObserver;

  readonly modCards: ModCard[] = [
    { key:'ubigeo',        icon:'🗺️', title:'Ubigeo',       desc:'Distritos del Perú' },
    { key:'rubro',         icon:'🏷️', title:'Rubros',       desc:'Actividades económicas' },
    { key:'marca',         icon:'⭐', title:'Marcas',       desc:'Fabricantes' },
    { key:'tipo_unidad',   icon:'🚚', title:'Tipos Unidad', desc:'Categorías' },
    { key:'conductor',     icon:'👤', title:'Conductores',  desc:'Personal' },
    { key:'cliente',       icon:'🏢', title:'Clientes',     desc:'Empresas' },
    { key:'unidad',        icon:'🚛', title:'Flota',        desc:'Unidades' },
    { key:'viaje',         icon:'🕐', title:'Viajes',       desc:'Servicios' },
    { key:'guia',          icon:'📋', title:'Guías GRT',    desc:'Remisión' },
    { key:'viaje_r',       icon:'✅', title:'Realizados',   desc:'Completados' },
    { key:'factura',       icon:'🧾', title:'Facturas',     desc:'Cobros' },
    { key:'presupuesto',   icon:'💼', title:'Presupuestos', desc:'Costos' },
  ];

  count(key: string): number { return this.crud.getItems(key).length; }

  ngOnInit(): void {
    setTimeout(() => this.initObserver(), 80);
  }

  ngOnDestroy(): void {
    this.observer?.disconnect();
  }

  goSlide(n: number): void {
    const clamped = Math.max(0, Math.min(n, this.totalSlides - 1));
    this.currentSlide.set(clamped);
    const el = document.querySelector(`[data-slide="${clamped}"]`);
    el?.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  next(): void { this.goSlide(this.currentSlide() + 1); }
  prev(): void { this.goSlide(this.currentSlide() - 1); }

  private initObserver(): void {
    const wrap = document.getElementById('pres-wrap-ng');
    if (!wrap) return;
    this.observer = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const idx = Number((e.target as HTMLElement).dataset['slide']);
          this.currentSlide.set(idx);
        }
      });
    }, { root: wrap, threshold: 0.4 });
    wrap.querySelectorAll('.pres-slide').forEach(s => this.observer!.observe(s));
    this.goSlide(0);
  }
}
