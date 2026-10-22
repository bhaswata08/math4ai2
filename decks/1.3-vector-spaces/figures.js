// Interactive figures for Block 1.3. Each one is a pure function of its
// state: a handle or slider changes the state, then draw() rebuilds the
// plane's dynamic layer and the readout. See shared/js/plane.js.

const PLANE = { xmin: -5, xmax: 5, ymin: -3.5, ymax: 3.5, unit: 70 };

// v and w draggable, a and b from sliders. a v, then b w from its tip, and
// the combination from the origin.
Figures.register('combo', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  const sa = el.querySelector('input[data-k=a]');
  const sb = el.querySelector('input[data-k=b]');
  let v = [2, 1], w = [-1, 1], a = Number(sa.value), b = Number(sb.value);

  const draw = () => {
    const av = [a * v[0], a * v[1]];
    const bw = [b * w[0], b * w[1]];
    const s = [av[0] + bw[0], av[1] + bw[1]];
    p.clear();
    p.arrow([0, 0], v, role('v'), { opacity: 0.3, width: 3, head: 14 });
    p.arrow([0, 0], w, role('w'), { opacity: 0.3, width: 3, head: 14 });
    p.arrow([0, 0], av, role('v'));
    p.arrow(av, s, role('w'));
    p.arrow([0, 0], s, role('result'), { width: 7, head: 22 });
    hv.place(); hw.place();
    const c = (name, tex) => `\\textcolor{${role(name)}}{${tex}}`;
    katex.render(
      `${c('result', fmt(a))}\\,${c('v', '\\vec v')} + ${c('result', fmt(b))}\\,${c('w', '\\vec w')} = ${c('result', colvec(s))}`,
      out, { displayMode: true });
  };
  const hv = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  const hw = p.handle(() => w, (q) => { w = q; draw(); }, { color: role('w') });
  for (const [sl, set] of [[sa, (x) => { a = x; }], [sb, (x) => { b = x; }]]) {
    sl.addEventListener('input', () => { set(Number(sl.value)); draw(); });
    // Keep reveal's keyboard navigation from stealing arrow keys off the slider.
    sl.addEventListener('keydown', (e) => e.stopPropagation());
  }
  draw();
});

// v and w draggable. The span is shaded: the whole visible plane when they
// are independent, a line through the origin when they are parallel, and
// the origin alone when both are zero. Handles snap to integers, so the
// cross product is exact.
Figures.register('span', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  const verdict = el.querySelector('.verdict');
  let v = [2, 1], w = [1, 2];

  const draw = () => {
    const cross = v[0] * w[1] - v[1] * w[0];
    const zero = (u) => u[0] === 0 && u[1] === 0;
    p.clear();
    let text;
    if (cross !== 0) {
      const r = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
      r.setAttribute('x', 0); r.setAttribute('y', 0);
      r.setAttribute('width', p.w); r.setAttribute('height', p.h);
      r.setAttribute('fill', role('result')); r.setAttribute('fill-opacity', 0.14);
      p.layer.appendChild(r);
      text = 'span: the plane';
    } else if (!(zero(v) && zero(w))) {
      const d = zero(v) ? w : v;
      const far = 20 / Math.hypot(d[0], d[1]);
      p.segment([-far * d[0], -far * d[1]], [far * d[0], far * d[1]], role('result'),
        { width: 14, dashed: false, opacity: 0.4 });
      text = 'span: a line';
    } else {
      p.dot([0, 0], role('result'), 13);
      text = 'span: a point';
    }
    p.arrow([0, 0], v, role('v'));
    p.arrow([0, 0], w, role('w'));
    hv.place(); hw.place();
    const c = (name, tex) => `\\textcolor{${role(name)}}{${tex}}`;
    katex.render(`${c('v', colvec(v))}\\quad ${c('w', colvec(w))}`, out, { displayMode: true });
    verdict.textContent = text;
    verdict.dataset.sign = cross !== 0 ? 1 : 0;
  };
  const hv = p.handle(() => v, (q) => { v = q; draw(); }, { color: role('v') });
  const hw = p.handle(() => w, (q) => { w = q; draw(); }, { color: role('w') });
  draw();
});
