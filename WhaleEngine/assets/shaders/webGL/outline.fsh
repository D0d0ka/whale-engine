precision mediump float;
varying vec2 vTexCoord;
uniform sampler2D uTexture;
uniform vec4 uColor;
uniform vec4 u_outline_color;
uniform float u_threshold;

void main() {
    vec2 uv = vTexCoord;
    vec4 c = texture2D(uTexture, uv) * uColor;
    float threshold = u_threshold > 0.0 ? u_threshold : 0.1;

    if (c.a < threshold) {
        float stepSize = 0.005;
        float neighbors =
            texture2D(uTexture, uv + vec2( stepSize, 0.0)).a +
            texture2D(uTexture, uv + vec2(-stepSize, 0.0)).a +
            texture2D(uTexture, uv + vec2(0.0,  stepSize)).a +
            texture2D(uTexture, uv + vec2(0.0, -stepSize)).a;
        if (neighbors > threshold) {
            vec4 outlineColor = u_outline_color.a > 0.0 ? u_outline_color : vec4(0.0, 0.0, 0.0, 1.0);
            gl_FragColor = outlineColor;
            return;
        }
    }
    gl_FragColor = c;
}