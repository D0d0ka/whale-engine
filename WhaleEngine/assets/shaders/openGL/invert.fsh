#version 330 core

in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec4 uColor;

out vec4 FragColor;

void main() {
    vec4 c = texture(uTexture, vTexCoord) * uColor;
    FragColor = vec4(1.0 - c.r, 1.0 - c.g, 1.0 - c.b, c.a);
}
