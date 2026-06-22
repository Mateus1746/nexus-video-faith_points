import os
import yaml
import json
import numpy as np
import glob
from PIL import Image, ImageDraw, ImageFilter
import scipy.io.wavfile as wav
import pictex

# API MovieLite 0.2.2 + Pictex 2.3.0 (SOTA 2026)
try:
    from movielite import VideoWriter, ImageClip, TextClip, AudioClip, vfx, afx
    MOVIELITE_AVAILABLE = True
except ImportError as e:
    MOVIELITE_AVAILABLE = False
    print(f"ERRO ao importar movielite: {e}")

class VideoEngine:
    def __init__(self, script_path, audio_dir="pipeline/sync_drive/audio_ready/video"):
        # Resolve path if script is in scripts/yaml/
        if not os.path.exists(script_path):
            potential_path = os.path.join("scripts/yaml", script_path)
            if os.path.exists(potential_path):
                script_path = potential_path

        with open(script_path, 'r', encoding='utf-8') as f:
            self.script = yaml.safe_load(f)
        
        self.metadata = self.script['metadata']
        self.segments = self.script['segments']
        self.audio_dir = audio_dir
        self.width = self.metadata.get('width', 1280)
        self.height = self.metadata.get('height', 720)
        self.fps = self.metadata.get('fps', 30)
        
        if not os.path.exists("assets/generated"):
            os.makedirs("assets/generated")
            
        self.generate_shared_assets()

    def generate_shared_assets(self):
        """Gera assets comuns como a máscara de bordas arredondadas."""
        self.generate_rounded_mask()
        self.generate_distressed_mask()

    def generate_rounded_mask(self):
        rect_w, rect_h = int(self.width * 0.85), int(self.height * 0.85)
        mask_img = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(mask_img)
        paste_x = (self.width - rect_w) // 2
        paste_y = (self.height - rect_h) // 2
        radius = int(80 * (self.height / 720.0))
        draw.rounded_rectangle(
            (paste_x, paste_y, paste_x + rect_w, paste_y + rect_h), 
            radius=radius, 
            fill=(255, 255, 255)
        )
        mask_img = mask_img.filter(ImageFilter.SMOOTH_MORE)
        mask_img.save("assets/generated/shared_mask.png")

    def generate_distressed_mask(self):
        """Gera uma máscara com bordas 'rasgadas' para o Fragment Protocol."""
        rect_w, rect_h = int(self.width * 0.80), int(self.height * 0.65)
        mask_img = Image.new('L', (self.width, self.height), 0)
        draw = ImageDraw.Draw(mask_img)
        
        x0 = (self.width - rect_w) // 2
        y0 = (self.height - rect_h) // 2
        x1, y1 = x0 + rect_w, y0 + rect_h
        
        # Desenhar base
        draw.rectangle([x0, y0, x1, y1], fill=255)
        
        # Adicionar ruído nas bordas (Efeito Rasgado)
        points = []
        # Top edge
        for x in range(x0, x1, 5):
            points.append((x, y0 + np.random.randint(-10, 10)))
        # Right edge
        for y in range(y0, y1, 5):
            points.append((x1 + np.random.randint(-10, 10), y))
        # Bottom edge
        for x in range(x1, x0, -5):
            points.append((x, y1 + np.random.randint(-10, 10)))
        # Left edge
        for y in range(y1, y0, -5):
            points.append((x0 + np.random.randint(-10, 10), y))
            
        draw.polygon(points, fill=255, outline=255)
        mask_img = mask_img.filter(ImageFilter.GaussianBlur(radius=2))
        mask_img.save("assets/generated/distressed_mask.png")

    def create_segment_clip(self, segment, index):
        start = segment['start_time']
        duration = segment['duration']
        bg_image_path = segment['bg_image']
        seg_type = segment['type']
        text = segment['text']

        # 1. Background com Ken Burns
        # Resolve path if image is in assets/source/
        if not os.path.exists(bg_image_path):
            potential_bg = os.path.join("assets/source", bg_image_path)
            if os.path.exists(potential_bg):
                bg_image_path = potential_bg

        img = Image.open(bg_image_path).resize((self.width, self.height), Image.Resampling.LANCZOS)
        temp_bg = f"assets/generated/temp_{index}.jpg"
        img.save(temp_bg)
        
        bg_clip = ImageClip(temp_bg, start=start, duration=duration)
        vfx.KenBurns(
            duration=duration, 
            start_scale=1.0, 
            end_scale=1.05, 
            start_position=(0, 0), 
            end_position=(0, 0)
        ).apply(bg_clip)
        vfx.Vignette(intensity=0.7, radius=0.6).apply(bg_clip)
        
        # Fragment Protocol: Use distressed mask for verses
        mask_path = "assets/generated/distressed_mask.png" if seg_type == "verse" else "assets/generated/shared_mask.png"
        mask_asset = ImageClip(mask_path, start=start, duration=duration)
        bg_clip.set_mask(mask_asset)

        # 2. Texto e Áudio Sincronizado
        clips = [bg_clip]
        
        # Procurar áudio
        segment_audio_dir = os.path.join(self.audio_dir, f"segment_{index}")
        audio_file = os.path.join(segment_audio_dir, f"segment_{index}.wav")
        
        if os.path.exists(audio_file):
            narration_audio = AudioClip(audio_file).set_start(start)
            clips.append(narration_audio)
        
        # Overlay de Texto com Cálculo Dinâmico de Espaço
        safe_w = int(self.width * 0.70)
        left_margin = (self.width - safe_w) // 2
        
        canvas = pictex.Canvas().width(safe_w).text_wrap("normal").text_align("center")
        
        # Ajuste de tamanhos para evitar corte - Brand Bible Standards
        scale = self.height / 720.0
        if seg_type == "verse":
            base_size = 34 if len(text) > 150 else 38
            f_size = int(base_size * scale)
            # Ivory Parchment text
            canvas.font_size(f_size).color("#F5F5DC").font_style("italic").padding(int(45 * scale)).background_color("#000000CC").border_radius(int(5 * scale))
        elif seg_type == "narration":
            base_size = 32 if len(text) > 250 else 36
            f_size = int(base_size * scale)
            canvas.font_size(f_size).color("#E0E0E0").font_weight("medium").padding(int(35 * scale)).background_color("#000000AA").border_radius(int(15 * scale))
        else: # macro
            f_size = int(80 * scale)
            # Sovereign Gold text
            canvas.font_size(f_size).color("#D4AF37").font_weight("bold")
        
        txt_clip = TextClip(text, start=start + 0.5, duration=duration - 1.0, canvas=canvas)
        
        tw, th = txt_clip.size
        pos_x = (self.width - tw) // 2
        pos_y = (self.height - th) // 2
        
        txt_clip.set_position((pos_x, pos_y))
        vfx.FadeIn(duration=1.5).apply(txt_clip)
        vfx.FadeOut(duration=1.0).apply(txt_clip)
        clips.append(txt_clip)

        return clips

    def run(self):
        all_clips = []
        for i, seg in enumerate(self.segments):
            print(f"📦 Processando segmento {i}: {seg['type']} ({seg['start_time']}s)")
            all_clips.extend(self.create_segment_clip(seg, i))
        
        # Trilha de Fundo (Drone C2)
        total_duration = self.segments[-1]['start_time'] + self.segments[-1]['duration']
        sr = 44100
        t = np.linspace(0, total_duration, int(sr * total_duration))
        wave = (0.12 * np.sin(2 * np.pi * 65 * t))
        wav_path = "assets/generated/master_drone.wav"
        wav.write(wav_path, sr, wave.astype(np.float32))
        
        master_audio = AudioClip(wav_path).set_start(0)
        all_clips.append(master_audio)
        
        output_file = os.path.join("exports", self.metadata['output_file'])
        print(f"🎬 Renderizando: {output_file} ({total_duration}s)...")
        
        writer = VideoWriter(output_file, fps=self.fps, size=(self.width, self.height))
        writer.add_clips(all_clips)
        writer.write(processes=4)
        print(f"✅ Vídeo gerado com sucesso: {output_file}")

if __name__ == "__main__":
    engine = VideoEngine("the_dungeon_protocol_5min.yaml")
    engine.run()
