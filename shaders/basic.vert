
#version 330 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec2 aUV;
layout(location = 3) in vec3 aColor;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;

out vec3 vColor;
out vec2 vUV;
out vec3 vNormal;
out vec3 vWorldPosition;

void main()
{
    // Transforma o vertice para coordenadas de mundo.
    vec4 worldPosition = uModel * vec4(aPosition, 1.0);

    vWorldPosition = worldPosition.xyz;

    // Corrige as normais para transformacoes e escalas.
    mat3 normalMatrix = transpose(inverse(mat3(uModel)));

    vNormal = normalize(normalMatrix * aNormal);

    // Preserva as cores e coordenadas de textura.
    vColor = aColor;
    vUV = aUV;

    // Calcula a posicao final na tela.
    gl_Position =
        uProjection *
        uView *
        worldPosition;
}
