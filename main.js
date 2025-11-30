import { Gioco } from "./game.js";

const canvas = document.getElementById("gioco");
const gioco = new Gioco(canvas);

// Ciclo principale
function loop() {
    if (!gioco.running) return;
    gioco.aggiorna();
    gioco.disegna();
    requestAnimationFrame(loop);
}
loop();

// --- Controlli touch ---
let touching = false;

canvas.addEventListener("touchstart", muoviBarraTouch, { passive: false });
canvas.addEventListener("touchmove", muoviBarraTouch, { passive: false });
canvas.addEventListener("touchend", () => touching = false);

function muoviBarraTouch(e) {
    e.preventDefault();
    const touch = e.touches[0];
    const rect = canvas.getBoundingClientRect();
    gioco.barra.x = touch.clientX - rect.left - gioco.barra.larghezza / 2;

    // Limiti ai bordi del canvas
    if (gioco.barra.x < 0) gioco.barra.x = 0;
    if (gioco.barra.x > canvas.width - gioco.barra.larghezza)
        gioco.barra.x = canvas.width - gioco.barra.larghezza;

    touching = true;
}

