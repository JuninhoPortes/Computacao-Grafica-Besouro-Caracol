# Besouro Mecânico e Caracol Robótico — Cena 3D Interativa

**Trabalho Prático de Computação Gráfica — Ciência da Computação — 2026/02**

## Integrantes e temas

| Integrante | Identificação | Tema |
| --- | --- | --- |
| 1 | **EVANDRO PORTES DA SILVA JÚNIOR / 231-000654** | **29 — Besouro mecânico** |
| 2 | **ANA BEATRIZ VIGIANE MAIA / 231-002727** | **30 — Caracol robótico** |

## Objetivo e descrição da cena

Desenvolver uma aplicação gráfica tridimensional em Python, Pygame e OpenGL, baseada nos conceitos e na organização do framework apresentados por Lee Stemkoski e Michael Pascale em *Developing Graphics Frameworks with Python and OpenGL*.

A cena representa um laboratório de testes com uma plataforma metálica texturizada e dois personagens modelados a partir de formas geométricas: um **besouro mecânico**, com seis patas e duas antenas articuladas, e um **caracol robótico**, com corpo, concha espiralada, cabeça e antenas móveis.

**Interação coordenada:** o caracol inicia o percurso; o besouro se aproxima; o caracol interrompe o deslocamento; o besouro realiza uma inspeção movimentando suas antenas; o besouro se afasta; somente então o caracol retoma o percurso. O comportamento é definido em cinco fases principais e um estado final, sem necessidade de simulação física ou detecção de colisões.

## Tecnologias e requisitos

- Python **3.11.9**, versão utilizada durante o desenvolvimento.
- Pygame, PyOpenGL, NumPy e Pillow (versões registradas em `requirements.txt`).
- OpenGL **3.3 Core Profile** e shaders **GLSL 330**.
- GPU e driver com suporte ao contexto OpenGL solicitado.

O diretório `framework/` contém uma **implementação própria e adaptada de componentes arquiteturais estudados no livro**. Não se trata de uma cópia integral do framework original nem da importação de uma engine 3D externa. A relação com a obra e as fontes consultadas estão descritas no final deste arquivo.

## Instalação e execução (Windows / PowerShell)

Abra o terminal na raiz do projeto (a pasta que contém `main.py`) e execute:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

A criação da `.venv` é necessária apenas na primeira configuração. A aplicação abre uma janela de **960 × 540** pixels. Para executá-la novamente, use apenas o último comando. Os caminhos de recursos são resolvidos a partir da pasta do próprio `main.py`, portanto não é necessário informar manualmente os diretórios dos shaders e da textura.

### Controles

| Tecla | Função |
| --- | --- |
| `A` / `D` | Orbitar a câmera horizontalmente |
| `W` / `S` | Aproximar / afastar a câmera |
| `Q` / `E` | Baixar / elevar a câmera |
| `Espaço` ou `P` | Pausar / retomar a animação sem interromper a visualização |
| `R` | Reiniciar a sequência coordenada |
| `C` | Restaurar o enquadramento inicial da câmera |
| `Esc` | Encerrar a aplicação |

A barra de título da janela informa a fase atual e o estado da animação (`ATIVO`, `PAUSADO` ou `FINALIZADO`). A câmera permanece utilizável quando a animação está pausada.

## Fases da interação

| Tempo aproximado | Fase | Comportamento |
| --- | --- | --- |
| 0–2 s | Exploração | O caracol desliza e o besouro aguarda. |
| 2–5,2 s | Aproximação | O besouro caminha em direção ao caracol, que interrompe o deslocamento ao notar a proximidade. |
| 5,2–7,8 s | Inspeção | Ambos param; o besouro aumenta a oscilação das antenas. |
| 7,8–10,2 s | Afastamento | O besouro recua; o caracol continua aguardando. |
| 10,2–13 s | Retomada | O caracol retoma o percurso após a liberação da passagem. |
| A partir de 13 s | Concluída | Ambos ficam parados; `R` reinicia a demonstração. |

O controlador em `cena/interacao.py` recebe o tempo decorrido (`delta_time`) e calcula estados e posições. A animação de patas, antenas e cabeça é atualizada separadamente a partir do tempo de animação, interrompido durante a pausa.

## Estrutura e localização dos principais recursos

