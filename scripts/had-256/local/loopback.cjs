/**
 * HAD-256 bench: the Playground CLI (3.1.56) calls server.listen(port) with no host, which binds every interface,
 * and it has no host/bind option. This preload (NODE_OPTIONS=--require <this file>, inherited by the CLI's own
 * re-spawned node process) pins every TCP listen() in that process to 127.0.0.1, so the bench, with its reset and
 * fault routes and its synthetic admin, is reachable from this machine only. No firewall or system setting changes.
 */
'use strict';
const net = require('net');
const LOOP = '127.0.0.1';
const orig = net.Server.prototype.listen;
net.Server.prototype.listen = function (...args) {
  const a0 = args[0];
  if (typeof a0 === 'number' || (typeof a0 === 'string' && /^\d+$/.test(a0))) {
    // listen(port[, host][, backlog][, callback]) -> the host is always the loopback
    const rest = typeof args[1] === 'string' ? args.slice(2) : args.slice(1);
    return orig.call(this, Number(a0), LOOP, ...rest);
  }
  if (a0 && typeof a0 === 'object' && !Array.isArray(a0) && a0.path === undefined && (a0.port !== undefined || a0.host !== undefined)) {
    args[0] = Object.assign({}, a0, { host: LOOP });
    return orig.apply(this, args);
  }
  if (a0 === undefined || typeof a0 === 'function') {
    // listen() / listen(callback): an ephemeral port, still on the loopback only
    return orig.call(this, 0, LOOP, ...args);
  }
  return orig.apply(this, args);
};
