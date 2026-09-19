import { Component, Input, OnInit, OnChanges, inject, signal, SimpleChanges } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { NgTemplateOutlet } from '@angular/common';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { CrudService } from '../../core/services/crud.service';
import { ToastService } from '../../core/services/toast.service';
import { CrudField } from '../../core/models/crud.model';

interface FieldState {
  field: CrudField;
  value: string;
  error: string;
}

@Component({
  selector: 'app-crud-view',
  standalone: true,
  imports: [FormsModule, NgTemplateOutlet],
  templateUrl: './crud-view.component.html',
})
export class CrudViewComponent implements OnInit, OnChanges {
  @Input({ required: true }) crudKey!: string;

  private crud     = inject(CrudService);
  private toast    = inject(ToastService);
  private sanitizer = inject(DomSanitizer);

  def       = signal(this.crud.getCrud(this.crudKey ?? ''));
  items     = signal<Record<string, unknown>[]>([]);
  filtered  = signal<Record<string, unknown>[]>([]);
  fieldStates: FieldState[] = [];
  searchTerm = '';
  loading   = signal(false);

  /* Modal JSON viewer */
  modalVisible = signal(false);
  modalTitle   = signal('');
  modalBody    = signal('');

  ngOnInit(): void { this.init(); }

  ngOnChanges(c: SimpleChanges): void {
    if (c['crudKey'] && !c['crudKey'].firstChange) this.init();
  }

  private init(): void {
    const c = this.crud.getCrud(this.crudKey);
    this.def.set(c);
    if (!c) return;
    this.fieldStates = c.fields.map(f => ({ field: f, value: '', error: '' }));
    this.load();
  }

  load(): void {
    const c = this.def();
    if (!c) return;
    this.loading.set(true);
    this.crud.loadList(this.crudKey);
    // Poll signal until loaded (simple approach: subscribe to data signal)
    const check = () => {
      const rows = this.crud.getItems(this.crudKey);
      this.items.set(rows);
      this.filtered.set(rows);
      this.loading.set(false);
    };
    // Give the HTTP call time to complete
    setTimeout(check, 600);
  }

  filter(): void {
    const t = this.searchTerm.toLowerCase();
    this.filtered.set(t
      ? this.items().filter(r => JSON.stringify(r).toLowerCase().includes(t))
      : this.items()
    );
  }

  /* Form validation */
  validateAll(): boolean {
    let valid = true;
    this.fieldStates.forEach(fs => {
      fs.error = '';
      const v = fs.value.trim();
      if (fs.field.req && !v) { fs.error = 'Campo obligatorio'; valid = false; return; }
      if (v && fs.field.rule && !fs.field.rule(v)) { fs.error = fs.field.msg ?? 'Inválido'; valid = false; return; }
      if (fs.field.tp === 'number' && v && isNaN(Number(v))) { fs.error = 'Debe ser número'; valid = false; }
    });
    return valid;
  }

  save(): void {
    const c = this.def();
    if (!c || !this.validateAll()) {
      this.toast.show('Error en formulario', 'Corrige los campos marcados', 'err');
      return;
    }
    /* Construimos un objeto fake que simula los HTMLInputElement para reutilizar pay() */
    const formMap: Record<string, { value: string }> = {};
    this.fieldStates.forEach(fs => { formMap[fs.field.id] = { value: fs.value }; });
    this.crud.saveItem(this.crudKey, c.pay(formMap as any));
    setTimeout(() => {
      this.clearForm();
      this.load();
    }, 500);
  }

  clearForm(): void {
    this.fieldStates.forEach(fs => { fs.value = ''; fs.error = ''; });
  }

  /* Cell rendering — usa la función row() del CrudDef */
  renderRow(item: Record<string, unknown>): SafeHtml[] {
    const c = this.def();
    if (!c) return [];
    return c.row(item).map(html => this.sanitizer.bypassSecurityTrustHtml(html));
  }

  showJson(item: Record<string, unknown>): void {
    const c = this.def();
    this.modalTitle.set(c?.title ?? 'Registro');
    this.modalBody.set(JSON.stringify(item, null, 2));
    this.modalVisible.set(true);
  }

  /* Pairs: pone campos half en pares */
  get fieldPairs(): (FieldState | [FieldState, FieldState])[] {
    const pairs: (FieldState | [FieldState, FieldState])[] = [];
    let i = 0;
    while (i < this.fieldStates.length) {
      const cur  = this.fieldStates[i];
      const next = this.fieldStates[i + 1];
      if (cur.field.half && next?.field.half) { pairs.push([cur, next]); i += 2; }
      else { pairs.push(cur); i++; }
    }
    return pairs;
  }

  isPair(x: FieldState | [FieldState, FieldState]): x is [FieldState, FieldState] {
    return Array.isArray(x);
  }

  asSingle(x: FieldState | [FieldState, FieldState]): FieldState { return x as FieldState; }
  asPair(x: FieldState | [FieldState, FieldState]): [FieldState, FieldState] { return x as [FieldState, FieldState]; }

  get groupIcon(): string {
    const icons: Record<string, string> = { Maestros:'📋', Operaciones:'🔧', 'Logística':'🚚', Finanzas:'💰' };
    return icons[this.def()?.group ?? ''] ?? '📁';
  }
}
