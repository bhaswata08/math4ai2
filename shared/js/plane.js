// Interactive figures on a coordinate plane.
//
// A figure is a <div data-fig="name"> in a section. A deck script registers
// the name with Figures.register(name, mount), and deck.js calls
// Figures.mountAll once the sections are in the page. mount(el) builds the
// figure inside el, usually with a Plane.
//
// Plane draws a static grid and axes once, then the figure redraws its
// dynamic layer from its own state on every change: clear(), then arrow(),
// segment(), label() and so on. That keeps a figure a pure function of its
// state, which is what makes dragging bugs rare.
//
// Colours come from the CSS custom properties in shared/css/custom.css
// through role('v') and friends, so figures match slides and clips. SVG
// attributes and KaTeX \textcolor both need a concrete colour, not var().

window.Figures = {
  registry: {},
  register(name, mount) { this.registry[name] = mount; },
  mountAll(root) {
    root.querySelectorAll('[data-fig]').forEach((el) => {
      const mount = this.registry[el.dataset.fig];
      if (!mount) { console.error('no figure registered as ' + el.dataset.fig); return; }
      mount(el);
    });
  },
};

const SVGNS = 'http://www.w3.org/2000/svg';

function svgEl(tag, attrs, parent) {
  const n = document.createElementNS(SVGNS, tag);
  for (const [k, v] of Object.entries(attrs || {})) n.setAttribute(k, v);
  if (parent) parent.appendChild(n);
  return n;
}

