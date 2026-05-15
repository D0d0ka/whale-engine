#version 120
uniform sampler2D u_texture;

void main() {
    vec4 c = texture2D(u_texture, gl_TexCoord[0].st);
    gl_FragColor = vec4(1.0 - c.r, 1.0 - c.g, 1.0 - c.b, c.a);
}
