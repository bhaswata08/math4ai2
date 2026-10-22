// Interactive figures for Block 1.2. Each one is a pure function of its
// state: a handle changes the state, then draw() rebuilds the plane's
// dynamic layer and the readout. See shared/js/plane.js.

const PLANE = { xmin: -5, xmax: 5, ymin: -3.5, ymax: 3.5, unit: 70 };
const tc = (name, tex) => `\\textcolor{${role(name)}}{${tex}}`;
const dotp = (a, b) => a[0] * b[0] + a[1] * b[1];
const len = (a) => Math.hypot(a[0], a[1]);
// A line through v, long enough to leave the plane on both sides.
const lineThrough = (p, v, color) => {
  const n = len(v);
  if (n === 0) return;
  const far = 20 / n;
  p.segment([-far * v[0], -far * v[1]], [far * v[0], far * v[1]], color, { width: 2, dashed: false });
};

// One draggable vector and its three lengths. The L1 path runs along the
// grid, the L2 arrow is the straight line, and the L-infinity square is
// every point whose largest entry equals that of v.
Figures.register('norms', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  let v = [3, 2];

  const draw = () => {
    const a = Math.abs(v[0]), b = Math.abs(v[1]);
    const l1 = a + b, l2 = Math.hypot(v[0], v[1]), li = Math.max(a, b);
    p.clear();
    p.segment([-li, -li], [li, -li], role('accent'), { width: 2.5, opacity: 0.7 });
    p.segment([li, -li], [li, li], role('accent'), { width: 2.5, opacity: 0.7 });
    p.segment([li, li], [-li, li], role('accent'), { width: 2.5, opacity: 0.7 });
    p.segment([-li, li], [-li, -li], role('accent'), { width: 2.5, opacity: 0.7 });
    p.segment([0, 0], [v[0], 0], role('result'), { width: 4, dashed: false, opacity: 0.8 });
    p.segment([v[0], 0], v, role('result'), { width: 4, dashed: false, opacity: 0.8 });
    p.arrow([0, 0], v, role('v'));
    tip.place();
    const sq = Number.isInteger(l2) ? fmt(l2) : `\\sqrt{${fmt(v[0] * v[0] + v[1] * v[1])}} \\approx ${fmt(l2)}`;
    katex.render(
      `\\begin{aligned}
        ${tc('result', 'L_1')} &= |${fmt(v[0])}| + |${fmt(v[1])}| = ${tc('result', fmt(l1))} \\\\
        ${tc('v', 'L_2')} &= \\sqrt{(${fmt(v[0])})^2 + (${fmt(v[1])})^2} = ${tc('v', sq)} \\\\
        ${tc('accent', 'L_\\infty')} &= \\max(|${fmt(v[0])}|, |${fmt(v[1])}|) = ${tc('accent', fmt(li))}
      \\end{aligned}`,
      out, { displayMode: true });
  };
  const tip = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  draw();
});

// v and w draggable. The line through v, w dropped perpendicular onto it,
// and the shadow, with the formula filled in.
Figures.register('project', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  let v = [3, 1], w = [1, 2];

  const draw = () => {
    const d = dotp(v, w), vv = dotp(v, v);
    p.clear();
    lineThrough(p, v, role('ink-faint'));
    let pr = [0, 0];
    if (vv > 0) {
      pr = [(d / vv) * v[0], (d / vv) * v[1]];
      p.segment(w, pr, role('w'), { width: 2.5 });
    }
    p.arrow([0, 0], v, role('v'));
    p.arrow([0, 0], w, role('w'));
    if (vv > 0) p.segment([0, 0], pr, role('result'), { width: 9, dashed: false, opacity: 0.85 });
    hv.place(); hw.place();
    if (vv === 0) {
      katex.render('\\text{v is the zero vector: there is no line to project onto}', out, { displayMode: true });
      return;
    }
    katex.render(
      `\\operatorname{proj}_{${tc('v', 'v')}} ${tc('w', 'w')} = \\frac{${tc('v', 'v')} \\cdot ${tc('w', 'w')}}{${tc('v', 'v')} \\cdot ${tc('v', 'v')}} ${tc('v', 'v')}` +
      ` \\\\[0.5em] = \\frac{${fmt(d)}}{${fmt(vv)}} ${colvec(v)} = ${tc('result', colvec(pr))}`,
      out, { displayMode: true });
  };
  const hv = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  const hw = p.handle(() => w, (q) => { w = q; draw(); }, { color: role('w') });
  draw();
});

// v and w draggable. The angle between them as an arc, and cos of it.
Figures.register('cosine', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  let v = [3, 1], w = [1, 2];

  const draw = () => {
    p.clear();
    const nv = len(v), nw = len(w);
    p.arrow([0, 0], v, role('v'));
    p.arrow([0, 0], w, role('w'));
    hv.place(); hw.place();
    if (nv === 0 || nw === 0) {
      katex.render('\\text{a zero vector has no direction, so no angle}', out, { displayMode: true });
      return;
    }
    const d = dotp(v, w);
    const c = Math.max(-1, Math.min(1, d / (nv * nw)));
    const th = Math.acos(c) * 180 / Math.PI;
    // Arc from v's direction to w's, the short way round.
    const a0 = Math.atan2(v[1], v[0]);
    let da = Math.atan2(w[1], w[0]) - a0;
    while (da > Math.PI) da -= 2 * Math.PI;
    while (da < -Math.PI) da += 2 * Math.PI;
    const r = 0.9, pts = [];
    for (let i = 0; i <= 40; i++) {
      const [x, y] = p.px([r * Math.cos(a0 + da * i / 40), r * Math.sin(a0 + da * i / 40)]);
      pts.push(`${x},${y}`);
    }
    const arc = document.createElementNS('http://www.w3.org/2000/svg', 'polyline');
    arc.setAttribute('points', pts.join(' '));
    arc.setAttribute('fill', 'none');
    arc.setAttribute('stroke', role('accent'));
    arc.setAttribute('stroke-width', 4);
    p.layer.appendChild(arc);
    const mid = a0 + da / 2, lr = 1.45;
    p.label([lr * Math.cos(mid), lr * Math.sin(mid)], tc('accent', '\\theta'), role('accent'), { size: 30 });
    katex.render(
      `\\cos\\theta = \\frac{${tc('v', 'v')} \\cdot ${tc('w', 'w')}}{\\lVert ${tc('v', 'v')} \\rVert \\, \\lVert ${tc('w', 'w')} \\rVert}` +
      ` = \\frac{${fmt(d)}}{${fmt(nv)} \\cdot ${fmt(nw)}} = ${tc('result', fmt(c))} \\\\[0.5em]` +
      `\\theta = ${tc('accent', fmt(th) + '^\\circ')}`,
      out, { displayMode: true });
  };
  const hv = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  const hw = p.handle(() => w, (q) => { w = q; draw(); }, { color: role('w') });
  draw();
});
