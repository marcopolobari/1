// --------------------------------------------------
// Colori
// --------------------------------------------------
class Colori {
    static NERO = "#000000";
    static BIANCO = "#FFFFFF";
    static VERDE = "#00FF00";
}

// --------------------------------------------------
// Barra
// --------------------------------------------------
class Barra {
    constructor(x, y, larghezzaSchermo) {
        this.x = x;
        this.y = y;
        this.larghezza = 80;
        this.altezza = 10;
        this.velocita = 6;
        this.larghezzaSchermo = larghezzaSchermo;
    }

    muoviSinistra() {
        if (this.x > 0) this.x -= this.velocita;
    }

    muoviDestra() {
        if (this.x < this.larghezzaSchermo - this.larghezza)
            this.x += this.velocita;
    }

    disegna(ctx) {
        ctx.fillStyle = Colori.BIANCO;
        ctx.fillRect(this.x, this.y, this.larghezza, this.altezza);
    }
}

// --------------------------------------------------
// Pallina
// --------------------------------------------------
class Pallina {
    constructor(x, y, w, h) {
        this.x = x;
        this.y = y;
        this.dx = 3;
        this.dy = -3;
        this.raggio = 5;
        this.w = w;
        this.h = h;
    }

    muovi() {
        this.x += this.dx;
        this.y += this.dy;

        if (this.x <= 0 || this.x >= this.w) this.dx = -this.dx;
        if (this.y <= 0) this.dy = -this.dy;
        if (this.y > this.h) this.reset();
    }

    reset() {
        this.x = 300;
        this.y = 200;
        this.dy = -3;
    }

    disegna(ctx) {
        ctx.fillStyle = Colori.BIANCO;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.raggio, 0, Math.PI * 2);
        ctx.fill();
    }
}

// --------------------------------------------------
// Mattone
// --------------------------------------------------
class Mattone {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.w = 55;
        this.h = 15;
        this.attivo = true;
    }

    disegna(ctx) {
        if (this.attivo) {
            ctx.fillStyle = Colori.VERDE;
            ctx.fillRect(this.x, this.y, this.w, this.h);
        }
    }

    collide(ball) {
        return (
            this.attivo &&
            ball.x > this.x &&
            ball.x < this.x + this.w &&
            ball.y > this.y &&
            ball.y < this.y + this.h
        );
    }
}

// --------------------------------------------------
// Gruppo Mattoni
// --------------------------------------------------
class GruppoMattoni {
    constructor() {
        this.mattoni = [];
        this.crea();
    }

    crea() {
        for (let r = 0; r < 5; r++) {
            for (let c = 0; c < 10; c++) {
                this.mattoni.push(new Mattone(c * 60, r * 20 + 50));
            }
        }
    }

    disegna(ctx) {
        this.mattoni.forEach(m => m.disegna(ctx));
    }

    controllaCollisione(pallina) {
        for (let m of this.mattoni) {
            if (m.collide(pallina)) {
                m.attivo = false;
                return true;
            }
        }
        return false;
    }

    tuttiDistrutti() {
        return this.mattoni.every(m => !m.attivo);
    }
}

// --------------------------------------------------
// Gioco
// --------------------------------------------------
class Gioco {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext("2d");

        this.w = canvas.width;
        this.h = canvas.height;

        this.barra = new Barra(250, 350, this.w);
        this.pallina = new Pallina(300, 200, this.w, this.h);
        this.mattoni = new GruppoMattoni();

        this.running = true;

        document.addEventListener("keydown", e => {
            if (e.key === "ArrowLeft") this.barra.muoviSinistra();
            if (e.key === "ArrowRight") this.barra.muoviDestra();
        });
    }

    aggiorna() {
        this.pallina.muovi();

        // collisione barra
        if (
            this.pallina.y > this.barra.y &&
            this.pallina.x > this.barra.x &&
            this.pallina.x < this.barra.x + this.barra.larghezza
        ) {
            this.pallina.dy = -this.pallina.dy;
        }

        // collisione mattoni
        if (this.mattoni.controllaCollisione(this.pallina))
            this.pallina.dy = -this.pallina.dy;
    }

    disegna() {
        this.ctx.fillStyle = Colori.NERO;
        this.ctx.fillRect(0, 0, this.w, this.h);

        this.barra.disegna(this.ctx);
        this.pallina.disegna(this.ctx);
        this.mattoni.disegna(this.ctx);
    }
}

export { Gioco };
