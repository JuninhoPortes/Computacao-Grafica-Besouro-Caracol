
#version 330 core

in vec3 vColor;
in vec2 vUV;
in vec3 vNormal;
in vec3 vWorldPosition;

// Textura.
uniform sampler2D uTexture;
uniform int uUseTexture;

// Fonte luminosa direcional.
uniform vec3 uLightDirection;
uniform vec3 uLightColor;

// Posicao da camera.
uniform vec3 uCameraPosition;

// Propriedades do material.
uniform float uMaterialAmbient;
uniform float uMaterialDiffuse;
uniform float uMaterialSpecular;
uniform float uMaterialShininess;

out vec4 FragColor;

void main()
{
    // Cor original do objeto.
    vec3 baseColor = vColor;

    if (uUseTexture == 1)
    {
        baseColor = texture(uTexture, vUV).rgb;
    }

    // Vetores usados no calculo da iluminacao.
    vec3 normal = normalize(vNormal);
    vec3 lightDir = normalize(uLightDirection);

    // 1. Componente ambiente.
    vec3 ambient =
        baseColor * uMaterialAmbient;

    // 2. Componente difusa.
    float diffuseFactor = max(
        dot(normal, lightDir),
        0.0
    );

    vec3 diffuse =
        baseColor *
        uLightColor *
        uMaterialDiffuse *
        diffuseFactor;

    // 3. Componente especular.
    vec3 viewDir = normalize(
        uCameraPosition - vWorldPosition
    );

    vec3 reflectedDir = reflect(
        -lightDir,
        normal
    );

    float specularFactor = 0.0;

    if (diffuseFactor > 0.0)
    {
        specularFactor = pow(
            max(dot(viewDir, reflectedDir), 0.0),
            uMaterialShininess
        );
    }

    vec3 specular =
        uLightColor *
        uMaterialSpecular *
        specularFactor;

    // Combina as componentes.
    vec3 finalColor =
        ambient + diffuse + specular;

    FragColor = vec4(
        clamp(finalColor, 0.0, 1.0),
        1.0
    );
}
