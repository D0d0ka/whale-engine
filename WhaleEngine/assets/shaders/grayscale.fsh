#version 120
uniform sampler2D u_texture;

void main() {
    vec4 c = texture2D(u_texture, gl_TexCoord[0].st);
    float gray = dot(c.rgb, vec3(0.299, 0.587, 0.114));
    gl_FragColor = vec4(gray, gray, gray, c.a);
}
