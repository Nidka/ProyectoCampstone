import { CrudDef } from './crud.model';

/* ── Helpers de render de celdas ── */
const esc = (v: unknown) => String(v ?? '').replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m] ?? m));
const p   = (v: unknown) => (v == null || v === '') ? `<span style="color:var(--t4)">—</span>` : esc(v);
const mkId    = (n: unknown) => `<span class="id-tag">#${p(n)}</span>`;
const mkMono  = (s: unknown) => `<span class="mono">${p(s)}</span>`;
const mkMoney = (n: unknown) => {
  if (n == null || n === '') return p(null);
  return `<span class="money"><span class="sy">S/.</span>${Number(n).toLocaleString('es-PE',{minimumFractionDigits:2,maximumFractionDigits:2})}</span>`;
};
const mkPlate = (s: unknown) => s ? `<span class="plate"><span class="plate-pe">PE</span><span class="plate-num">${esc(s)}</span></span>` : p(null);
const mkRoute = (a: unknown, b: unknown) =>
  `<span class="route"><span>${p(a)}</span><svg width="10" height="10" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="9 18 15 12 9 6"/></svg><span>${p(b)}</span></span>`;
const mkSt = (v: unknown, tl = 'Activo', fl = 'Inactivo') => {
  const ok = v ?? true;
  return `<span class="lbl ${ok ? 'lbl-ok':'lbl-err'}"><span class="ldot ${ok ? 'ldot-ok':'ldot-err'}"></span>${ok ? tl : fl}</span>`;
};
const AVC = ['#e11d48','#4ADE80','#60A5FA','#F87171','#FCD34D','#C084FC','#34D399','#FB923C'];
const avc = (s: string) => { let h=0; for(const c of s) h=(h<<5)-h+c.charCodeAt(0); return AVC[Math.abs(h)%AVC.length]; };
const ini = (s: string) => s.trim().split(/\s+/).map(w=>w[0]??'').slice(0,2).join('').toUpperCase()||'?';
const mkAv = (name: string, sq=false) => `<span class="${sq?'av av-sq':'av'}" style="background:${avc(name||'?')}" title="${esc(name)}">${ini(name||'?')}</span>`;

