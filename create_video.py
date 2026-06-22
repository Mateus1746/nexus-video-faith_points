import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import os
import sys
import scipy.io.wavfile as wav
import pictex
import multiprocessing

# API MovieLite 0.2.2 + Pictex 2.3.0 (SOTA 2026)
try:
    from movielite import VideoWriter, ImageClip, TextClip, AudioClip, vfx, afx, enums
    MOVIELITE_AVAILABLE = True
except ImportError as e:
    MOVIELITE_AVAILABLE = False
    print(f"ERRO ao importar movielite: {e}")

def generate_assets():
    """Gera áudio e máscara em 1080p."""
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # 1. Gerar Drone de Áudio
    sr = 44100
    duration = 10
    t = np.linspace(0, duration, int(sr * duration))
    wave = (0.5 * np.sin(2 * np.pi * 55 * t) + 0.3 * np.sin(2 * np.pi * 55.5 * t))
    wav.write("assets/drone.wav", sr, wave.astype(np.float32))

    # 2. Criar MÁSCARA de bordas arredondadas (1080p)
    width, height = 1920, 1080
    rect_w, rect_h = int(width * 0.85), int(height * 0.85)
    mask_img = Image.new('RGB', (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(mask_img)
    paste_x, paste_y = (width - rect_w) // 2, (height - rect_h) // 2
    draw.rounded_rectangle(
        (paste_x, paste_y, paste_x + rect_w, paste_y + rect_h), 
        radius=100, fill=(255, 255, 255)
    )
    mask_img = mask_img.filter(ImageFilter.SMOOTH_MORE)
    mask_img.save("assets/rounded_mask_1080p.png")

def create_optimized_video(output_name="faith_points_1080p_stable.mp4"):
    generate_assets()
    duration = 10
    width, height = 1920, 1080
    cores = multiprocessing.cpu_count()
    
    user_bg_path = "/home/mateus/.gemini/projetos/nexus_media/video/faith_points/Geopolitical_command_and_control_center_202605041546.jpeg"
    
    # 1. Carregar imagem diretamente para a memória (Zero Disk I/O)
    img_pil = Image.open(user_bg_path).resize((width, height), Image.Resampling.LANCZOS)
    img_array = np.array(img_pil)
    img_clip = ImageClip(img_array).set_duration(duration)
    
    vfx.KenBurns(duration=duration, start_scale=1.0, end_scale=1.05).apply(img_clip)
    vfx.Vignette(intensity=0.7, radius=0.6).apply(img_clip)
    
    # Aplicar Máscara
    mask_asset = ImageClip("assets/rounded_mask_1080p.png").set_duration(duration)
    img_clip.set_mask(mask_asset)

    # 2. Bible Verse (Safe Area 60%)
    safe_w = int(width * 0.60)
    left_margin = (width - safe_w) // 2
    bible_canvas = (
        pictex.Canvas()
        .width(safe_w)
        .text_wrap("normal")
        .font_size(54)
        .color("white")
        .font_style("italic")
        .text_align("center")
        .padding(50)
        .background_color("#000000CC") 
        .border_radius(30)
    )
    bible_text = "Wait for the Lord; be strong and take heart and wait for the Lord. - Psalm 27:14"
    txt_clip = TextClip(bible_text, start=1.5, duration=7.5, canvas=bible_canvas)
    txt_clip.set_position((left_margin, height // 2 - 120))
    vfx.FadeIn(duration=2.0).apply(txt_clip)

    # 3. Áudio
    audio = AudioClip("assets/drone.wav").set_start(0)

    # 4. Renderização Otimizada (Multi-Core)
    print(f"🚀 Renderizando em 1080p ({cores} Cores)...")
    writer = VideoWriter(
        output_name, 
        fps=30, 
        size=(width, height)
    )
    writer.add_clips([img_clip, txt_clip, audio])
    
    # Otimização: uint8 e paralelismo total
    writer.write(
        processes=cores, 
        video_quality=enums.VideoQuality.HIGH,
        high_precision_blending=False
    )
    print(f"✅ Vídeo concluído: {output_name}")

if __name__ == "__main__":
    if MOVIELITE_AVAILABLE:
        create_optimized_video()
    else:
        print("\nErro de dependências. Execute: uv pip install movielite numpy pillow scipy pictex")
