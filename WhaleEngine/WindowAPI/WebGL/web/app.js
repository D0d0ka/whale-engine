const canvas = document.getElementById("stage");
const titleEl = document.getElementById("appTitle");
const statusEl = document.getElementById("status");
const closeBtn = document.getElementById("closeBtn");

const gl = canvas.getContext("webgl", { alpha: false, antialias: true });
if (!gl) {
  statusEl.textContent = "WebGL unavailable";
  throw new Error("WebGL not supported in this browser");
}

const vertexSource = `
attribute vec2 aPosition;
attribute vec2 aTexCoord;
uniform vec2 uResolution;
uniform vec2 uTranslation;
uniform vec2 uSize;
uniform float uRotation;
uniform vec2 uCameraPos;
uniform float uCameraZoom;
uniform float uCameraRotation;
varying vec2 vTexCoord;

void main() {
  float c = cos(uRotation);
  float s = sin(uRotation);
  vec2 scaled = vec2(aPosition.x * uSize.x, aPosition.y * uSize.y);
  vec2 rotated = vec2(
    scaled.x * c - scaled.y * s,
    scaled.x * s + scaled.y * c
  );
  vec2 world = rotated + uTranslation;
  vec2 camOffset = world - uCameraPos;
  float camC = cos(-uCameraRotation);
  float camS = sin(-uCameraRotation);
  vec2 camRotated = vec2(
    camOffset.x * camC - camOffset.y * camS,
    camOffset.x * camS + camOffset.y * camC
  );
  vec2 camTransformed = camRotated * uCameraZoom;
  vec2 clip = vec2(
    camTransformed.x / (uResolution.x * 0.5),
    camTransformed.y / (uResolution.y * 0.5)
  );
  gl_Position = vec4(clip, 0.0, 1.0);
  vTexCoord = aTexCoord;
}
`;

const fragmentSource = `
precision mediump float;
varying vec2 vTexCoord;
uniform sampler2D uTexture;
uniform vec4 uColor;

void main() {
  vec4 tex = texture2D(uTexture, vTexCoord);
  gl_FragColor = tex * uColor;
}
`;

function compileShader(type, source) {
  const shader = gl.createShader(type);
  gl.shaderSource(shader, source);
  gl.compileShader(shader);
  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    const message = gl.getShaderInfoLog(shader);
    gl.deleteShader(shader);
    throw new Error(message || "Shader compile failed");
  }
  return shader;
}

function createProgram(vs, fs) {
  const program = gl.createProgram();
  gl.attachShader(program, compileShader(gl.VERTEX_SHADER, vs));
  gl.attachShader(program, compileShader(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(program);
  if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
    const message = gl.getProgramInfoLog(program);
    gl.deleteProgram(program);
    throw new Error(message || "Program link failed");
  }
  return program;
}

const programCache = new Map();

function getOrCreateProgram(fragSource) {
  if (programCache.has(fragSource)) {
    return programCache.get(fragSource);
  }
  const prog = createProgram(vertexSource, fragSource);
  const locs = {
    program: prog,
    aPosition: gl.getAttribLocation(prog, "aPosition"),
    aTexCoord: gl.getAttribLocation(prog, "aTexCoord"),
    uResolution: gl.getUniformLocation(prog, "uResolution"),
    uTranslation: gl.getUniformLocation(prog, "uTranslation"),
    uSize: gl.getUniformLocation(prog, "uSize"),
    uRotation: gl.getUniformLocation(prog, "uRotation"),
    uColor: gl.getUniformLocation(prog, "uColor"),
    uTexture: gl.getUniformLocation(prog, "uTexture"),
    uCameraPos: gl.getUniformLocation(prog, "uCameraPos"),
    uCameraZoom: gl.getUniformLocation(prog, "uCameraZoom"),
    uCameraRotation: gl.getUniformLocation(prog, "uCameraRotation"),
  };
  programCache.set(fragSource, locs);
  return locs;
}

const defaultProgramLocs = getOrCreateProgram(fragmentSource);
const { program } = defaultProgramLocs;
const aPosition = defaultProgramLocs.aPosition;
const aTexCoord = defaultProgramLocs.aTexCoord;
const uResolution = defaultProgramLocs.uResolution;
const uTranslation = defaultProgramLocs.uTranslation;
const uSize = defaultProgramLocs.uSize;
const uRotation = defaultProgramLocs.uRotation;
const uColor = defaultProgramLocs.uColor;
const uTexture = defaultProgramLocs.uTexture;

const quadData = new Float32Array([
  -0.5, -0.5, 0.0, 0.0,
   0.5, -0.5, 1.0, 0.0,
   0.5,  0.5, 1.0, 1.0,
  -0.5, -0.5, 0.0, 0.0,
   0.5,  0.5, 1.0, 1.0,
  -0.5,  0.5, 0.0, 1.0,
]);

const buffer = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
gl.bufferData(gl.ARRAY_BUFFER, quadData, gl.STATIC_DRAW);

const stride = 4 * Float32Array.BYTES_PER_ELEMENT;
gl.enableVertexAttribArray(aPosition);
gl.vertexAttribPointer(aPosition, 2, gl.FLOAT, false, stride, 0);
gl.enableVertexAttribArray(aTexCoord);
gl.vertexAttribPointer(aTexCoord, 2, gl.FLOAT, false, stride, 2 * Float32Array.BYTES_PER_ELEMENT);

gl.useProgram(program);
gl.uniform1i(uTexture, 0);

gl.enable(gl.BLEND);
gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);

