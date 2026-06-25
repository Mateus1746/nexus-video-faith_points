# Guia de Execucao Autonoma (AGENTS)

Este arquivo define as regras de desenvolvimento e integracao para a fabrica de conteudo do projeto utilizando o Engine-Headless-Recorder.

## 1. Integracao com Gravador Headless

Para que o gravador headless em \`tools/Engine-Headless-Recorder/src/node/record_video.js\` consiga exportar a animacao deterministica do canvas corretamente, atente-se a:

- **Canvas Selector:** A aplicacao deve ter um elemento `<canvas>` disponivel no DOM. O seletor padrao procurado e `#nox-canvas`, mas se nao existir, o gravador usa o primeiro \`canvas\` que encontrar (\`document.querySelector('canvas')\`).
- **renderFrame API:** A aplicacao deve expor no contexto global (window) uma funcao sincrona/assincrona chamada \`renderFrame(timeMs)\` que avanca o estado do frame (graficos/animacoes) para o tempo em milissegundos passado por parametro.
- **initializeScene API:** Se houver pre-processamentos iniciais isolados ou especificos alem do carregamento assincrono puro, certifique-se de prever uma rotina \`initializeScene\` caso necessario no workflow. O ideal e que toda a cena ja esteja pronta ou em preparo no carregamento da janela ou quando requisitado.
- **__appReady Flag:** Uma vez que todas as imagens, fontes, shaders e dependencias assincronas terminarem de carregar (geralmente depois de preloads e/ou \`initializeScene\`), certifique-se de expor \`window.__appReady = true\` globalmente. O gravador pode ser programado para esperar este estado.
- **WebGL Context:** Se voce usa WebGL para desenhar as texturas, nao se esqueca de inicializar o contexto com a flag \`preserveDrawingBuffer: true\`. O gravador usa a API VideoFrame do WebCodecs que ira puxar os pixels da memoria do Canvas diretamente e, senao habilitada essa opcao em alguns cenarios de buffers nativos, os frames podem ser gravados pretos ou corrompidos.

## 2. Inicializacao e Assets (Copias Faltantes)

- O frontend busca todos os seus assets usando URLs ou o proprio gravador levanta um server estatico apontado para a raiz do monorepo, que as fabrica deve acessar.
- Qualquer fetch ou src (em imagens, modelos, audios) para dentro do diretorio \`assets/\` precisa ser validado. Se algum asset especifico estiver faltando na pasta de \`public/\` ou na propria pasta local, certifique-se de copia-los durante o ciclo de build.

## 3. Output do Build (npm run build)

- O projeto preve a existencia de um processo de bundle padrao. Se voce usar Node para processar o Frontend, lembre-se de configurar e usar os scripts do \`package.json\`. O comando \`npm run build\` deve conseguir colocar o index.html, JS processado, CSS e assets todos numa pasta comum (por exemplo, \`dist/\`, ou a ser servido do dir que o gravador chama).

## 4. Rodando o Gravador

Para gravar qualquer fabrica usando nosso Engine-Headless-Recorder (usualmente localizado em ferramentas), o comando padrao aceita argumentos por CLI de projeto, canvas, duracao e FPS:

\`\`\`bash
node tools/Engine-Headless-Recorder/src/node/record_video.js --canvas=#video-canvas --duration=<segundos> --output=pipeline/sync_drive/exports/output.mp4
\`\`\`

*(Nota: Alguns destes parametros e configuracoes sao especificos para as fabricas integradas em nexus_media ou projetos individuais como "olhos", verifique os caminhos absolutos usados nos scripts).*
