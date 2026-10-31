
#version 330 core

in vec3 vColor;
in vec2 vUV;
in vec3 vNormal;
in vec3 vWorldPosition;
in vec4 vLightSpacePosition;

uniform sampler2D uTexture;
uniform int uUseTexture;

// Mapa de profundidade gerado pela luz.
uniform sampler2D uShadowMap;

uniform vec3 uLightDirection;
uniform vec3 uLightColor;
uniform vec3 uCameraPosition;

uniform float uMaterialAmbient;
uniform float uMaterialDiffuse;
uniform float uMaterialSpecular;
uniform float uMaterialShininess;

out vec4 FragColor;


// Calcula a proporcao de sombra usando PCF 3x3.
float calcularSombra(
    vec4 lightSpacePosition,
    vec3 normal,
    vec3 lightDir
)
{
    // Converte de coordenadas de recorte para NDC.
    vec3 coords =
        lightSpacePosition.xyz /
        lightSpacePosition.w;

    // Transforma o intervalo [-1, 1] em [0, 1].
    coords = coords * 0.5 + 0.5;

    // Regioes fora do volume da luz nao recebem sombra.
    if (
        coords.z <= 0.0 ||
        coords.z >= 1.0 ||
        coords.x < 0.0 ||
        coords.x > 1.0 ||
        coords.y < 0.0 ||
        coords.y > 1.0
    )
    {
        return 0.0;
    }

    // Evita sombras indevidas na propria superficie.
    float bias = max(
        0.002 * (1.0 - dot(normal, lightDir)),
        0.0005
    );

    // Tamanho de um pixel da textura de profundidade.
    vec2 texelSize =
        1.0 / vec2(textureSize(uShadowMap, 0));

    float shadow = 0.0;

    // Percentage-Closer Filtering: nove amostras.
    for (int x = -1; x <= 1; ++x)
    {
        for (int y = -1; y <= 1; ++y)
        {
            vec2 offset =
                vec2(float(x), float(y)) * texelSize;

            float closestDepth = texture(
                uShadowMap,
                coords.xy + offset
            ).r;

            if (coords.z - bias > closestDepth)
            {
                shadow += 1.0;
            }
        }
    }

    return shadow / 9.0;
}


void main()
{
    // Cor da superficie: textura ou cor por vertice.
    vec3 baseColor = vColor;

    if (uUseTexture == 1)
    {
        baseColor = texture(uTexture, vUV).rgb;
    }

    vec3 normal = normalize(vNormal);
    vec3 lightDir = normalize(uLightDirection);

    // Iluminacao ambiente.
    vec3 ambient =
        baseColor * uMaterialAmbient;

    // Iluminacao difusa.
    float diffuseFactor = max(
        dot(normal, lightDir),
        0.0
    );

    vec3 diffuse =
        baseColor *
        uLightColor *
        uMaterialDiffuse *
        diffuseFactor;

    // Iluminacao especular.
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

    // Consulta o mapa de profundidade.
    float shadow = calcularSombra(
        vLightSpacePosition,
        normal,
        lightDir
    );

    // A sombra reduz apenas a luz direta.
    // A componente ambiente permanece visivel.
    vec3 finalColor =
        ambient +
        (1.0 - shadow) * (diffuse + specular);

    FragColor = vec4(
        clamp(finalColor, 0.0, 1.0),
        1.0
    );
}
