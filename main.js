// --- Touch per smartphone ---
let touching = false;

canvas.addEventListener('touchstart', (e) => {
  touching = true;
  const t = e.touches[0];
  const rect = canvas.getBoundingClientRect();
  gioco.barra.x = t.clientX - rect.left - gioco.barra.larghezza / 2;
  e.preventDefault();
}, {passive: false});

canvas.addEventListener('touchmove', (e) => {
  if (!touching) return;
  const t = e.touches[0];
  const rect = canvas.getBoundingClientRect();
  gioco.barra.x = t.clientX - rect.left - gioco.barra.larghezza / 2;
  e.preventDefault();
}, {passive: false});

canvas.addEventListener('touchend', () => {
  touching = false;
}, {passive: true});
