#version 120
uniform sampler2D u_texture;
// u_outline_color: äärise värv (RGBA), default must
uniform vec4 u_outline_color;
// u_threshold: alpha künnis äärise tuvastamiseks, default 0.1
uniform float u_threshold;

void main() {
    vec2 uv = gl_TexCoord[0].st;
    vec4 c = texture2D(u_texture, uv);
    float threshold = u_threshold > 0.0 ? u_threshold : 0.1;

    if (c.a < threshold) {
        float step = 0.005;
        float neighbors =
            texture2D(u_texture, uv + vec2( step, 0.0)).a +
            texture2D(u_texture, uv + vec2(-step, 0.0)).a +
            texture2D(u_texture, uv + vec2(0.0,  step)).a +
            texture2D(u_texture, uv + vec2(0.0, -step)).a;
        if (neighbors > threshold) {
            vec4 oc = u_outline_color.a > 0.0 ? u_outline_color : vec4(0.0, 0.0, 0.0, 1.0);
            gl_FragColor = oc;
            return;
        }
    }
    gl_FragColor = c;
}