/* ════════════════════════════════════
   18 MÓDULOS CRUD
════════════════════════════════════ */
export const CRUDS: CrudDef[] = [

  /* ── MAESTROS ── */
  {
    key:'ubigeo', title:'Ubigeo', route:'/ubigeos', nk:'ubigeo', group:'Maestros',
    desc:'Distritos, provincias y departamentos del Perú',
    fields:[
      {id:'ub_c',  l:'Código (6 dígitos)', tp:'number', req:true,  half:true, rule:v=>/^\d{6}$/.test(v), msg:'Debe tener 6 dígitos'},
      {id:'ub_dp', l:'Departamento',       tp:'text',   req:true,  half:true},
      {id:'ub_p',  l:'Provincia',          tp:'text',   req:true,  half:true},
      {id:'ub_d',  l:'Distrito',           tp:'text',   req:true,  half:true},
    ],
    pay: f => ({ codigo:Number(f['ub_c'].value), departamento:f['ub_dp'].value, provincia:f['ub_p'].value, distrito:f['ub_d'].value }),
    cols:['Código','Departamento','Provincia','Distrito'],
    row: i => [
      `<span class="lbl lbl-info" style="font-family:monospace">${p(i['codigo'])}</span>`,
      `<strong>${p(i['departamento'])}</strong>`, p(i['provincia']),
      `<span style="color:var(--t2)">${p(i['distrito'])}</span>`,
    ],
  },
  {
    key:'rubro', title:'Rubro', route:'/rubros', nk:'rubro', group:'Maestros',
    desc:'Clasificación de actividades económicas',
    fields:[{id:'ru_n',l:'Nombre',tp:'text',req:true},{id:'ru_d',l:'Descripción',tp:'text',req:false}],
    pay: f => ({ nombre:f['ru_n'].value, descripcion:f['ru_d'].value||null }),
    cols:['#','Nombre','Descripción'],
    row: i => [mkId(i['id_rubro']??i['id']), `<div style="display:flex;align-items:center;gap:8px">${mkAv(String(i['nombre']||'?'),true)}<strong>${p(i['nombre'])}</strong></div>`, `<span style="color:var(--t3)">${p(i['descripcion'])}</span>`],
  },
  {
    key:'marca', title:'Marca', route:'/marcas', nk:'marca', group:'Maestros',
    desc:'Fabricantes de vehículos de la flota',
    fields:[{id:'ma_n',l:'Nombre',tp:'text',req:true,half:true},{id:'ma_p',l:'País de origen',tp:'text',req:false,half:true,placeholder:'Ej: Alemania…'}],
    pay: f => ({ nombre:f['ma_n'].value, pais_origen:f['ma_p'].value||null }),
    cols:['#','Marca','País'],
    row: i => [mkId(i['id_marca']??i['id']), `<div style="display:flex;align-items:center;gap:8px">${mkAv(String(i['nombre']||'?'),true)}<strong>${p(i['nombre'])}</strong></div>`, i['pais_origen']?`<span class="lbl lbl-n">🌍 ${p(i['pais_origen'])}</span>`:p(null)],
  },
  {
    key:'tipo_unidad', title:'Tipo de Unidad', route:'/tipos-unidad', nk:'tipo_unidad', group:'Maestros',
    desc:'Tracto, camión, semirremolque, etc.',
    fields:[{id:'tu_n',l:'Nombre',tp:'text',req:true,placeholder:'Ej: Tracto…'},{id:'tu_d',l:'Descripción',tp:'text',req:false}],
    pay: f => ({ nombre:f['tu_n'].value, descripcion:f['tu_d'].value||null }),
    cols:['#','Tipo','Descripción'],
    row: i => [mkId(i['id_tipo_unidad']??i['id']), `<span class="lbl lbl-y">🚚 ${p(i['nombre'])}</span>`, `<span style="color:var(--t3)">${p(i['descripcion'])}</span>`],
  },
  {
    key:'subtipo_unidad', title:'Subtipo de Unidad', route:'/subtipos-unidad', nk:'subtipo_unidad', group:'Maestros',
    desc:'Subclasificación dentro de cada tipo de vehículo',
    fields:[
      {id:'su_t',l:'ID Tipo unidad',tp:'number',req:true,half:true},
      {id:'su_n',l:'Nombre',tp:'text',req:true,half:true,placeholder:'Ej: Plataforma…'},
      {id:'su_d',l:'Descripción',tp:'text',req:false},
    ],
    pay: f => ({ id_tipo_unidad:Number(f['su_t'].value), nombre:f['su_n'].value, descripcion:f['su_d'].value||null }),
    cols:['#','Subtipo','Tipo padre','Descripción'],
    row: i => [mkId(i['id_subtipo_unidad']??i['id']), `<strong>${p(i['nombre'])}</strong>`, `<span class="lbl lbl-n">Tipo #${p(i['id_tipo_unidad'])}</span>`, `<span style="color:var(--t3)">${p(i['descripcion'])}</span>`],
  },
  {
    key:'tipo_gasto', title:'Tipo de Gasto', route:'/tipos-gasto', nk:'tipo_gasto', group:'Maestros',
    desc:'Combustible, peajes, mantenimiento…',
    fields:[{id:'tg_n',l:'Nombre',tp:'text',req:true,placeholder:'Ej: Combustible…'},{id:'tg_d',l:'Descripción',tp:'text',req:false}],
    pay: f => ({ nombre:f['tg_n'].value, descripcion:f['tg_d'].value||null }),
    cols:['#','Tipo de gasto','Descripción'],
    row: i => [mkId(i['id_tipo_gasto']??i['id']), `<div style="display:flex;align-items:center;gap:8px"><div style="width:8px;height:8px;border-radius:50%;background:var(--warn)"></div><strong>${p(i['nombre'])}</strong></div>`, `<span style="color:var(--t3)">${p(i['descripcion'])}</span>`],
  },
  {
    key:'cat_prod', title:'Categoría Producto', route:'/categorias-producto', nk:'cat_prod', group:'Maestros',
    desc:'Clasificación de mercancías transportadas',
    fields:[{id:'cp_n',l:'Nombre',tp:'text',req:true,placeholder:'Ej: Alimentos…'},{id:'cp_d',l:'Descripción',tp:'text',req:false}],
    pay: f => ({ nombre:f['cp_n'].value, descripcion:f['cp_d'].value||null }),
    cols:['#','Categoría','Descripción'],
    row: i => [mkId(i['id_categoria']??i['id']), `<span class="lbl lbl-info">📦 ${p(i['nombre'])}</span>`, `<span style="color:var(--t3)">${p(i['descripcion'])}</span>`],
  },

  /* ── OPERACIONES ── */
  {
    key:'direccion', title:'Dirección', route:'/direcciones', nk:'direccion', group:'Operaciones',
    desc:'Puntos de origen, destino y domicilios',
    fields:[
      {id:'di_u',l:'Código Ubigeo',     tp:'number',req:true, half:true,placeholder:'6 dígitos'},
      {id:'di_r',l:'Referencia',         tp:'text',  req:false,half:true,placeholder:'Cerca al parque…'},
      {id:'di_d',l:'Dirección detallada',tp:'text',  req:true, placeholder:'Av. / Jr. + número'},
    ],
    pay: f => ({ codigo_ubigeo:Number(f['di_u'].value), direccion_detallada:f['di_d'].value, referencia:f['di_r'].value||null }),
    cols:['#','Dirección','Ubigeo','Referencia'],
    row: i => [mkId(i['id_direccion']??i['id']), `<strong>${p(i['direccion_detallada'])}</strong>`, `<span class="lbl lbl-info">UB-${p(i['codigo_ubigeo'])}</span>`, `<span style="color:var(--t3)">${p(i['referencia'])}</span>`],
  },
  {
    key:'conductor', title:'Conductor', route:'/conductores', nk:'conductor', group:'Operaciones',
    desc:'Personal conductor habilitado con licencia vigente',
    fields:[
      {id:'co_dni',l:'DNI',              tp:'text',  req:true, half:true,rule:v=>/^\d{8}$/.test(v),msg:'8 dígitos'},
      {id:'co_lic',l:'N° Licencia',      tp:'text',  req:true, half:true},
      {id:'co_n1', l:'Primer nombre',    tp:'text',  req:true, half:true},
      {id:'co_a1', l:'Apellido paterno', tp:'text',  req:true, half:true},
      {id:'co_n2', l:'Segundo nombre',   tp:'text',  req:false,half:true},
      {id:'co_a2', l:'Apellido materno', tp:'text',  req:false,half:true},
      {id:'co_tel',l:'Teléfono',         tp:'text',  req:false,half:true,placeholder:'+51 9…'},
      {id:'co_cor',l:'Correo',           tp:'email', req:false,half:true},
    ],
    pay: f => ({ dni:f['co_dni'].value, nombre1:f['co_n1'].value, nombre2:f['co_n2'].value||null, apellido1:f['co_a1'].value, apellido2:f['co_a2'].value||null, licencia_conducir:f['co_lic'].value, telefono:f['co_tel'].value||null, correo:f['co_cor'].value||null }),
    cols:['Conductor','DNI','Licencia','Teléfono','Estado'],
    row: i => {
      const nm = `${i['nombre1']||''} ${i['apellido1']||''}`.trim();
      return [
        `<div style="display:flex;align-items:center;gap:10px">${mkAv(nm)}<div><div style="font-weight:600">${p(nm)}</div><div style="font-size:.7rem;color:var(--t4)">${p(i['nombre2']||'')} ${p(i['apellido2']||'')}</div></div></div>`,
        mkMono(i['dni']), mkMono(i['licencia_conducir']),
        `<span style="color:var(--t2)">${p(i['telefono'])}</span>`,
        mkSt(i['estado_conductor'] ?? true),
      ];
    },
  },
  {
    key:'cliente', title:'Cliente', route:'/clientes', nk:'cliente', group:'Operaciones',
    desc:'Empresas y personas que contratan el servicio',
    fields:[
      {id:'cl_r',  l:'Razón social',       tp:'text',  req:true},
      {id:'cl_ruc',l:'RUC',                tp:'text',  req:true,half:true,rule:v=>/^\d{11}$/.test(v),msg:'11 dígitos'},
      {id:'cl_rb', l:'ID Rubro',           tp:'number',req:false,half:true,placeholder:'Opcional'},
      {id:'cl_t',  l:'Teléfono',           tp:'text',  req:false,half:true,placeholder:'+51…'},
      {id:'cl_e',  l:'Correo',             tp:'email', req:false,half:true},
      {id:'cl_c',  l:'Persona de contacto',tp:'text',  req:false},
    ],
    pay: f => ({ razon_social:f['cl_r'].value, ruc:f['cl_ruc'].value, telefono:f['cl_t'].value||null, correo:f['cl_e'].value||null, contacto:f['cl_c'].value||null, id_rubro:f['cl_rb'].value?Number(f['cl_rb'].value):null }),
    cols:['Empresa','RUC','Teléfono','Estado'],
    row: i => [
      `<div style="display:flex;align-items:center;gap:10px">${mkAv(String(i['razon_social']||'?'),true)}<div><div style="font-weight:600">${p(i['razon_social'])}</div><div style="font-size:.7rem;color:var(--t4)">${p(i['correo'])}</div></div></div>`,
      mkMono(i['ruc']), `<span style="color:var(--t2)">${p(i['telefono'])}</span>`,
      mkSt(i['estado_cliente'] ?? true),
    ],
  },
  {
    key:'unidad', title:'Flota — Unidades', route:'/unidades', nk:'unidad', group:'Operaciones',
    desc:'Tractos, camiones y remolques registrados',
    fields:[
      {id:'un_p', l:'Placa',           tp:'text',  req:true, half:true,placeholder:'ABC-123'},
      {id:'un_a', l:'Año',             tp:'number',req:false,half:true,rule:v=>!v||Number(v)>=1900,msg:'Inválido'},
      {id:'un_ti',l:'ID Tipo unidad',  tp:'number',req:true, half:true},
      {id:'un_s', l:'ID Subtipo',      tp:'number',req:false,half:true,placeholder:'Opcional'},
      {id:'un_m', l:'ID Marca',        tp:'number',req:true, half:true},
      {id:'un_mo',l:'Modelo',          tp:'text',  req:false,half:true,placeholder:'Ej: Actros 2646'},
      {id:'un_pt',l:'Peso tara (ton)', tp:'number',req:false,half:true},
      {id:'un_pm',l:'Peso máx. (ton)', tp:'number',req:false,half:true},
    ],
    pay: f => ({ placa:(f['un_p'].value as string).toUpperCase(), id_tipo_unidad:Number(f['un_ti'].value), id_subtipo_unidad:f['un_s'].value?Number(f['un_s'].value):null, id_marca:Number(f['un_m'].value), modelo:f['un_mo'].value||null, anio:f['un_a'].value?Number(f['un_a'].value):null, peso_tara:f['un_pt'].value?Number(f['un_pt'].value):null, peso_maximo:f['un_pm'].value?Number(f['un_pm'].value):null }),
    cols:['Placa','Modelo','Tipo','Año','Estado'],
    row: i => [
      mkPlate(i['placa']),
      `<div><div style="font-weight:600">${p(i['modelo']||'Sin modelo')}</div><div style="font-size:.7rem;color:var(--t4)">Marca #${p(i['id_marca'])}</div></div>`,
      `<span class="lbl lbl-y">Tipo #${p(i['id_tipo_unidad'])}</span>`,
      i['anio']?`<span class="lbl lbl-n">${p(i['anio'])}</span>`:p(null),
      mkSt(i['estado_unidad']??true,'Operativa','Inactiva'),
    ],
  },
  {
    key:'cond_uni', title:'Asignación C/U', route:'/asignaciones-conductor-unidad', nk:'cond_uni', group:'Operaciones',
    desc:'Vinculación conductor–vehículo',
    fields:[{id:'cu_c',l:'ID Conductor',tp:'number',req:true,half:true},{id:'cu_u',l:'ID Unidad',tp:'number',req:true,half:true}],
    pay: f => ({ id_conductor:Number(f['cu_c'].value), id_unidad:Number(f['cu_u'].value) }),
    cols:['#','Conductor','Unidad','Estado'],
    row: i => [mkId(i['id_conductor_unidad']??i['id']), `<span class="lbl lbl-info">Cond. #${p(i['id_conductor'])}</span>`, `<span class="lbl lbl-y">Unid. #${p(i['id_unidad'])}</span>`, mkSt(i['estado_asignacion']??true,'Activa','Finalizada')],
  },

  /* ── LOGÍSTICA ── */
  {
    key:'viaje', title:'Viaje', route:'/viajes', nk:'viaje', group:'Logística',
    desc:'Servicios de transporte de carga programados',
    fields:[
      {id:'vi_tr',l:'ID Tracto',        tp:'number',req:true, half:true},
      {id:'vi_ca',l:'ID Carreta',       tp:'number',req:false,half:true,placeholder:'Opcional'},
      {id:'vi_cu',l:'ID Asignación C/U',tp:'number',req:true, half:true},
      {id:'vi_cl',l:'ID Cliente',       tp:'number',req:true, half:true},
      {id:'vi_o', l:'ID Dir. Origen',   tp:'number',req:true, half:true},
      {id:'vi_d', l:'ID Dir. Destino',  tp:'number',req:true, half:true},
    ],
    pay: f => ({ id_tracto:Number(f['vi_tr'].value), id_carreta:f['vi_ca'].value?Number(f['vi_ca'].value):null, id_conductor_unidad:Number(f['vi_cu'].value), id_cliente:Number(f['vi_cl'].value), id_direccion_origen:Number(f['vi_o'].value), id_direccion_destino:Number(f['vi_d'].value) }),
    cols:['#','Ruta','Cliente','Tracto','Estado'],
    row: i => [mkId(i['id_viaje']??i['id']), mkRoute(`Orig.#${i['id_direccion_origen']}`,`Dest.#${i['id_direccion_destino']}`), `<span class="lbl lbl-n">CLI-${p(i['id_cliente'])}</span>`, `<span class="lbl lbl-y">🚛 #${p(i['id_tracto'])}</span>`, mkSt(i['estado_viaje']??true,'Programado','Cancelado')],
  },
  {
    key:'guia', title:'Guía Transportista', route:'/guias-transportista', nk:'guia', group:'Logística',
    desc:'Guías de remisión del transportista (GRT)',
    fields:[
      {id:'gu_n',l:'N° de guía GRT',tp:'text',  req:true, placeholder:'GRT-001-0001'},
      {id:'gu_v',l:'ID Viaje',      tp:'number',req:true, half:true},
      {id:'gu_p',l:'Peso total (kg)',tp:'number',req:true, half:true,rule:v=>Number(v)>0,msg:'>0'},
      {id:'gu_r',l:'Guías remitente',tp:'text', req:false},
    ],
    pay: f => ({ numero_guia:f['gu_n'].value, id_viaje:Number(f['gu_v'].value), peso_total:Number(f['gu_p'].value), guias_remitente:f['gu_r'].value||null }),
    cols:['N° GRT','Viaje','Peso','Estado'],
    row: i => [mkMono(i['numero_guia']), `<span class="lbl lbl-n">Viaje #${p(i['id_viaje'])}</span>`, `<strong>${p(i['peso_total'])} <small style="color:var(--t4)">kg</small></strong>`, mkSt(i['estado_guia']??true,'Vigente','Anulada')],
  },
  {
    key:'viaje_r', title:'Viaje Realizado', route:'/viajes-realizados', nk:'viaje_r', group:'Logística',
    desc:'Servicios de transporte completados con flete',
    fields:[
      {id:'vr_g',l:'ID Guía GRT',   tp:'number',  req:true,  half:true},
      {id:'vr_f',l:'Flete (S/.)',    tp:'number',  req:true,  half:true,rule:v=>Number(v)>0,msg:'>0'},
      {id:'vr_o',l:'Observaciones', tp:'textarea', req:false, placeholder:'Incidencias del viaje…'},
    ],
    pay: f => ({ id_guia_transportista:Number(f['vr_g'].value), flete:Number(f['vr_f'].value), observaciones:f['vr_o'].value||null }),
    cols:['#','GRT','Flete','Estado'],
    row: i => [mkId(i['id_viaje_realizado']??i['id']), `<span class="mono">GRT #${p(i['id_guia_transportista'])}</span>`, mkMoney(i['flete']), mkSt(i['estado_viaje_realizado']??true,'Completado','Pendiente')],
  },
  {
    key:'prod_t', title:'Productos Transportados', route:'/productos-transportados', nk:'prod_t', group:'Logística',
    desc:'Detalle de mercancías por guía de remisión',
    fields:[
      {id:'pt_g', l:'ID Guía GRT',  tp:'number',req:true, half:true},
      {id:'pt_c', l:'ID Categoría', tp:'number',req:true, half:true},
      {id:'pt_d', l:'Descripción',  tp:'text',  req:true, placeholder:'Ej: Harina de trigo…'},
      {id:'pt_ca',l:'Cantidad',     tp:'number',req:true, half:true,rule:v=>Number(v)>0,msg:'>0'},
      {id:'pt_p', l:'Peso (kg)',    tp:'number',req:true, half:true,rule:v=>Number(v)>0,msg:'>0'},
    ],
    pay: f => ({ id_guia_transportista:Number(f['pt_g'].value), id_categoria:Number(f['pt_c'].value), descripcion_producto:f['pt_d'].value, cantidad:Number(f['pt_ca'].value), peso:Number(f['pt_p'].value) }),
    cols:['#','Producto','Cant.','Peso','GRT'],
    row: i => [mkId(i['id_producto_transportado']??i['id']), `<strong>${p(i['descripcion_producto'])}</strong>`, `<strong>${p(i['cantidad'])}</strong>`, `<strong>${p(i['peso'])} <small style="color:var(--t4)">kg</small></strong>`, `<span class="mono">GRT #${p(i['id_guia_transportista'])}</span>`],
  },

  /* ── FINANZAS ── */
  {
    key:'factura', title:'Factura', route:'/facturas', nk:'factura', group:'Finanzas',
    desc:'Documentos de cobro por servicios de transporte',
    fields:[
      {id:'fa_n',l:'N° de factura',      tp:'text',  req:true, placeholder:'F001-00001'},
      {id:'fa_v',l:'ID Viaje realizado', tp:'number',req:true, half:true},
      {id:'fa_m',l:'Monto total (S/.)',  tp:'number',req:true, half:true,rule:v=>Number(v)>0,msg:'>0'},
    ],
    pay: f => ({ numero_factura:f['fa_n'].value, id_viaje_realizado:Number(f['fa_v'].value), monto_total:Number(f['fa_m'].value) }),
    cols:['N° Factura','Viaje Realizado','Monto','Estado'],
    row: i => [
      `<div style="display:flex;align-items:center;gap:7px"><div style="width:7px;height:7px;border-radius:50%;background:var(--red)"></div>${mkMono(i['numero_factura'])}</div>`,
      `<span class="lbl lbl-n">VR #${p(i['id_viaje_realizado'])}</span>`,
      mkMoney(i['monto_total']), mkSt(i['estado_factura']??true,'Activa','Anulada'),
    ],
  },
  {
    key:'presupuesto', title:'Presupuesto de Viaje', route:'/presupuestos-viaje', nk:'presupuesto', group:'Finanzas',
    desc:'Estimación de costos operativos por viaje',
    fields:[
      {id:'pe_v',l:'ID Viaje',         tp:'number',req:true, half:true},
      {id:'pe_m',l:'Monto total (S/.)',tp:'number',req:true, half:true,rule:v=>Number(v)>0,msg:'>0'},
    ],
    pay: f => ({ id_viaje:Number(f['pe_v'].value), monto_total:Number(f['pe_m'].value) }),
    cols:['#','Viaje','Monto','Estado'],
    row: i => [mkId(i['id_presupuesto']??i['id']), `<span class="lbl lbl-n">Viaje #${p(i['id_viaje'])}</span>`, mkMoney(i['monto_total']), mkSt(i['estado_presupuesto']??true,'Aprobado','Pendiente')],
  },
  {
    key:'det_pres', title:'Detalle Presupuesto', route:'/detalles-presupuesto', nk:'det_pres', group:'Finanzas',
    desc:'Desglose de gastos por tipo de cada presupuesto',
    fields:[
      {id:'dp_p',l:'ID Presupuesto',       tp:'number',req:true, half:true},
      {id:'dp_t',l:'ID Tipo de gasto',     tp:'number',req:true, half:true},
      {id:'dp_m',l:'Monto estimado (S/.)', tp:'number',req:true, rule:v=>Number(v)>0,msg:'>0'},
    ],
    pay: f => ({ id_presupuesto_viaje:Number(f['dp_p'].value), id_tipo_gasto:Number(f['dp_t'].value), monto_estimado:Number(f['dp_m'].value) }),
    cols:['#','Presupuesto','Tipo gasto','Monto est.'],
    row: i => [mkId(i['id_detalle_presupuesto']??i['id']), `<span class="lbl lbl-n">Pres. #${p(i['id_presupuesto']??i['id_presupuesto_viaje'])}</span>`, `<span class="lbl lbl-warn">⚡ TG #${p(i['id_tipo_gasto'])}</span>`, mkMoney(i['monto_estimado'])],
  },
];
