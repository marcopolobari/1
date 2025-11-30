import { Gioco } from "./game.js";

const canvas = document.getElementById("gioco");
const gioco = new Gioco(canvas);

function loop() {
    if (!gioco.running) return;
    gioco.aggiorna();
    gioco.disegna();
    requestAnimationFrame(loop);
}

loop();
