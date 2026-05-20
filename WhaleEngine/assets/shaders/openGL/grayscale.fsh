#version 330 core

in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec4 uColor;

out vec4 FragColor;

void main() {
    vec4 c = texture(uTexture, vTexCoord) * uColor;
    float gray = dot(c.rgb, vec3(0.299, 0.587, 0.114));
    FragColor = vec4(gray, gray, gray, c.a);
}