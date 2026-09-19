import { Component, OnInit, inject } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { GastosApiService } from '../../core/services/gastos-api.service';
import { Comprobante, Gasto } from '../../core/models/gasto.model';
import { catchError, of } from 'rxjs';

interface LiveStat { id: string; label: string; value: string; }

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [RouterLink],
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.css'],
})
export class LandingComponent implements OnInit {
  private router = inject(Router);
  private gastosApi = inject(GastosApiService);

  // Solo se muestran indicadores del Módulo de Registro de Gastos y
  // Comprobantes, que es lo especificado para esta iteración.
  stats: LiveStat[] = [
    { id: 'registrados',  label: 'Gastos registrados',   value: '—' },
    { id: 'pagados',      label: 'Gastos pagados',       value: '—' },
    { id: 'sustentados',  label: 'Gastos sustentados',   value: '—' },
    { id: 'pendientes',   label: 'Comprobantes por aprobar', value: '—' },
  ];

  navLinks = ['Inicio', 'Dashboard'];
  activeNav = 'Inicio';

  ngOnInit(): void {
    this.loadStats();
    this.initParticles();
  }

  goToDashboard(): void {
    this.router.navigate(['/dashboard']);
  }

  setNav(link: string): void {
    this.activeNav = link;
    if (link === 'Dashboard') this.goToDashboard();
  }

  private loadStats(): void {
    this.gastosApi.get<Gasto[]>('/gastos').pipe(catchError(() => of([] as Gasto[]))).subscribe(gastos => {
      this.setStat('registrados', gastos.filter(g => g.estado === 'Registrado').length);
      this.setStat('pagados', gastos.filter(g => g.estado === 'Pagado').length);
      this.setStat('sustentados', gastos.filter(g => g.estado === 'Sustentado').length);
    });
    this.gastosApi.get<Comprobante[]>('/comprobantes?estado=Pendiente').pipe(catchError(() => of([] as Comprobante[]))).subscribe(rows => {
      this.setStat('pendientes', rows.length);
    });
  }

  private setStat(id: string, value: number): void {
    const stat = this.stats.find(s => s.id === id);
    if (stat) stat.value = String(value);
  }

  private initParticles(): void {
    // Defer to allow DOM to render
    setTimeout(() => {
      const container = document.getElementById('particles');
      if (!container) return;
      for (let i = 0; i < 18; i++) {
        const p = document.createElement('div');
        p.className = 'particle';
        p.style.cssText = `left:${Math.random()*100}%;width:${1+Math.random()*3}px;height:${1+Math.random()*3}px;animation-duration:${4+Math.random()*8}s;animation-delay:${Math.random()*6}s;opacity:${.2+Math.random()*.5}`;
        container.appendChild(p);
      }
    }, 0);
  }
}
