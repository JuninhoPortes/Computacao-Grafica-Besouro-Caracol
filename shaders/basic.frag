
#version 330 core

in vec3 vColor;
in vec2 vUV;

uniform sampler2D uTexture;
uniform int uUseTexture;

out vec4 FragColor;

void main()
{
    vec3 surfaceColor = vColor;

    if (uUseTexture == 1)
    {
        surfaceColor = texture(uTexture, vUV).rgb;
    }

    FragColor = vec4(surfaceColor, 1.0);
}
