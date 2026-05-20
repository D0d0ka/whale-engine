#version 330 core

in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec4 uColor;
uniform float u_brightness;

out vec4 FragColor;

void main() {
    vec4 c = texture(uTexture, vTexCoord) * uColor;
    float b = u_brightness != 0.0 ? u_brightness : 0.2;
    FragColor = vec4(clamp(c.rgb + b, 0.0, 1.0), c.a);
}