#version 330 core

in vec2 vTexCoord;

uniform sampler2D uTexture;
uniform vec4 uColor;
uniform vec4 u_outline_color;
uniform float u_threshold;

out vec4 FragColor;

void main() {
    vec2 uv = vTexCoord;
    vec4 c = texture(uTexture, uv) * uColor;
    float threshold = u_threshold > 0.0 ? u_threshold : 0.1;

    if (c.a < threshold) {
        float stepSize = 0.005;
        float neighbors =
            texture(uTexture, uv + vec2( stepSize, 0.0)).a +
            texture(uTexture, uv + vec2(-stepSize, 0.0)).a +
            texture(uTexture, uv + vec2(0.0,  stepSize)).a +
            texture(uTexture, uv + vec2(0.0, -stepSize)).a;
        if (neighbors > threshold) {
            vec4 outlineColor = u_outline_color.a > 0.0 ? u_outline_color : vec4(0.0, 0.0, 0.0, 1.0);
            FragColor = outlineColor;
            return;
        }
    }
    FragColor = c;
}
