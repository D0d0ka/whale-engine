#version 330 core

in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec4 uColor;
uniform float u_strength;

out vec4 FragColor;

void main() {
    vec4 c = texture(uTexture, vTexCoord) * uColor;
    vec2 uv = vTexCoord - 0.5;
    float dist = length(uv);
    float strength = u_strength > 0.0 ? u_strength : 0.5;
    float vignette = 1.0 - dist * strength * 2.0;
    vignette = clamp(vignette, 0.0, 1.0);
    FragColor = vec4(c.rgb * vignette, c.a);
}