const textureCache = new Map();
const keyState = Object.create(null);
const mouseState = { left: false, right: false, middle: false };
const cursor = { x: canvas.width / 2, y: canvas.height / 2 };
let eventQueue = [];
let lastFrameId = -1;
let needFullTextures = true;
let requestInFlight = false;
let shuttingDown = false;

function beginShutdown(message = "Closing browser page...") {
  if (shuttingDown) {
    return;
  }
  shuttingDown = true;
  requestInFlight = false;
  statusEl.textContent = message;
  try {
    window.stop();
  } catch {}
  try {
    window.close();
  } catch {}
  try {
    const sameWindow = window.open("", "_self");
    if (sameWindow && typeof sameWindow.close === "function") {
      sameWindow.close();
    }
  } catch {}
  setTimeout(() => {
    try {
      window.location.replace("about:blank");
    } catch {
      try {
        window.location.href = "about:blank";
      } catch {}
    }
  }, 100);
}

const presentedFps = {
  min: Infinity,
  max: 0,
  avg: 0,
  count: 0,
  lastTime: 0,
};

function normalizeKey(key) {
  const map = {
    " ": "space",
    Escape: "escape",
    Enter: "enter",
    Tab: "tab",
    Backspace: "backspace",
    Shift: "left_shift",
    Control: "left_ctrl",
    Alt: "left_alt",
    ArrowUp: "up",
    ArrowDown: "down",
    ArrowLeft: "left",
    ArrowRight: "right",
    Insert: "insert",
    Home: "home",
    PageUp: "page_up",
    Delete: "delete",
    End: "end",
    PageDown: "page_down",
  };
  if (Object.prototype.hasOwnProperty.call(map, key)) {
    return map[key];
  }
  if (key.length === 1) {
    return key.toLowerCase();
  }
  if (/^F\d+$/i.test(key)) {
    return key.toLowerCase();
  }
  return key.toLowerCase();
}

function ensureTexture(texDef) {
  if (!texDef || !texDef.id || !texDef.data) {
    return;
  }
  if (textureCache.has(texDef.id)) {
    return;
  }
  const texture = gl.createTexture();
  const image = new Image();
  image.onload = () => {
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
    const filterMode = texDef.pixelated ? gl.NEAREST : gl.LINEAR;
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, filterMode);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, filterMode);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, image);
  };
  image.src = texDef.data;
  textureCache.set(texDef.id, texture);
}

function drawFrame(state) {
  const width = Math.max(1, Number(state.width || 800));
  const height = Math.max(1, Number(state.height || 600));
  if (canvas.width !== width || canvas.height !== height) {
    canvas.width = width;
    canvas.height = height;
  }
  gl.viewport(0, 0, canvas.width, canvas.height);

  const clear = state.clear_color || [0.08, 0.08, 0.1, 1.0];
  gl.clearColor(clear[0], clear[1], clear[2], clear[3]);
  gl.clear(gl.COLOR_BUFFER_BIT);

  gl.useProgram(program);
  gl.uniform2f(uResolution, canvas.width, canvas.height);

  const textures = Array.isArray(state.textures) ? state.textures : [];
  for (const tex of textures) {
    ensureTexture(tex);
  }

  const entities = Array.isArray(state.entities) ? state.entities : [];
  const cam = state.camera || { x: 0, y: 0, zoom: 1, rotation: 0 };
  const camX = Number(cam.x || 0);
  const camY = Number(cam.y || 0);
  const camZoom = Number(cam.zoom != null ? cam.zoom : 1);
  const camRotRad = (Number(cam.rotation || 0) * Math.PI) / 180;
  for (const entity of entities) {
    const texture = textureCache.get(entity.texture_id);
    if (!texture) {
      continue;
    }

    const locs = entity.shader_frag
      ? getOrCreateProgram(entity.shader_frag)
      : defaultProgramLocs;

    gl.useProgram(locs.program);

    // rebind vertex attributes for this program
    gl.enableVertexAttribArray(locs.aPosition);
    gl.vertexAttribPointer(locs.aPosition, 2, gl.FLOAT, false, stride, 0);
    gl.enableVertexAttribArray(locs.aTexCoord);
    gl.vertexAttribPointer(locs.aTexCoord, 2, gl.FLOAT, false, stride, 2 * Float32Array.BYTES_PER_ELEMENT);

    gl.uniform2f(locs.uResolution, canvas.width, canvas.height);
    gl.uniform1i(locs.uTexture, 0);
    gl.uniform2f(locs.uCameraPos, camX, camY);
    gl.uniform1f(locs.uCameraZoom, camZoom);
    gl.uniform1f(locs.uCameraRotation, camRotRad);

    const w = Number(entity.w || 1) * Number(entity.scale_x || 1);
    const h = Number(entity.h || 1) * Number(entity.scale_y || 1);
    const x = Number(entity.x || 0);
    const y = Number(entity.y || 0);
    const radians = (Number(entity.rotation || 0) * Math.PI) / 180;
    const color = entity.color || [1, 1, 1, 1];

    gl.activeTexture(gl.TEXTURE0);
    gl.bindTexture(gl.TEXTURE_2D, texture);
    gl.uniform2f(locs.uTranslation, x, y);
    gl.uniform2f(locs.uSize, w, h);
    gl.uniform1f(locs.uRotation, radians);
    gl.uniform4f(locs.uColor, color[0], color[1], color[2], color[3]);
    gl.drawArrays(gl.TRIANGLES, 0, 6);
  }
}

