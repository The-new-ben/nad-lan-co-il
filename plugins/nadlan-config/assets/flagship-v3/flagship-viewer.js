/* First-party GLB viewer for flagship-v3. WebGL2 + same-origin read-only GET. */
(function () {
  "use strict";

  var LIGHTING_SCHEMA = "nadlan-flagship-viewer-lighting/v1";
  var DEFAULT_LIGHTING = Object.freeze({
    schema: LIGHTING_SCHEMA,
    mode: "illustrative_directional",
    direction: Object.freeze([0.45, 0.82, 0.56]),
    ambient: 0.38,
    diffuse: 0.62,
    decisionGrade: false,
    sunSimulation: false
  });

  function clone(value) { return JSON.parse(JSON.stringify(value)); }
  function finite(value) { return typeof value === "number" && Number.isFinite(value); }
  function validCamera(value) {
    return !!value && typeof value === "object" && !Array.isArray(value)
      && finite(value.azimuth) && Math.abs(value.azimuth) <= Math.PI * 1000
      && finite(value.elevation) && value.elevation >= -0.08 && value.elevation <= 1.18
      && finite(value.distance) && value.distance > 0 && value.distance <= 1000000
      && Array.isArray(value.target) && value.target.length === 3 && value.target.every(function (item) { return finite(item) && Math.abs(item) <= 1000000; })
      && finite(value.fieldOfView) && value.fieldOfView >= 10 && value.fieldOfView <= 100;
  }
  function validLighting(value) {
    return !!value && typeof value === "object" && !Array.isArray(value)
      && value.schema === LIGHTING_SCHEMA && value.mode === "illustrative_directional"
      && Array.isArray(value.direction) && value.direction.length === 3 && value.direction.every(function (item) { return finite(item) && Math.abs(item) <= 1; })
      && Math.hypot.apply(Math, value.direction) >= 0.001
      && finite(value.ambient) && value.ambient >= 0 && value.ambient <= 1
      && finite(value.diffuse) && value.diffuse >= 0 && value.diffuse <= 1
      && value.ambient + value.diffuse <= 1.5
      && value.decisionGrade === false && value.sunSimulation === false;
  }
  function identity() { return [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]; }
  function multiply(a, b) {
    var out = new Array(16);
    for (var column = 0; column < 4; column += 1) {
      for (var row = 0; row < 4; row += 1) {
        out[column * 4 + row] = a[row] * b[column * 4] + a[4 + row] * b[column * 4 + 1] + a[8 + row] * b[column * 4 + 2] + a[12 + row] * b[column * 4 + 3];
      }
    }
    return out;
  }
  function transform(matrix, point) {
    return [
      matrix[0] * point[0] + matrix[4] * point[1] + matrix[8] * point[2] + matrix[12],
      matrix[1] * point[0] + matrix[5] * point[1] + matrix[9] * point[2] + matrix[13],
      matrix[2] * point[0] + matrix[6] * point[1] + matrix[10] * point[2] + matrix[14]
    ];
  }
  function transform4(matrix, point) {
    return [
      matrix[0] * point[0] + matrix[4] * point[1] + matrix[8] * point[2] + matrix[12],
      matrix[1] * point[0] + matrix[5] * point[1] + matrix[9] * point[2] + matrix[13],
      matrix[2] * point[0] + matrix[6] * point[1] + matrix[10] * point[2] + matrix[14],
      matrix[3] * point[0] + matrix[7] * point[1] + matrix[11] * point[2] + matrix[15]
    ];
  }
  function compose(node) {
    if (Array.isArray(node.matrix) && node.matrix.length === 16) return node.matrix.slice();
    var translation = node.translation || [0, 0, 0];
    var scale = node.scale || [1, 1, 1];
    var rotation = node.rotation || [0, 0, 0, 1];
    var x = rotation[0], y = rotation[1], z = rotation[2], w = rotation[3];
    return [
      (1 - 2 * y * y - 2 * z * z) * scale[0], (2 * x * y + 2 * w * z) * scale[0], (2 * x * z - 2 * w * y) * scale[0], 0,
      (2 * x * y - 2 * w * z) * scale[1], (1 - 2 * x * x - 2 * z * z) * scale[1], (2 * y * z + 2 * w * x) * scale[1], 0,
      (2 * x * z + 2 * w * y) * scale[2], (2 * y * z - 2 * w * x) * scale[2], (1 - 2 * x * x - 2 * y * y) * scale[2], 0,
      translation[0], translation[1], translation[2], 1
    ];
  }
  function perspective(fieldOfView, aspect, near, far) {
    var factor = 1 / Math.tan(fieldOfView / 2);
    var range = 1 / (near - far);
    return [factor / aspect, 0, 0, 0, 0, factor, 0, 0, 0, 0, (far + near) * range, -1, 0, 0, 2 * far * near * range, 0];
  }
  function lookAt(eye, target, up) {
    var zx = eye[0] - target[0], zy = eye[1] - target[1], zz = eye[2] - target[2];
    var zLength = Math.hypot(zx, zy, zz) || 1;
    zx /= zLength; zy /= zLength; zz /= zLength;
    var xx = up[1] * zz - up[2] * zy, xy = up[2] * zx - up[0] * zz, xz = up[0] * zy - up[1] * zx;
    var xLength = Math.hypot(xx, xy, xz) || 1;
    xx /= xLength; xy /= xLength; xz /= xLength;
    var yx = zy * xz - zz * xy, yy = zz * xx - zx * xz, yz = zx * xy - zy * xx;
    return [xx, yx, zx, 0, xy, yy, zy, 0, xz, yz, zz, 0, -(xx * eye[0] + xy * eye[1] + xz * eye[2]), -(yx * eye[0] + yy * eye[1] + yz * eye[2]), -(zx * eye[0] + zy * eye[1] + zz * eye[2]), 1];
  }
  function parseTarget(value) {
    var parts = String(value || "").trim().split(/\s+/).map(function (part) { return Number(part.replace(/m$/, "")); });
    return parts.length === 3 && parts.every(Number.isFinite) ? parts : null;
  }
  function parseOrbit(value) {
    var parts = String(value || "").trim().split(/\s+/);
    if (parts.length < 2) return null;
    var azimuth = Number(parts[0].replace(/deg$/, ""));
    var polar = Number(parts[1].replace(/deg$/, ""));
    return Number.isFinite(azimuth) && Number.isFinite(polar) ? { azimuth: azimuth * Math.PI / 180, elevation: (90 - polar) * Math.PI / 180 } : null;
  }
  function parsePosition(value) {
    return parseTarget(value);
  }

  function create(canvas, options) {
    options = options || {};
    if (!(canvas instanceof HTMLCanvasElement)) throw new Error("Canvas required");
    var gl = canvas.getContext("webgl2", { antialias: true, alpha: true, powerPreference: "high-performance" });
    if (!gl) throw new Error("WebGL2 unavailable");
    var abort = new AbortController();
    var signal = abort.signal;
    var vertex = "#version 300 es\nin vec3 p;in vec3 n;uniform mat4 mvp;uniform mat4 world;uniform vec3 lightDirection;uniform float ambientLight;uniform float diffuseLight;out float light;void main(){vec3 nn=normalize(mat3(world)*n);light=ambientLight+diffuseLight*max(dot(nn,normalize(lightDirection)),0.0);gl_Position=mvp*vec4(p,1.0);}";
    var fragment = "#version 300 es\nprecision highp float;uniform vec4 color;in float light;out vec4 outColor;void main(){outColor=vec4(color.rgb*light,color.a);}";
    function shader(type, source) {
      var item = gl.createShader(type);
      gl.shaderSource(item, source); gl.compileShader(item);
      if (!gl.getShaderParameter(item, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(item));
      return item;
    }
    var program = gl.createProgram();
    gl.attachShader(program, shader(gl.VERTEX_SHADER, vertex));
    gl.attachShader(program, shader(gl.FRAGMENT_SHADER, fragment));
    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(program));
    var locations = {
      p: gl.getAttribLocation(program, "p"),
      n: gl.getAttribLocation(program, "n"),
      mvp: gl.getUniformLocation(program, "mvp"),
      world: gl.getUniformLocation(program, "world"),
      color: gl.getUniformLocation(program, "color"),
      lightDirection: gl.getUniformLocation(program, "lightDirection"),
      ambientLight: gl.getUniformLocation(program, "ambientLight"),
      diffuseLight: gl.getUniformLocation(program, "diffuseLight")
    };
    var draws = [], radius = 1, dirty = true, drag = null, wheelCommitTimer = null, viewProjection = identity(), destroyed = false;
    var orbit = parseOrbit(options.defaultOrbit) || { azimuth: 0.62, elevation: 0.36 };
    var state = {
      camera: { azimuth: orbit.azimuth, elevation: orbit.elevation, distance: 10, target: parseTarget(options.defaultTarget) || [0, 0, 0], fieldOfView: 42 },
      lighting: clone(DEFAULT_LIGHTING)
    };
    var initial = clone(state);
    function stateChanged() { if (typeof options.onStateChange === "function") options.onStateChange(clone(state)); }

    function accessor(json, binary, index, forceFloat) {
      var item = json.accessors[index], view = json.bufferViews[item.bufferView];
      var components = { SCALAR: 1, VEC2: 2, VEC3: 3, VEC4: 4 }[item.type];
      var sizes = { 5120: 1, 5121: 1, 5122: 2, 5123: 2, 5125: 4, 5126: 4 };
      var getters = { 5120: "getInt8", 5121: "getUint8", 5122: "getInt16", 5123: "getUint16", 5125: "getUint32", 5126: "getFloat32" };
      if (!components || !sizes[item.componentType]) throw new Error("Unsupported accessor");
      var size = sizes[item.componentType], stride = view.byteStride || components * size;
      var bytes = new DataView(binary, view.byteOffset || 0, view.byteLength), total = item.count * components;
      var output = forceFloat ? new Float32Array(total) : new Uint32Array(total);
      for (var row = 0; row < item.count; row += 1) {
        for (var column = 0; column < components; column += 1) {
          output[row * components + column] = bytes[getters[item.componentType]]((item.byteOffset || 0) + row * stride + column * size, true);
        }
      }
      return output;
    }
    function buffer(data, target) {
      var item = gl.createBuffer();
      gl.bindBuffer(target, item); gl.bufferData(target, data, gl.STATIC_DRAW);
      return item;
    }
    function deleteDraws(items) {
      items.forEach(function (draw) { gl.deleteBuffer(draw.position); gl.deleteBuffer(draw.normal); gl.deleteBuffer(draw.index); });
    }
    function clearDraws() {
      deleteDraws(draws);
      draws = [];
    }
    function load(arrayBuffer) {
      if (!(arrayBuffer instanceof ArrayBuffer) || arrayBuffer.byteLength < 20 || arrayBuffer.byteLength > 12 * 1024 * 1024) throw new Error("GLB size rejected");
      var data = new DataView(arrayBuffer);
      if (data.getUint32(0, true) !== 0x46546c67 || data.getUint32(4, true) !== 2) throw new Error("Invalid GLB");
      var offset = 12, json = null, binary = null;
      while (offset + 8 <= arrayBuffer.byteLength) {
        var length = data.getUint32(offset, true), type = data.getUint32(offset + 4, true);
        if (offset + 8 + length > arrayBuffer.byteLength) throw new Error("Malformed GLB");
        var body = arrayBuffer.slice(offset + 8, offset + 8 + length);
        if (type === 0x4e4f534a) json = JSON.parse(new TextDecoder().decode(body));
        if (type === 0x004e4942) binary = body;
        offset += 8 + length;
      }
      if (!json || !binary || !Array.isArray(json.nodes) || !Array.isArray(json.meshes)) throw new Error("Incomplete GLB");
      var minimum = [Infinity, Infinity, Infinity], maximum = [-Infinity, -Infinity, -Infinity];
      var nextDraws = [], createdBuffers = [];
      function nextBuffer(values, target) {
        var item = buffer(values, target);
        createdBuffers.push(item);
        return item;
      }
      function visit(index, parent) {
        var node = json.nodes[index];
        if (!node) return;
        var world = multiply(parent, compose(node));
        if (node.mesh != null && json.meshes[node.mesh]) {
          json.meshes[node.mesh].primitives.forEach(function (primitive) {
            if (!primitive.attributes || primitive.attributes.POSITION == null) return;
            var positions = accessor(json, binary, primitive.attributes.POSITION, true);
            var normals = primitive.attributes.NORMAL != null ? accessor(json, binary, primitive.attributes.NORMAL, true) : new Float32Array(positions.length);
            var indices = primitive.indices != null ? accessor(json, binary, primitive.indices, false) : new Uint32Array(positions.length / 3);
            if (primitive.indices == null) for (var generated = 0; generated < indices.length; generated += 1) indices[generated] = generated;
            if (primitive.attributes.NORMAL == null) for (var normal = 1; normal < normals.length; normal += 3) normals[normal] = 1;
            for (var vertexIndex = 0; vertexIndex < positions.length; vertexIndex += 3) {
              var worldPoint = transform(world, [positions[vertexIndex], positions[vertexIndex + 1], positions[vertexIndex + 2]]);
              for (var axis = 0; axis < 3; axis += 1) { minimum[axis] = Math.min(minimum[axis], worldPoint[axis]); maximum[axis] = Math.max(maximum[axis], worldPoint[axis]); }
            }
            var material = (json.materials || [])[primitive.material] || {};
            var factor = material.pbrMetallicRoughness && material.pbrMetallicRoughness.baseColorFactor || [0.72, 0.62, 0.43, 1];
            nextDraws.push({ position: nextBuffer(positions, gl.ARRAY_BUFFER), normal: nextBuffer(normals, gl.ARRAY_BUFFER), index: nextBuffer(indices, gl.ELEMENT_ARRAY_BUFFER), count: indices.length, world: world, color: factor });
          });
        }
        (node.children || []).forEach(function (child) { visit(child, world); });
      }
      var nextRadius, nextState;
      try {
        var scene = (json.scenes || [])[json.scene || 0];
        if (!scene) throw new Error("Missing GLB scene");
        (scene.nodes || []).forEach(function (node) { visit(node, identity()); });
        if (!nextDraws.length) throw new Error("GLB has no drawable mesh");
        var center = minimum.map(function (value, index) { return (value + maximum[index]) / 2; });
        nextRadius = Math.max(1, Math.hypot(maximum[0] - minimum[0], maximum[1] - minimum[1], maximum[2] - minimum[2]) / 2);
        nextState = clone(state);
        nextState.camera.target = parseTarget(options.defaultTarget) || center;
        nextState.camera.distance = nextRadius * 2.7;
      } catch (error) {
        createdBuffers.forEach(function (item) { gl.deleteBuffer(item); });
        throw error;
      }
      var previousDraws = draws;
      draws = nextDraws;
      radius = nextRadius;
      state = nextState;
      deleteDraws(previousDraws);
      initial = clone(state);
      stateChanged();
      dirty = true; render();
      return { meshes: nextDraws.length, bytes: arrayBuffer.byteLength };
    }
    function resize() {
      var ratio = Math.min(2, window.devicePixelRatio || 1), width = Math.max(1, Math.floor(canvas.clientWidth * ratio)), height = Math.max(1, Math.floor(canvas.clientHeight * ratio));
      if (canvas.width !== width || canvas.height !== height) { canvas.width = width; canvas.height = height; dirty = true; }
    }
    function computeViewProjection() {
      var camera = state.camera, azimuth = camera.azimuth, elevation = camera.elevation, distance = camera.distance, target = camera.target;
      var eye = [target[0] + Math.sin(azimuth) * Math.cos(elevation) * distance, target[1] + Math.sin(elevation) * distance, target[2] + Math.cos(azimuth) * Math.cos(elevation) * distance];
      return multiply(perspective(camera.fieldOfView * Math.PI / 180, canvas.width / canvas.height, 0.01, Math.max(1000, radius * 20)), lookAt(eye, target, [0, 1, 0]));
    }
    function render() {
      if (destroyed) return;
      resize(); if (!dirty) return; dirty = false;
      viewProjection = computeViewProjection();
      gl.viewport(0, 0, canvas.width, canvas.height); gl.enable(gl.DEPTH_TEST); gl.enable(gl.CULL_FACE);
      gl.clearColor(0.035, 0.16, 0.15, 1); gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT); gl.useProgram(program);
      gl.uniform3fv(locations.lightDirection, new Float32Array(state.lighting.direction));
      gl.uniform1f(locations.ambientLight, state.lighting.ambient);
      gl.uniform1f(locations.diffuseLight, state.lighting.diffuse);
      draws.forEach(function (draw) {
        gl.bindBuffer(gl.ARRAY_BUFFER, draw.position); gl.enableVertexAttribArray(locations.p); gl.vertexAttribPointer(locations.p, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ARRAY_BUFFER, draw.normal); gl.enableVertexAttribArray(locations.n); gl.vertexAttribPointer(locations.n, 3, gl.FLOAT, false, 0, 0);
        gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, draw.index); gl.uniformMatrix4fv(locations.world, false, new Float32Array(draw.world)); gl.uniformMatrix4fv(locations.mvp, false, new Float32Array(multiply(viewProjection, draw.world))); gl.uniform4fv(locations.color, new Float32Array(draw.color)); gl.drawElements(gl.TRIANGLES, draw.count, gl.UNSIGNED_INT, 0);
      });
      if (typeof options.onChange === "function") options.onChange();
    }
    function requestRender() { dirty = true; window.requestAnimationFrame(render); }
    function getState() { return clone(state); }
    function setState(next) {
      if (!next || !validCamera(next.camera) || (next.lighting !== undefined && !validLighting(next.lighting))) return false;
      state = { camera: clone(next.camera), lighting: clone(next.lighting || state.lighting || DEFAULT_LIGHTING) };
      stateChanged(); requestRender(); return true;
    }
    function getLightingState() { return clone(state.lighting); }
    function setLightingState(next) {
      if (!validLighting(next)) return false;
      state.lighting = clone(next);
      stateChanged(); requestRender();
      return true;
    }
    function getCapabilities() {
      return {
        schema: "nadlan-flagship-viewer-capabilities/v1",
        cameraState: true,
        illustrativeLightingState: true,
        sunSimulation: false,
        sunSimulationReason: "No source-backed solar/time calibration is connected to this viewer."
      };
    }
    function reset() { setState(initial); }
    function zoom(delta, notify) {
      state.camera.distance = Math.max(radius * 1.25, Math.min(radius * 6, state.camera.distance * (delta < 0 ? 0.86 : 1.16)));
      if (notify !== false) stateChanged();
      requestRender();
    }
    function scheduleWheelCommit() {
      if (wheelCommitTimer === null) stateChanged();
      else window.clearTimeout(wheelCommitTimer);
      wheelCommitTimer = window.setTimeout(function () { wheelCommitTimer = null; stateChanged(); }, 100);
    }
    function flushWheelCommit() {
      if (wheelCommitTimer === null) return;
      window.clearTimeout(wheelCommitTimer);
      wheelCommitTimer = null;
      stateChanged();
    }
    function project(value) {
      var point = Array.isArray(value) ? value : parsePosition(value);
      if (!point) return { visible: false, x: 0, y: 0 };
      var clip = transform4(viewProjection, point);
      if (!clip[3] || clip[3] <= 0) return { visible: false, x: 0, y: 0 };
      var x = clip[0] / clip[3], y = clip[1] / clip[3], z = clip[2] / clip[3];
      return { visible: z >= -1 && z <= 1 && x >= -1.2 && x <= 1.2 && y >= -1.2 && y <= 1.2, x: (x * 0.5 + 0.5) * 100, y: (-y * 0.5 + 0.5) * 100 };
    }
    function loadUrl(url) {
      var target = new URL(String(url || ""), window.location.href);
      if (target.origin !== window.location.origin || !/\.glb$/i.test(target.pathname) || target.search || target.hash) return Promise.reject(new Error("Model URL rejected"));
      return window.fetch(target.href, { method: "GET", credentials: "same-origin", cache: "force-cache", redirect: "error", signal: signal }).then(function (response) {
        if (!response.ok || new URL(response.url).origin !== window.location.origin) throw new Error("Model response rejected");
        var length = Number(response.headers.get("content-length") || 0);
        if (length > 12 * 1024 * 1024) throw new Error("Model too large");
        return response.arrayBuffer();
      }).then(load);
    }
    function destroy() {
      if (destroyed) return;
      flushWheelCommit();
      destroyed = true;
      abort.abort(); clearDraws(); gl.deleteProgram(program);
      var extension = gl.getExtension("WEBGL_lose_context"); if (extension) extension.loseContext();
    }
    canvas.addEventListener("keydown", function (event) {
      var handled = true, delegated = false;
      if (event.key === "ArrowLeft") state.camera.azimuth -= 0.12;
      else if (event.key === "ArrowRight") state.camera.azimuth += 0.12;
      else if (event.key === "ArrowUp") state.camera.elevation = Math.min(1.18, state.camera.elevation + 0.08);
      else if (event.key === "ArrowDown") state.camera.elevation = Math.max(-0.08, state.camera.elevation - 0.08);
      else if (event.key === "+" || event.key === "=") { zoom(-1); delegated = true; }
      else if (event.key === "-" || event.key === "_") { zoom(1); delegated = true; }
      else if (event.key === "Home") { reset(); delegated = true; }
      else handled = false;
      if (handled) { if (!delegated) { stateChanged(); requestRender(); } event.preventDefault(); }
    }, { signal: signal });
    canvas.addEventListener("pointerdown", function (event) { drag = { x: event.clientX, y: event.clientY, azimuth: state.camera.azimuth, elevation: state.camera.elevation }; try { canvas.setPointerCapture(event.pointerId); } catch (_error) {} event.preventDefault(); }, { signal: signal });
    canvas.addEventListener("pointermove", function (event) { if (!drag) return; state.camera.azimuth = drag.azimuth + (event.clientX - drag.x) * 0.009; state.camera.elevation = Math.max(-0.08, Math.min(1.18, drag.elevation + (event.clientY - drag.y) * 0.007)); requestRender(); }, { signal: signal });
    canvas.addEventListener("pointerup", function () { if (!drag) return; drag = null; stateChanged(); }, { signal: signal });
    canvas.addEventListener("pointercancel", function () { if (!drag) return; drag = null; stateChanged(); }, { signal: signal });
    canvas.addEventListener("wheel", function (event) { zoom(event.deltaY, false); scheduleWheelCommit(); event.preventDefault(); }, { passive: false, signal: signal });
    window.addEventListener("blur", flushWheelCommit, { signal: signal });
    window.addEventListener("pagehide", flushWheelCommit, { signal: signal });
    window.addEventListener("resize", requestRender, { signal: signal });
    return Object.freeze({
      loadUrl: loadUrl,
      getState: getState,
      setState: setState,
      getLightingState: getLightingState,
      setLightingState: setLightingState,
      getCapabilities: getCapabilities,
      reset: reset,
      zoom: zoom,
      project: project,
      render: requestRender,
      destroy: destroy
    });
  }

  window.NadlanFlagshipLocalViewer = Object.freeze({ create: create, LIGHTING_SCHEMA: LIGHTING_SCHEMA });
})();
