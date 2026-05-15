#version 120
uniform sampler2D u_texture;
// u_strength: vinjeti tugevus (0.0-1.0), default 0.5
uniform float u_strength;

void main() {
    vec4 c = texture2D(u_texture, gl_TexCoord[0].st);
    vec2 uv = gl_TexCoord[0].st - 0.5;
    float dist = length(uv);
    float strength = u_strength > 0.0 ? u_strength : 0.5;
    float vignette = 1.0 - dist * strength * 2.0;
    vignette = clamp(vignette, 0.0, 1.0);
    gl_FragColor = vec4(c.rgb * vignette, c.a);
}
