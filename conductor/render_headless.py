import os
import subprocess
import wave
import contextlib
import sys

def render_story(factory, scene_id, **kwargs):
    print(f"🎬 Iniciando Renderização Headless para {factory} / {scene_id}...")
    
    wav_path = f"pipeline/sync_drive/audio_ready/{factory}/{scene_id}/roteiro.wav"
    output_path = f"pipeline/sync_drive/exports/{factory}_{scene_id}.mp4"

    if not os.path.exists(wav_path):
        print(f"❌ Erro: Áudio não encontrado em {wav_path}")
        return False

    with contextlib.closing(wave.open(wav_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        duration = frames / float(rate)
    
    duration_rounded = round(duration + 0.2, 2)
    print(f"⏱️ Duração do áudio detectada: {duration_rounded}s")

    print("🎥 Executando Engine-Headless-Recorder...")
    recorder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../tools/Engine-Headless-Recorder/src/node/record_video.js"))
    
    cmd = [
        "node", recorder_path,
        "--project=web",
        "--canvas=#video-canvas",
        f"--duration={duration_rounded}",
        "--fps=25",
        f"--output={output_path}"
    ]
    
    print(f"🚀 Rodando comando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)
    print(f"🎉 Sucesso! Vídeo gravado e salvo em: {output_path}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python render_headless.py <factory> <scene_id>")
        sys.exit(1)
    
    factory = sys.argv[1]
    scene_id = sys.argv[2]
    render_story(factory, scene_id)