```text
Besouro_Caracol/
├── main.py                         # Inicialização, cena e controles principais
├── cena/
│   ├── interacao.py                # EstadoInteracao, ControladorInteracao
│   └── controle_camera.py          # ControleCamera
├── personagens/
│   ├── besouro.py                  # BesouroMecanico
│   └── caracol.py                  # CaracolRobotico
├── framework/
│   ├── core/
│   │   ├── base.py                 # Base: janela, eventos, ciclo e delta_time
│   │   └── shader_program.py       # ShaderProgram: compilação e uniforms
│   ├── core_ext/
│   │   ├── camera.py               # Camera: matrizes view e perspective
│   │   ├── mesh.py                 # Mesh: VAO, VBO, atributos e desenho
│   │   ├── object3d.py             # Object3D: hierarquia e matrizes locais/globais
│   │   ├── scene.py                # Scene: objeto-raiz da cena
│   │   ├── renderer.py             # Renderer: duas passagens de renderização
│   │   ├── shadow_map.py           # ShadowMap: depth texture e framebuffer
│   │   └── texture.py              # Texture: carregamento PNG e mipmaps
│   ├── geometry/
│   │   ├── box.py                  # create_box_geometry
│   │   └── sphere.py               # create_sphere_geometry
│   ├── light/directional.py        # DirectionalLight
│   └── material/surface.py         # SurfaceMaterial
├── shaders/
│   ├── basic.vert                  # Transformações, normais, UV e espaço da luz
│   ├── basic.frag                  # Phong, textura, PCF e sombras
│   ├── shadow_depth.vert           # Passagem de profundidade da luz
│   └── shadow_depth.frag           # Fragment shader da passagem de profundidade
├── texturas/
│   └── piso_laboratorio.png        # Textura de imagem aplicada ao piso
├── ferramentas/
│   └── gerar_textura_piso.py       # Geração autoral da textura com Pillow
├── tests/
│   ├── test_interacao.py           # Testes da sequência coordenada
│   └── test_grafico.py             # Testes das geometrias e transformações
├── requirements.txt
└── README.md
```

O projeto **não requer os arquivos de exemplos de terceiros para executar**, mas mantém os componentes do seu framework adaptado como código-fonte. Os diretórios também incluem arquivos `__init__.py` de pacotes Python.

## Requisitos gráficos e suas implementações

| Exigência | Implementação principal |
| --- | --- |
| Dois modelos 3D reconhecíveis | `personagens/besouro.py` e `personagens/caracol.py`, com malhas geométricas de caixas e esferas |
| Animação coordenada, independente do FPS | `cena/interacao.py`, métodos `update()` dos personagens e `delta_time` de `Base` |
| Translação, rotação, escala e hierarquia | `Object3D`, métodos `set_position`, `set_rotation`, `set_scale`, `get_local_matrix`, `get_world_matrix`, `traverse` |
| Câmera perspectiva, controle e pausa | `Camera`, `ControleCamera`, `main.py` e método `handle_event` |
| Textura de imagem com UV | `texturas/piso_laboratorio.png`, `Texture`, `Mesh`, `basic.vert` e `basic.frag` |
| Iluminação direcional, materiais e normais | `DirectionalLight`, `SurfaceMaterial`, shaders `basic.vert` e `basic.frag` |
| Sombra projetada dinâmica por shadow mapping | `ShadowMap`, `Renderer`, `shadow_depth.vert`, `shadow_depth.frag`, `basic.vert` e `basic.frag` |

### Shaders, atributos de vértice e uniforms

**Atributos declarados no `basic.vert` e preenchidos por `Mesh`:**

| Layout | Atributo | Componentes | Utilização |
| --- | --- | --- | --- |
| 0 | `aPosition` | `vec3` | Posição local do vértice; multiplicada pelas matrizes de modelo, visualização e projeção |
| 1 | `aNormal` | `vec3` | Normal da superfície; transformada por inversa transposta para iluminação |
| 2 | `aUV` | `vec2` | Coordenadas de textura para amostragem da imagem PNG |
| 3 | `aColor` | `vec3` | Cor do vértice quando o objeto não utiliza textura |

O buffer de cada vértice contém **11 floats**: posição (3), normal (3), UV (2) e cor (3).

**Uniforms efetivamente utilizados nos shaders:**

