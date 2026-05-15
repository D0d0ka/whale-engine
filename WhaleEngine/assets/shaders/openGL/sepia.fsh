#version 330 core

in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec4 uColor;

out vec4 FragColor;

void main() {
    vec4 c = texture(uTexture, vTexCoord) * uColor;
    float r = dot(c.rgb, vec3(0.393, 0.769, 0.189));
    float g = dot(c.rgb, vec3(0.349, 0.686, 0.168));
    float b = dot(c.rgb, vec3(0.272, 0.534, 0.131));
    FragColor = vec4(clamp(r, 0.0, 1.0), clamp(g, 0.0, 1.0), clamp(b, 0.0, 1.0), c.a);
}
