// ============================================================
// THE DUNGEON PROTOCOL - FAITH POINTS FRONTEND ENGINE (SOTA 2026)
// ============================================================

const segments = [
  { type: "narration", text: "What if your current effort is completely invisible to the world? What if your silence isn't a failure of destiny, but a calculated deployment of time?", duration: 15, start_time: 0, bg_image: "Stone_room_with_oil_lamp_202606151120.jpeg" },
  { type: "macro", text: "STRATEGIC INVISIBILITY", duration: 10, start_time: 15, bg_image: "Stone_room_with_oil_lamp_202606151120.jpeg" },
  { type: "narration", text: "The mistake most people make when analyzing Joseph is believing he succeeded because he was a victim. He didn't. He succeeded because he learned to manage scarcity in the darkness of a dungeon.", duration: 20, start_time: 25, bg_image: "Ancient_scrolls_and_tablet_202606151120.jpeg" },
  { type: "verse", text: "But the Lord was with Joseph, and shewed him mercy, and gave him favour in the sight of the keeper of the prison. - Genesis 39:21", duration: 15, start_time: 45, bg_image: "Ancient_scrolls_and_tablet_202606151120.jpeg" },
  { type: "narration", text: "The prison was not a punishment; it was a laboratory. It was the only environment where Joseph could master the mechanics of administration without the noise of the palace. Anonymity is the only soil where true leadership capability is pressure-tested.", duration: 30, start_time: 60, bg_image: "Stone_room_with_oil_lamp_202606151120.jpeg" },
  { type: "macro", text: "THE INCUBATION PHASE", duration: 15, start_time: 90, bg_image: "Stone_room_with_oil_lamp_202606151120.jpeg" },
  { type: "narration", text: "In the void, Joseph stopped being a dreamer and started being an operator. He managed the prisoners, the logistics, and the morale of the forgotten. He optimized a failing system until he became the system itself.", duration: 30, start_time: 105, bg_image: "Ancient_scrolls_and_tablet_202606151120.jpeg" },
  { type: "narration", text: "When the king finally called, Joseph didn't offer a religious platitude. He offered a 14-year economic protocol. He identified a systemic collapse—the coming famine—and proposed a solution based on state-level hoarding and distribution.", duration: 30, start_time: 135, bg_image: "Geopolitical_command_and_control_center_202605041546.jpeg" },
  { type: "macro", text: "SCARCITY PROTOCOL", duration: 15, start_time: 165, bg_image: "Geopolitical_command_and_control_center_202605041546.jpeg" },
  { type: "narration", text: "He turned a natural disaster into a geopolitical consolidation of power. By the end of the famine, the Pharaoh owned the land, the livestock, and the people—all because one man knew how to manage bread in the dark.", duration: 30, start_time: 180, bg_image: "War_room_with_holographic_maps_202606151120.jpeg" },
  { type: "narration", text: "If you are in a season of obscurity, do not rush to the light. The palace has no room for amateurs. It only has room for those who have already mastered the dungeon.", duration: 30, start_time: 210, bg_image: "Desert_landscape_with_ruins_202606151120.jpeg" },
  { type: "narration", text: "Your current invisibility is not a malfunction. It is a dam holding back the force before your ascent. Stop looking for applause and start looking for the levers of your current prison.", duration: 30, start_time: 240, bg_image: "Stone_room_with_oil_lamp_202606151120.jpeg" },
  { type: "narration", text: "Master the small logistics of your void. Build your capability in secret. When the protocol of your promotion is activated, the world will see the results—but they will never understand the process.", duration: 20, start_time: 270, bg_image: "Throne_room_with_crown_shadows_202606151120.jpeg" },
  { type: "macro", text: "MASTER THE VOID", duration: 10, start_time: 290, bg_image: "Desert_landscape_with_ruins_202606151120.jpeg" }
];

const totalDuration = 300; // 5 minutos
const canvas = document.getElementById("video-canvas");
const ctx = canvas.getContext("2d");
const hudTime = document.getElementById("hud-time");
const hudSegment = document.getElementById("hud-segment");

// Pré-carregamento total de texturas na RAM
const textureCache = {};
let texturesLoaded = 0;
const uniqueImages = [...new Set(segments.map(s => s.bg_image))];

