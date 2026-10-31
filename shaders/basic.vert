
#version 330 core

layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;
layout(location = 2) in vec2 aUV;
layout(location = 3) in vec3 aColor;

uniform mat4 uModel;
uniform mat4 uView;
uniform mat4 uProjection;
uniform mat4 uLightViewProjection;

out vec3 vColor;
out vec2 vUV;
out vec3 vNormal;
out vec3 vWorldPosition;
out vec4 vLightSpacePosition;

void main()
{
    vec4 worldPosition =
        uModel * vec4(aPosition, 1.0);

    vWorldPosition = worldPosition.xyz;

    // Transforma as normais para o espaco de mundo.
    mat3 normalMatrix =
        transpose(inverse(mat3(uModel)));

    vNormal = normalize(normalMatrix * aNormal);

    vColor = aColor;
    vUV = aUV;

    // Posicao do vertice vista pela fonte luminosa.
    vLightSpacePosition =
        uLightViewProjection * worldPosition;

    // Posicao do vertice vista pela camera principal.
    gl_Position =
        uProjection *
        uView *
        worldPosition;
}
