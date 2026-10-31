
from pathlib import Path

from PIL import Image, ImageDraw


def gerar_textura():
    """Gera uma textura PNG para o piso do laboratorio."""

    tamanho = 768
    quantidade = 8
    celula = tamanho // quantidade

    imagem = Image.new(
        "RGB",
        (tamanho, tamanho),
        (34, 42, 54),
    )

    desenho = ImageDraw.Draw(imagem)

    for linha in range(quantidade):
        for coluna in range(quantidade):
            x = coluna * celula
            y = linha * celula

            # Alterna suavemente as cores dos paineis.
            cor = (
                (65, 78, 96)
                if (linha + coluna) % 2 == 0
                else (55, 68, 84)
            )

            desenho.rectangle(
                (
                    x + 4,
                    y + 4,
                    x + celula - 4,
                    y + celula - 4,
                ),
                fill=cor,
                outline=(108, 124, 140),
                width=3,
            )

            # Pequenos parafusos decorativos.
            for dx in (16, celula - 16):
                for dy in (16, celula - 16):
                    px = x + dx
                    py = y + dy

                    desenho.ellipse(
                        (px - 3, py - 3, px + 3, py + 3),
                        fill=(165, 178, 186),
                    )

    # Linha de sinalizacao do laboratorio.
    desenho.line(
        (0, tamanho // 2, tamanho, tamanho // 2),
        fill=(215, 169, 68),
        width=5,
    )

    destino = (
        Path(__file__).resolve().parents[1]
        / "texturas"
        / "piso_laboratorio.png"
    )

    destino.parent.mkdir(parents=True, exist_ok=True)
    imagem.save(destino)

    print(f"Textura gerada: {destino}")


if __name__ == "__main__":
    gerar_textura()
