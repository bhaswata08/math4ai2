// Interactive figures for Block 1.4. Each one is a pure function of its
// state: a handle changes the state, then draw() rebuilds the plane's
// dynamic layer and the readout. See shared/js/plane.js.

const PLANE = { xmin: -5, xmax: 5, ymin: -3.5, ymax: 3.5, unit: 70 };

// b1, b2 and a target x are draggable. The grid of a b1 + b b2 for integer
// a, b is drawn faint; the readout solves x = a b1 + b b2 for a and b by
// Cramer's rule, or says b1, b2 are parallel when the determinant is 0.
Figures.register('basis', (el) => {
  const p = new Plane(el.querySelector('.plane-host'), PLANE);
  const out = el.querySelector('.readout');
  const verdict = el.querySelector('.verdict');
  let b1 = [2, 1], b2 = [-1, 1], x = [3, 2];

  const draw = () => {
    const det = b1[0] * b2[1] - b1[1] * b2[0];
    const c = (name, tex) => `\\textcolor{${role(name)}}{${tex}}`;
    p.clear();
    if (Math.abs(det) < 1e-9) {
      p.arrow([0, 0], b1, role('v'));
      p.arrow([0, 0], b2, role('w'));
      p.arrow([0, 0], x, role('result'), { width: 6, head: 20 });
      hb1.place(); hb2.place(); hx.place();
      katex.render(`${c('v', '\\vec b_1')}\\ \\text{and}\\ ${c('w', '\\vec b_2')}\\ \\text{are parallel}`, out, { displayMode: true });
      verdict.textContent = 'b1 and b2 are parallel: not a basis';
      verdict.dataset.sign = 0;
      return;
    }
    const a = (x[0] * b2[1] - x[1] * b2[0]) / det;
    const b = (b1[0] * x[1] - b1[1] * x[0]) / det;
    // Grid: for each integer k, the line k b1 + t b2 and the line t b1 + k b2.
    // The range of k comes from the plane's corners in (a, b) coordinates.
    const { xmin, xmax, ymin, ymax } = p.o;
    let amin = Infinity, amax = -Infinity, bmin = Infinity, bmax = -Infinity;
    for (const [cx, cy] of [[xmin, ymin], [xmin, ymax], [xmax, ymin], [xmax, ymax]]) {
      const ca = (cx * b2[1] - cy * b2[0]) / det;
      const cb = (b1[0] * cy - b1[1] * cx) / det;
      amin = Math.min(amin, ca); amax = Math.max(amax, ca);
      bmin = Math.min(bmin, cb); bmax = Math.max(bmax, cb);
    }
    const far = 60;
    const gridLine = (o, d) => p.segment(
      [o[0] - far * d[0], o[1] - far * d[1]], [o[0] + far * d[0], o[1] + far * d[1]],
      role('ink-faint'), { width: 1.5, dashed: false, opacity: 0.55 });
    const cap = (lo, hi) => [Math.max(Math.floor(lo), -40), Math.min(Math.ceil(hi), 40)];
    const [a0, a1] = cap(amin, amax), [c0, c1] = cap(bmin, bmax);
    for (let k = a0; k <= a1; k++) gridLine([k * b1[0], k * b1[1]], b2);
    for (let k = c0; k <= c1; k++) gridLine([k * b2[0], k * b2[1]], b1);

    const ab1 = [a * b1[0], a * b1[1]];
    p.arrow([0, 0], b1, role('v'));
    p.arrow([0, 0], b2, role('w'));
    p.arrow([0, 0], ab1, role('v'), { opacity: 0.45, width: 9, head: 14 });
    p.arrow(ab1, x, role('w'), { opacity: 0.45, width: 9, head: 14 });
    p.arrow([0, 0], x, role('result'), { width: 6, head: 20 });
    hb1.place(); hb2.place(); hx.place();
    katex.render(
      `${c('result', colvec(x))} = ${c('result', fmt(a))}\\,${c('v', '\\vec b_1')} + ${c('result', fmt(b))}\\,${c('w', '\\vec b_2')}`,
      out, { displayMode: true });
    verdict.textContent = `coordinates in this basis: (${fmt(a).replace('{-}', '−')}, ${fmt(b).replace('{-}', '−')})`;
    verdict.dataset.sign = 1;
  };
  // Draw order: handles last, so x sits on top.
  const hb1 = p.handle(() => b1, (q) => { b1 = q; draw(); }, { color: role('v') });
  const hb2 = p.handle(() => b2, (q) => { b2 = q; draw(); }, { color: role('w') });
  const hx = p.handle(() => x, (q) => { x = q; draw(); }, { color: role('result') });
  draw();
});