function preloadImages() {
    return new Promise((resolve) => {
        uniqueImages.forEach(imgName => {
            const img = new Image();
            img.src = `../assets/source/${imgName}`;
            img.onload = () => {
                textureCache[imgName] = img;
                texturesLoaded++;
                if (texturesLoaded === uniqueImages.length) {
                    console.log("🎨 All background textures preloaded in memory.");
                    resolve();
                }
            };
            img.onerror = () => {
                console.error(`❌ Failed to load asset: ${imgName}. Generating fallback...`);
                // Fallback de canvas colorido caso a imagem falhe
                const fallbackCanvas = document.createElement("canvas");
                fallbackCanvas.width = 1920;
                fallbackCanvas.height = 1080;
                const fCtx = fallbackCanvas.getContext("2d");
                fCtx.fillStyle = "#111827"; // Dark gray background fallback
                fCtx.fillRect(0, 0, 1920, 1080);
                textureCache[imgName] = fallbackCanvas;
                texturesLoaded++;
                if (texturesLoaded === uniqueImages.length) {
                    resolve();
                }
            };
        });
    });
}

// Lógica de Renderização de Frame Único determinístico
function renderFrameAtTime(t) {
    // Encontrar segmento ativo
    const segIdx = segments.findIndex(s => t >= s.start_time && t < s.start_time + s.duration);
    if (segIdx === -1) return;

    const segment = segments[segIdx];
    const segmentProgress = (t - segment.start_time) / segment.duration;

    // Limpar fundo do Canvas global
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // --- MÁSCARA COM BORDAS ARREDONDADAS (Safe Margins 85%) ---
    ctx.save();
    ctx.beginPath();
    const rectW = canvas.width * 0.85;
    const rectH = canvas.height * 0.85;
    const rx = (canvas.width - rectW) / 2;
    const ry = (canvas.height - rectH) / 2;
    ctx.roundRect(rx, ry, rectW, rectH, 80);
    ctx.clip();

    // Desenhar Imagem de Fundo (Ken Burns interpolado)
    const img = textureCache[segment.bg_image];
    if (img) {
        // Escala Ken Burns vai de 1.0 a 1.05
        const scale = 1.0 + segmentProgress * 0.05;
        const dw = canvas.width * scale;
        const dh = canvas.height * scale;
        const dx = (canvas.width - dw) / 2;
        const dy = (canvas.height - dh) / 2;
        ctx.drawImage(img, dx, dy, dw, dh);
    }

    // Vignette (Escurecimento suave das bordas)
    const grad = ctx.createRadialGradient(
        canvas.width / 2, canvas.height / 2, canvas.height / 3,
        canvas.width / 2, canvas.height / 2, canvas.width / 1.5
    );
    grad.addColorStop(0, "rgba(0, 0, 0, 0)");
    grad.addColorStop(1, "rgba(0, 0, 0, 0.75)");
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.restore(); // Finaliza a região da máscara arredondada

    // Desenhar borda de contorno da máscara para estética de moldura (opcional)
    ctx.strokeStyle = "rgba(212, 175, 55, 0.2)";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.roundRect(rx, ry, rectW, rectH, 80);
    ctx.stroke();

    // --- OVERLAY DE TEXTO ---
    // Fade in (1.5s) e Fade out (1.0s) de acordo com o main.py
    let alpha = 1.0;
    const textStart = segment.start_time + 0.5;
    const textEnd = segment.start_time + segment.duration - 1.0;

    if (t < textStart) {
        alpha = Math.max(0, (t - segment.start_time) / 0.5);
    } else if (t > textEnd) {
        alpha = Math.max(0, 1.0 - (t - textEnd) / 1.0);
    }

    if (alpha > 0.01) {
        const safeW = canvas.width * 0.70;
        drawTextCard(ctx, segment.text, canvas.width / 2, canvas.height / 2, safeW, segment.type, alpha);
    }

    // --- TELEMETRIA HUD ---
    hudTime.innerText = `${t.toFixed(2)}s`;
    hudSegment.innerText = `${segIdx + 1} / ${segments.length}`;
}

