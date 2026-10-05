#!/usr/bin/env node
/**
 * HAD-256: lint and LOAD a PHP file under a given PHP version (php-wasm, offline: the runtime the Playground CLI already
 * cached), as Code Snippets would load it: no WordPress, stub add_action(), E_ALL, every notice / deprecation collected.
 *
 *   node scripts/had-256/local/php-lint.mjs 8.5 docs/qa/had-256/claim-proof-stage1.php [...]
 *
 * Per file: (1) token_get_all(TOKEN_PARSE) = php -l; (2) include with a recording error handler (compile-time and
 * load-time messages: deprecations such as implicit nullable types, non-canonical casts, backticks); (3) which functions
 * and hooks the file declared at load. Nothing runs past load (the REST callbacks need WordPress).
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { pathToFileURL } from 'node:url';

const ver = process.argv[2];
const files = process.argv.slice(3);
const npx = path.join(os.homedir(), 'AppData', 'Local', 'npm-cache', '_npx');
const root = fs.readdirSync(npx).map((d) => path.join(npx, d, 'node_modules')).find((d) => fs.existsSync(path.join(d, '@php-wasm', 'node', 'package.json')) && fs.existsSync(path.join(d, '@php-wasm', 'node-' + ver.replace('.', '-'))));
if (!root) { console.error('no cached @php-wasm/node with PHP ' + ver); process.exit(2); }
const { loadNodeRuntime } = await import(pathToFileURL(path.join(root, '@php-wasm', 'node', 'index.js')).href);
const { PHP } = await import(pathToFileURL(path.join(root, '@php-wasm', 'universal', 'index.js')).href);
const php = new PHP(await loadNodeRuntime(ver, { emscriptenOptions: { processId: 1 } }));
let bad = 0;
for (const f of files) {
  php.writeFile('/tmp/t.php', fs.readFileSync(f));
  const r = await php.run({ code: `<?php
error_reporting( E_ALL );
ini_set( 'display_errors', '0' );
$msgs = array();
set_error_handler( function ( $no, $str, $file, $line ) use ( &$msgs ) { $msgs[] = $no . ' ' . $str . ' @' . $line; return true; } );
$out = array( 'php' => PHP_VERSION );
try { token_get_all( file_get_contents( '/tmp/t.php' ), TOKEN_PARSE ); $out['parse'] = 'ok'; }
catch ( ParseError $e ) { $out['parse'] = 'ERROR ' . $e->getMessage() . ' line ' . $e->getLine(); }
$hooks = array();
function add_action( $h, $cb, $p = 10, $a = 1 ) { $GLOBALS['hooks'][] = $h; return true; }
function add_filter( $h, $cb, $p = 10, $a = 1 ) { $GLOBALS['hooks'][] = $h; return true; }
$before = get_defined_functions()['user'];
if ( $out['parse'] === 'ok' ) {
  try { include '/tmp/t.php'; $out['load'] = 'ok'; } catch ( Throwable $e ) { $out['load'] = 'ERROR ' . get_class( $e ) . ': ' . $e->getMessage(); }
}
$out['declared'] = array_values( array_diff( get_defined_functions()['user'], $before ) );
$out['hooks'] = $GLOBALS['hooks'] ?? array();
$out['messages'] = $msgs;
echo json_encode( $out );
` });
  let j;
  try { j = JSON.parse(r.text); } catch (e) { j = { raw: r.text, errors: r.errors }; }
  const okf = j.parse === 'ok' && j.load === 'ok' && (!j.messages || j.messages.length === 0);
  if (!okf) bad++;
  console.log((okf ? 'OK   ' : 'FAIL ') + f + ' ' + JSON.stringify(j));
}
process.exit(bad ? 1 : 0);