window.Plane = class Plane {
  // opts: xmin, xmax, ymin, ymax in plane units; unit = pixels per unit.
  constructor(container, opts) {
    this.o = Object.assign({ xmin: -5, xmax: 5, ymin: -3, ymax: 3, unit: 60, ticks: true }, opts);
    const { xmin, xmax, ymin, ymax, unit } = this.o;
    this.w = (xmax - xmin) * unit;
    this.h = (ymax - ymin) * unit;
    this.svg = svgEl('svg', { viewBox: `0 0 ${this.w} ${this.h}` }, container);
    this.svg.style.maxWidth = this.w + 'px';
    this.static = svgEl('g', {}, this.svg);
    this.layer = svgEl('g', {}, this.svg);
    this.handles = svgEl('g', {}, this.svg);
    this.drawGrid();
  }

  px([x, y]) {
    return [(x - this.o.xmin) * this.o.unit, (this.o.ymax - y) * this.o.unit];
  }

  // Screen point to plane units. getScreenCTM folds in reveal's own scaling
  // of the stage, so dragging stays under the pointer at any window size.
  fromEvent(ev) {
    const pt = this.svg.createSVGPoint();
    pt.x = ev.clientX; pt.y = ev.clientY;
    const p = pt.matrixTransform(this.svg.getScreenCTM().inverse());
    return [p.x / this.o.unit + this.o.xmin, this.o.ymax - p.y / this.o.unit];
  }

  drawGrid() {
    const { xmin, xmax, ymin, ymax } = this.o;
    const g = this.static;
    for (let x = Math.ceil(xmin); x <= xmax; x++) {
      const [a, b] = [this.px([x, ymin]), this.px([x, ymax])];
      svgEl('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: role('grid'), 'stroke-width': 1.5 }, g);
    }
    for (let y = Math.ceil(ymin); y <= ymax; y++) {
      const [a, b] = [this.px([xmin, y]), this.px([xmax, y])];
      svgEl('line', { x1: a[0], y1: a[1], x2: b[0], y2: b[1], stroke: role('grid'), 'stroke-width': 1.5 }, g);
    }
    const ax = [this.px([xmin, 0]), this.px([xmax, 0])];
    const ay = [this.px([0, ymin]), this.px([0, ymax])];
    svgEl('line', { x1: ax[0][0], y1: ax[0][1], x2: ax[1][0], y2: ax[1][1], stroke: role('ink-dim'), 'stroke-width': 2.5 }, g);
    svgEl('line', { x1: ay[0][0], y1: ay[0][1], x2: ay[1][0], y2: ay[1][1], stroke: role('ink-dim'), 'stroke-width': 2.5 }, g);
  }

  clear() { this.layer.replaceChildren(); }

  // An arrow from a to b in plane units. The shaft stops at the base of the
  // head so a thick stroke never pokes through the tip.
  arrow(a, b, color, { width = 5, head = 18, opacity = 1, dashed = false } = {}) {
    const [x1, y1] = this.px(a), [x2, y2] = this.px(b);
    const len = Math.hypot(x2 - x1, y2 - y1);
    if (len < 1e-6) return;
    const ux = (x2 - x1) / len, uy = (y2 - y1) / len;
    const h = Math.min(head, len * 0.6);
    const bx = x2 - ux * h, by = y2 - uy * h;
    const g = svgEl('g', { opacity }, this.layer);
    svgEl('line', {
      x1, y1, x2: bx, y2: by, stroke: color, 'stroke-width': width,
      'stroke-dasharray': dashed ? '10 8' : 'none',
    }, g);
    const px = -uy * h * 0.42, py = ux * h * 0.42;
    svgEl('polygon', { points: `${x2},${y2} ${bx + px},${by + py} ${bx - px},${by - py}`, fill: color }, g);
    return g;
  }

  segment(a, b, color, { width = 3, dashed = true, opacity = 1 } = {}) {
    const [x1, y1] = this.px(a), [x2, y2] = this.px(b);
    return svgEl('line', {
      x1, y1, x2, y2, stroke: color, 'stroke-width': width, opacity,
      'stroke-dasharray': dashed ? '8 7' : 'none',
    }, this.layer);
  }

  // The graph of y = f(x) as a polyline, sampled across the plane.
  curve(f, color, { width = 4, from = this.o.xmin, to = this.o.xmax, steps = 400, opacity = 1, dashed = false } = {}) {
    const pts = [];
    for (let i = 0; i <= steps; i++) {
      const x = from + ((to - from) * i) / steps;
      pts.push(this.px([x, f(x)]).join(","));
    }
    return svgEl("polyline", {
      points: pts.join(" "), fill: "none", stroke: color, "stroke-width": width, opacity,
      "stroke-linecap": "round", "stroke-linejoin": "round",
      "stroke-dasharray": dashed ? "8 7" : "none",
    }, this.layer);
  }

  dot(p, color, r = 6) {
    const [x, y] = this.px(p);
    return svgEl('circle', { cx: x, cy: y, r, fill: color }, this.layer);
  }

  // KaTeX label centred on p (plane units), nudged by [dx, dy] pixels.
  label(p, tex, color, { dx = 0, dy = 0, size = 30 } = {}) {
    const [x, y] = this.px(p);
    const fo = svgEl('foreignObject', { x: x + dx - 150, y: y + dy - 30, width: 300, height: 60 }, this.layer);
    fo.style.overflow = 'visible';
    const div = document.createElement('div');
    div.style.cssText = `width:300px;height:60px;display:flex;align-items:center;justify-content:center;color:${color};font-size:${size}px;pointer-events:none`;
    katex.render(tex, div, { throwOnError: false });
    fo.appendChild(div);
    return fo;
  }

  // A draggable handle at the tip of a vector. get() returns its current
  // position, set(p) is called with the snapped new position while dragging.
  handle(get, set, { snap = 1, color = role('ink'), clamp = true } = {}) {
    const c = svgEl('circle', { r: 16, fill: color, 'fill-opacity': 0.18, stroke: color, 'stroke-width': 2, class: 'handle' }, this.handles);
    const place = () => { const [x, y] = this.px(get()); c.setAttribute('cx', x); c.setAttribute('cy', y); };
    const { xmin, xmax, ymin, ymax } = this.o;
    const move = (ev) => {
      let [x, y] = this.fromEvent(ev);
      x = Math.round(x / snap) * snap;
      y = Math.round(y / snap) * snap;
      if (clamp) { x = Math.min(xmax, Math.max(xmin, x)); y = Math.min(ymax, Math.max(ymin, y)); }
      set([+x.toFixed(4), +y.toFixed(4)]);
    };
    c.addEventListener('pointerdown', (ev) => {
      ev.preventDefault();
      ev.stopPropagation();
      c.setPointerCapture(ev.pointerId);
      c.addEventListener('pointermove', move);
      c.addEventListener('pointerup', () => c.removeEventListener('pointermove', move), { once: true });
    });
    place();
    return { el: c, place };
  }
};

// Number formatting for readouts: integers stay integers, everything else
// gets at most two decimals with trailing zeros dropped.
window.fmt = (n) => {
  const r = Math.round(n * 100) / 100;
  return (Object.is(r, -0) ? 0 : r).toString().replace('-', '{-}');
};

// A 2D column vector in TeX, each entry optionally coloured by a CSS colour.
window.colvec = ([x, y], cx, cy) => {
  const c = (col, s) => (col ? `\\textcolor{${col}}{${s}}` : s);
  return `\\begin{bmatrix} ${c(cx, fmt(x))} \\\\ ${c(cy, fmt(y))} \\end{bmatrix}`;
};

// A colour role from shared/css/custom.css as a concrete hex string.
window.role = (name) => getComputedStyle(document.documentElement).getPropertyValue('--' + name).trim();