// Renderizador e wrapper de layout de texto no Canvas
function drawTextCard(ctx, text, cx, cy, maxW, type, alpha) {
    ctx.save();
    ctx.globalAlpha = alpha;

    let fontSize = 38;
    let fontStyle = "normal";
    let fontWeight = "400";
    let fontColor = "#ffffff";
    let cardColor = "rgba(0, 0, 0, 0)";
    let borderRadius = 0;
    let padding = 45;

    // Layout com base no tipo de segmento (Sovereign Gold / Ivory Parchment)
    if (type === "verse") {
        fontSize = 38;
        fontStyle = "italic";
        fontColor = "#F5F5DC"; // Ivory
        cardColor = "rgba(0, 0, 0, 0.8)";
        borderRadius = 30;
    } else if (type === "narration") {
        fontSize = 34;
        fontWeight = "500";
        fontColor = "#E2E8F0";
        cardColor = "rgba(0, 0, 0, 0.65)";
        borderRadius = 15;
    } else if (type === "macro") {
        fontSize = 80;
        fontWeight = "900";
        fontColor = "#D4AF37"; // Sovereign Gold
    }

    ctx.font = `${fontStyle} ${fontWeight} ${fontSize}px 'Outfit'`;
    ctx.textAlign = "center";
    ctx.textBaseline = "middle";

    // Quebra de texto inteligente em linhas
    const words = text.split(" ");
    const lines = [];
    let currentLine = "";

    for (let word of words) {
        let testLine = currentLine + word + " ";
        let testWidth = ctx.measureText(testLine).width;
        if (testWidth > maxW - padding * 2 && currentLine !== "") {
            lines.push(currentLine.trim());
            currentLine = word + " ";
        } else {
            currentLine = testLine;
        }
    }
    lines.push(currentLine.trim());

    const lineHeight = fontSize * 1.4;
    const cardH = lines.length * lineHeight + padding * 2;
    const cardW = maxW;
    const rx = cx - cardW / 2;
    const ry = cy - cardH / 2;

    if (cardColor !== "rgba(0, 0, 0, 0)") {
        ctx.fillStyle = cardColor;
        ctx.beginPath();
        ctx.roundRect(rx, ry, cardW, cardH, borderRadius);
        ctx.fill();
    }

    ctx.fillStyle = fontColor;
    let py = cy - (lines.length - 1) * lineHeight / 2;
    for (let line of lines) {
        ctx.fillText(line, cx, py);
        py += lineHeight;
    }

    ctx.restore();
}

// --- CONTROLE DE ÁUDIO REAL-TIME (OPCIONAL LIVE VIEW) ---
let audioCtx = null;
let oscillator = null;
let gainNode = null;

function startLiveAudio() {
    try {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        oscillator = audioCtx.createOscillator();
        gainNode = audioCtx.createGain();
        
        oscillator.type = "sine";
        oscillator.frequency.value = 65; // Drone C2 de 65Hz do main.py
        
        gainNode.gain.value = 0.12; // Volume da trilha
        
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        oscillator.start();
        console.log("🔊 Live Audio Drone running at 65Hz.");
    } catch (e) {
        console.warn("Audio Context block by autoplay policies.");
    }
}

// --- PROTOCOLO DE GRAVAÇÃO HYPERFRAMES ---
let initialized = false;

window.__hf = {
    duration: totalDuration,
    seek: async (timeSeconds) => {
        if (!initialized) {
            await preloadImages();
            initialized = true;
        }
        renderFrameAtTime(timeSeconds);
        await new Promise(resolve => requestAnimationFrame(resolve));
    }
};

window.renderFrame = async (timeMs) => {
    await window.__hf.seek(timeMs / 1000);
};

// Auto inicialização em live view no navegador
window.onload = async () => {
    await preloadImages();
    initialized = true;
    
    // Se não estiver em modo headless, executa o loop real-time
    const isHeadless = new URLSearchParams(window.location.search).get("headless") === "true";
    if (!isHeadless) {
        let startTime = performance.now();
        document.body.addEventListener("click", () => {
            if (!audioCtx) startLiveAudio();
        }, { once: true });

        function loop() {
            let elapsed = (performance.now() - startTime) / 1000;
            if (elapsed > totalDuration) {
                startTime = performance.now();
                elapsed = 0;
            }
            renderFrameAtTime(elapsed);
            requestAnimationFrame(loop);
        }
        loop();
    }
};
