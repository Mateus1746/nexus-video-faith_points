# Plano de Execução: Atualização de Resolução e Geração de Vídeos

## Objective
Aumentar a resolução dos vídeos gerados para 1080p (1920x1080) e renderizar todos os vídeos planejados no canal (`script_aitofel_5min.yaml` e `script_traicao.yaml`).

## Key Files & Context
- `script_aitofel_5min.yaml` e `script_traicao.yaml`: Arquivos de dados que geram os vídeos. Atualmente configurados para 1280x720.
- `main.py`: O motor principal (VideoEngine) que orquestra a geração.
- A engine atual utiliza tamanhos de fonte, margens e arredondamentos (*radius*) com valores "hardcoded" que funcionam bem em 720p, mas que ficariam desproporcionais ou pequenos em 1080p.

## Implementation Steps

1. **Ajuste Dinâmico de Escala (`main.py`)**
   - Atualizar `generate_shared_assets` para escalar o `radius` da máscara proporcionalmente à resolução (ex: `int(80 * (self.height / 720.0))`).
   - Atualizar `create_segment_clip` para calcular um `scale_factor = self.height / 720.0`.
   - Multiplicar os valores de `font_size`, `padding` e `border_radius` do Pictex por esse `scale_factor`.

2. **Atualização das Configurações**
   - No `script_aitofel_5min.yaml`, alterar `width` para 1920 e `height` para 1080.
   - No `script_traicao.yaml`, alterar `width` para 1920 e `height` para 1080.

3. **Geração (Renderização)**
   - Executar `python main.py` utilizando o `script_aitofel_5min.yaml` para gerar o primeiro vídeo em 1080p.
   - Modificar o `main.py` temporariamente ou passá-lo como argumento para executar também com o `script_traicao.yaml` e gerar o segundo vídeo.

## Verification & Testing
- Verificar se os arquivos MP4 gerados (`ahithophel_protocol_sovereign.mp4` e `gestao_da_traicao.mp4`) estão na resolução 1920x1080.
- Confirmar visualmente (ou pelas métricas) se a tipografia preenche o espaço corretamente como na versão 720p.