function updatePresentedFps(frameId) {
  const now = performance.now();
  if (presentedFps.lastTime > 0) {
    const delta = (now - presentedFps.lastTime) / 1000;
    if (delta > 0 && frameId !== lastFrameId) {
      const fps = 1 / delta;
      presentedFps.min = Math.min(presentedFps.min, fps);
      presentedFps.max = Math.max(presentedFps.max, fps);
      presentedFps.avg = presentedFps.avg === 0 ? fps : (presentedFps.avg * 0.9 + fps * 0.1);
      presentedFps.count += 1;
    }
  }
  presentedFps.lastTime = now;
}

async function sync(close = false) {
  const payload = {
    cursor,
    mouse: mouseState,
    keys: keyState,
    events: eventQueue,
    full_textures: needFullTextures,
    close,
  };
  eventQueue = [];

  try {
    const response = await fetch("/sync", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!response.ok) {
      statusEl.textContent = "Waiting for engine";
      return null;
    }
    const state = await response.json();
    needFullTextures = false;
    return state;
  } catch {
    if (!shuttingDown) {
      statusEl.textContent = "Disconnected";
    }
    return null;
  }
}

async function tick() {
  if (shuttingDown) {
    return;
  }
  if (requestInFlight) {
    requestAnimationFrame(tick);
    return;
  }
  requestInFlight = true;

  const state = await sync(false);
  if (!state) {
    beginShutdown("Disconnected from engine");
    return;
  }
  if (state.close_browser) {
    beginShutdown("Closing browser page...");
    return;
  }

  if (state) {
    const frameId = Number(state.frame_id || 0);
    titleEl.textContent = state.title || "WhaleEngine WebGL";
    if (frameId !== lastFrameId) {
      updatePresentedFps(frameId);
      drawFrame(state);
      lastFrameId = frameId;
    }

    if (presentedFps.count > 0) {
      statusEl.textContent = `FPS ${presentedFps.avg.toFixed(1)} (min ${presentedFps.min.toFixed(1)}, max ${presentedFps.max.toFixed(1)})`;
    } else {
      statusEl.textContent = "Running";
    }
  }

  requestInFlight = false;

  if (!shuttingDown) {
    requestAnimationFrame(tick);
  }
}

window.addEventListener("keydown", (event) => {
  const key = normalizeKey(event.key);
  keyState[key] = true;
  eventQueue.push({ type: "key", key, action: "press" });
});

window.addEventListener("keyup", (event) => {
  const key = normalizeKey(event.key);
  keyState[key] = false;
  eventQueue.push({ type: "key", key, action: "release" });
});

canvas.addEventListener("mousemove", (event) => {
  const rect = canvas.getBoundingClientRect();
  const scaleX = canvas.width / Math.max(1, rect.width);
  const scaleY = canvas.height / Math.max(1, rect.height);
  cursor.x = (event.clientX - rect.left) * scaleX;
  cursor.y = (event.clientY - rect.top) * scaleY;
});

canvas.addEventListener("mousedown", (event) => {
  if (event.button === 0) mouseState.left = true;
  if (event.button === 1) mouseState.middle = true;
  if (event.button === 2) mouseState.right = true;
});

canvas.addEventListener("mouseup", (event) => {
  if (event.button === 0) mouseState.left = false;
  if (event.button === 1) mouseState.middle = false;
  if (event.button === 2) mouseState.right = false;
});

canvas.addEventListener("contextmenu", (event) => {
  event.preventDefault();
});

closeBtn.addEventListener("click", async () => {
  await sync(true);
  statusEl.textContent = "Stopping...";
});

window.addEventListener("beforeunload", () => {
  const data = JSON.stringify({ close: true });
  navigator.sendBeacon("/input", data);
});

tick();