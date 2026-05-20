attribute vec2 aPosition;
attribute vec2 aTexCoord;

uniform mat4 uProjection;
uniform mat4 uModel;

varying vec2 vTexCoord;

void main() {
    vTexCoord = aTexCoord;
    gl_Position = uProjection * uModel * vec4(aPosition, 0.0, 1.0);
}