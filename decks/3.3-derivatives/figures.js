// Interactive figures for Block 3.3. See shared/js/plane.js.

const tc = (name, tex) => `\\textcolor{${role(name)}}{${tex}}`;

// Walk theta along the sin graph and read the slope off the cos graph.
// The slope triangle over a run of 1 rises by cos(theta); the bar standing
// on the axis at the same theta has exactly that height, and its tip is on
// the cos curve. Sweeping theta draws cos out of the slopes of sin.
Figures.register('sine-slope-graph', (el) => {
  const TMIN = -0.3, TMAX = 6.3;
  const p = new Plane(el.querySelector('.plane-host'), {
    xmin: -0.35, xmax: 7.6, ymin: -1.5, ymax: 1.9, unit: 100,
  });
  const out = el.querySelector('.readout');
  const btn = el.querySelector('.sweep');
  let th = 0.6, timer = null;

  const draw = () => {
    const s = Math.sin(th), c = Math.cos(th);
    p.clear();
    p.label([Math.PI, 0], '\\pi', role('ink-faint'), { dy: 26, size: 22 });
    p.label([2 * Math.PI, 0], '2\\pi', role('ink-faint'), { dy: 26, size: 22 });

    // sin: the function being walked. cos: faint ahead of theta, solid behind.
    p.curve(Math.sin, role('v'), { width: 5 });
    p.curve(Math.cos, role('result'), { width: 4, opacity: 0.18 });
    p.curve(Math.cos, role('result'), { width: 5, to: th });
    p.label([3 * Math.PI / 2, -1], '\\sin\\theta', role('v'), { dy: 36, size: 26 });
    p.label([2 * Math.PI, 1], '\\cos\\theta', role('result'), { dy: -32, size: 26 });

    // The tangent at theta, and its rise over a run of 1.
    const tan = (x) => s + c * (x - th);
    const a = th;
    p.segment([th - 1.1, tan(th - 1.1)], [th + 1.3, tan(th + 1.3)], role('result'), { width: 2.5, dashed: true, opacity: 0.8 });
    p.segment([a, tan(a)], [a + 1, tan(a)], role('ink-dim'), { width: 3, dashed: false });
    p.segment([a + 1, tan(a)], [a + 1, tan(a + 1)], role('result'), { width: 7, dashed: false });
    p.label([a + 0.5, tan(a)], '1', role('ink-dim'), { dy: 24, size: 22 });

    // The same height, standing on the axis under the cos graph.
    p.segment([th, 0], [th, c], role('result'), { width: 7, dashed: false });
    p.segment([th, Math.min(0, c, s)], [th, Math.max(0, c, s)], role('ink-faint'), { width: 2, dashed: true, opacity: 0.6 });
    p.dot([th, s], role('v'), 8);
    p.dot([th, c], role('result'), 8);
    handle.place();

    katex.render(
      `\\begin{aligned}
        \\theta &= ${fmt(th)} \\\\
        \\text{slope of } ${tc('v', '\\sin\\theta')} &= ${tc('result', fmt(c))} \\\\
        ${tc('result', '\\cos\\theta')} &= ${tc('result', fmt(c))}
      \\end{aligned}`,
      out, { displayMode: true });
  };

  const handle = p.handle(() => [th, Math.sin(th)], (q) => {
    th = Math.min(TMAX, Math.max(TMIN, q[0]));
    draw();
  }, { snap: 0.05, color: role('v') });

  const stop = () => { clearInterval(timer); timer = null; btn.textContent = 'sweep'; };
  btn.addEventListener('click', () => {
    if (timer) return stop();
    btn.textContent = 'stop';
    if (th >= TMAX - 0.05) th = TMIN;
    timer = setInterval(() => {
      th = Math.min(TMAX, th + 0.03);
      draw();
      if (th >= TMAX) stop();
    }, 16);
  });

  draw();
});
