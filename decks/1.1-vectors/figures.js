// Interactive figures for Block 1.1. Each one is a pure function of its
// state: a handle changes the state, then draw() rebuilds the plane's
// dynamic layer and the readout. See shared/js/plane.js.

const PLANE = { xmin: -5, xmax: 5, ymin: -3.5, ymax: 3.5, unit: 70 };

// One draggable vector, its x and y components, and the column it reads as.
Figures.register('coords', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  let v = [3, -1];

  const draw = () => {
    p.clear();
    p.segment([0, 0], [v[0], 0], role('x'), { width: 4 });
    p.segment([v[0], 0], v, role('y'), { width: 4 });
    p.arrow([0, 0], v, role('v'));
    tip.place();
    katex.render(`\\textcolor{${role('v')}}{\\vec v} = ${colvec(v, role('x'), role('y'))}`, out);
  };
  const tip = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  draw();
});

// v and w, both draggable. The sum, and a faded copy of w moved to v's tip.
Figures.register('add', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  let v = [1, 2], w = [3, -1];

  const draw = () => {
    const s = [v[0] + w[0], v[1] + w[1]];
    p.clear();
    p.arrow(v, s, role('w'), { opacity: 0.45, dashed: true });
    p.arrow([0, 0], s, role('result'));
    p.arrow([0, 0], v, role('v'));
    p.arrow([0, 0], w, role('w'));
    hv.place(); hw.place();
    const c = (name, tex) => `\\textcolor{${role(name)}}{${tex}}`;
    katex.render(
      `${c('v', colvec(v))} + ${c('w', colvec(w))} = ${c('result', colvec(s))}`,
      out, { displayMode: true });
  };
  const hv = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  const hw = p.handle(() => w, (q) => { w = q; draw(); }, { color: role('w') });
  draw();
});

// v draggable, c from the slider. Shows the line through v so that every
// c v visibly stays on it.
Figures.register('scale', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  const slider = el.querySelector('input[type=range]');
  let v = [2, 1], c = Number(slider.value);

  const draw = () => {
    const cv = [c * v[0], c * v[1]];
    p.clear();
    const n = Math.hypot(v[0], v[1]);
    if (n > 0) {
      const far = 20 / n;
      p.segment([-far * v[0], -far * v[1]], [far * v[0], far * v[1]], role('ink-faint'), { width: 2 });
    }
    p.arrow([0, 0], cv, role('result'), { width: 7, head: 22 });
    p.arrow([0, 0], v, role('v'));
    hv.place();
    katex.render(
      `\\textcolor{${role('result')}}{${fmt(c)}} \\textcolor{${role('v')}}{${colvec(v)}} = \\textcolor{${role('result')}}{${colvec(cv)}}`,
      out, { displayMode: true });
  };
  const hv = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  slider.addEventListener('input', () => { c = Number(slider.value); draw(); });
  // Keep reveal's keyboard navigation from stealing arrow keys off the slider.
  slider.addEventListener('keydown', (e) => e.stopPropagation());
  draw();
});

// v and w draggable. w is dropped onto the line through v; the readout
// shows the entry-by-entry sum and the verdict reads the sign as an angle.
Figures.register('dot', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  const verdict = el.querySelector('.verdict');
  let v = [3, 1], w = [1, 2];

  const draw = () => {
    const d = v[0] * w[0] + v[1] * w[1];
    const vv = v[0] * v[0] + v[1] * v[1];
    p.clear();
    if (vv > 0) {
      const far = 20 / Math.sqrt(vv);
      p.segment([-far * v[0], -far * v[1]], [far * v[0], far * v[1]], role('ink-faint'), { width: 2 });
      const proj = [(d / vv) * v[0], (d / vv) * v[1]];
      p.segment(w, proj, role('w'), { width: 2.5 });
    }
    p.arrow([0, 0], v, role('v'));
    p.arrow([0, 0], w, role('w'));
    // The projection goes on top of v, or v's shaft hides it whenever it is
    // shorter than v.
    if (vv > 0) p.segment([0, 0], [(d / vv) * v[0], (d / vv) * v[1]], role('result'), { width: 9, dashed: false, opacity: 0.85 });
    hv.place(); hw.place();
    const c = (name, tex) => `\\textcolor{${role(name)}}{${tex}}`;
    katex.render(
      `${c('v', colvec(v))} \\cdot ${c('w', colvec(w))} = ` +
      `${fmt(v[0])} \\cdot ${fmt(w[0])} + ${fmt(v[1])} \\cdot ${fmt(w[1])} = ${c('result', fmt(d))}`,
      out, { displayMode: true });
    verdict.textContent = d > 0 ? 'positive: roughly the same direction'
      : d < 0 ? 'negative: roughly opposite' : 'zero: perpendicular';
    verdict.dataset.sign = Math.sign(d);
  };
  const hv = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  const hw = p.handle(() => w, (q) => { w = q; draw(); }, { color: role('w') });
  draw();
});
