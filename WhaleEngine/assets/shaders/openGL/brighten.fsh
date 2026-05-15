#version 120
uniform sampler2D u_texture;
// u_brightness: heleduse muutus (-1.0 kuni 1.0), default 0.2
uniform float u_brightness;

void main() {
    vec4 c = texture2D(u_texture, gl_TexCoord[0].st);
    float b = u_brightness != 0.0 ? u_brightness : 0.2;
    gl_FragColor = vec4(clamp(c.rgb + b, 0.0, 1.0), c.a);
}