| Uniform(s) | Arquivo(s) | Finalidade |
| --- | --- | --- |
| `uModel` | `basic.vert`, `shadow_depth.vert` | Transformação do objeto em coordenadas de mundo |
| `uView`, `uProjection` | `basic.vert` | Visualização da câmera e projeção em perspectiva |
| `uLightViewProjection` | `basic.vert`, `shadow_depth.vert` | Transformação para o espaço de profundidade da luz |
| `uTexture`, `uUseTexture` | `basic.frag` | Amostragem de textura da superfície ou uso da cor dos vértices |
| `uShadowMap` | `basic.frag` | Mapa de profundidade consultado para calcular a sombra |
| `uLightDirection`, `uLightColor` | `basic.frag` | Direção e cor da iluminação |
| `uCameraPosition` | `basic.frag` | Vetor de visão para a reflexão especular |
| `uMaterialAmbient`, `uMaterialDiffuse` | `basic.frag` | Contribuições ambiente e difusa do material |
| `uMaterialSpecular`, `uMaterialShininess` | `basic.frag` | Intensidade e concentração do brilho especular |

**Sombreamento versus sombra projetada:** a iluminação Phong calcula, em cada superfície, as contribuições ambiente, difusa e especular a partir das normais, da direção da luz e da posição da câmera. O **shadow mapping** é um processo separado: renderiza uma textura de profundidade a partir da luz e a consulta na renderização final, reduzindo a luz direta em regiões ocluídas. O shader utiliza um ajuste de profundidade (*bias*) e filtro PCF 3 × 3 para suavizar bordas.

## Testes e verificações

Para executar os testes automatizados na raiz do projeto:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -p "test_*.py" -v
```

Durante o desenvolvimento, foram relatados **15 testes automatizados aprovados**, cobrindo estados da interação, comparação entre simulações de 30 e 120 FPS, geometrias, normais, UV e transformações. A aplicação também foi validada manualmente em ambiente Windows, incluindo câmera, pausa, retomada, textura, iluminação e sombras dinâmicas. Esses testes não substituem uma nova execução em cada computador onde o trabalho for apresentado.

A textura pode ser regenerada, caso necessário, com:

```powershell
.\.venv\Scripts\python.exe ferramentas\gerar_textura_piso.py
```

## Contribuições individuais

**Integrante 1 — EVANDRO PORTES DA SILVA JÚNIOR:** implementação do código Python, modelagem e animação dos dois personagens, sistema de interação, framework adaptado, recursos de renderização, testes, organização do repositório e documentação técnica, com apoio de IA quando indicado abaixo.

**Integrante 2 — ANA BEATRIZ VIGIANE MAIA:** elaboração da apresentação em PowerPoint a partir do projeto concluído, preparação dos slides e participação na exposição oral.

Ambos os integrantes deverão estudar e explicar a aplicação integrada durante a apresentação individual avaliada pelo professor.

## Declaração de uso de inteligência artificial

Foi utilizada a ferramenta **ChatGPT (OpenAI)** como apoio ao planejamento, estruturação das etapas, elaboração inicial e revisão de códigos Python e GLSL, definição da interação, elaboração de testes e preparação da documentação. O apoio incidiu, de maneira ampla, sobre os módulos `main.py`, `cena/`, `personagens/`, `framework/`, `shaders/`, scripts de geração de textura e testes automatizados. O código foi integrado, executado e validado localmente durante o desenvolvimento. Também foram utilizadas ferramentas de inteligência artificial como apoio à organização e elaboração da apresentação acadêmica, a partir da documentação técnica e dos resultados reais da aplicação.

A utilização de IA não substitui a compreensão técnica, a verificação do código nem a capacidade de explicar seu funcionamento.

## Fontes e referências

1. STEMKOSKI, Lee; PASCALE, Michael. *Developing Graphics Frameworks with Python and OpenGL*. 1. ed. Boca Raton: CRC Press, 2022. DOI: **10.1201/9781003181378**. Referência principal para arquitetura de framework e técnicas gráficas (incluindo shadow mapping na seção 6.9).
2. **OpenGL / Khronos Group**. Especificações e documentação técnica da API OpenGL e da linguagem GLSL. https://www.khronos.org/opengl/
3. **Exemplos de terceiros consultados como referência de estudo:** https://github.com/ax-va/PyOpenGL-Pygame-Stemkoski-Pascale-2021 . O repositório apresenta implementações relacionadas ao livro; **não declarar seu código como próprio nem pressupor autorização para redistribuí-lo**. A aplicação entregue utiliza classes próprias adaptadas à arquitetura estudada.

A textura `piso_laboratorio.png` é produzida localmente pelo script `ferramentas/gerar_textura_piso.py`, sem necessidade de imagem externa.

## Observações de entrega

- Incluir o código Python, os quatro shaders, a textura PNG, o framework adaptado, o `requirements.txt`, os testes e este README.
- Não incluir a pasta `.venv`, caches de Python nem o diretório `.git` no ZIP de entrega.
- Anexar a documentação técnica em PDF e a apresentação da dupla conforme o planejamento de entrega.
