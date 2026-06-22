# TRACE: Portabilidade e Correções — faith_points

## Registro de Decisões Causal

### [DECISION]
Portabilidade da pipeline estática baseada em MoviePy/Python para uma interface nativa HTML5/Canvas 2D, com renderização de Ken Burns, máscaras vetoriais dinâmicas e quebra de linhas para os cards de texto de versículos e narração, com suporte ao protocolo `window.__hf`.

### [RATIONALE]
* A pipeline Python (`create_video.py` / `main.py`) dependia da compilação de pacotes complexos de processamento como `scipy`, `pictex` e `movielite`, o que gerava alta fricção de dependências e instabilidade em CPUs locais.
* A renderização nativa de clipes e máscaras foi simplificada no navegador através do vetor de desenho `ctx.roundRect` e `ctx.clip` do Canvas 2D, eliminando o I/O de arquivos PNG adicionais.
* Os textos de versículos usam a fonte "Outfit" com a especificação Ivory Parchment (`#F5F5DC`) itálica e as narrações usam a cor cinza (`#E2E8F0`), seguindo rigorosamente a Brand Bible.

### [CONSEQUENCE]
* O projeto foi portado para Web de forma 100% autônoma na subpasta `./web`.
* A renderização agora é determinística, leve e compatível com a CLI headless.

### Decisão: Eliminação Completa do Google Colab e Automação Local Unificada (SOTA 2026)
`[DECISION] -> [RATIONALE] -> [CONSEQUENCE]`
* **DECISION**: Migrar o fluxo de áudio do Colab para síntese local via Kokoro (usando os DNAs de voz `.pt` no Drive) e utilizar o `Engine-Headless-Recorder` no lugar de compilação por CPU do FFmpeg.
* **RATIONALE**: A esteira anterior exigia sincronização manual e processamento externo lento. Com o Kokoro local e a gravação via Puppeteer Headless Canvas, alcançamos velocidades de renderização acima de **~85 FPS** de forma 100% automatizada e offline.
* **CONSEQUENCE**: Pipeline unificado e executado em um único comando: `uv run python conductor/run_pipeline.py`.
