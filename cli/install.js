#!/usr/bin/env node
// npx installer for the Skillkeel Starter plugin.
// It copies nothing and edits no settings file itself: it runs Claude Code's own
// `claude plugin` commands, which add the GitHub marketplace and install the plugin.
'use strict';

const { spawnSync } = require('node:child_process');

const MARKETPLACE_SOURCE = 'skillkeel/skillkeel-starter';
const MARKETPLACE = 'skillkeel';
const PLUGIN = 'skillkeel-starter@' + MARKETPLACE;
const VERSION = require('../package.json').version;
const SCOPES = ['user', 'project', 'local'];

const HELP = `skillkeel-starter ${VERSION}

Installs the Skillkeel Starter plugin into Claude Code through the claude CLI.

Usage:
  npx skillkeel-starter [install] [--scope user|project|local]
  npx skillkeel-starter update
  npx skillkeel-starter uninstall [--scope user|project|local]

What install runs (you can run these yourself instead):
  claude plugin marketplace add ${MARKETPLACE_SOURCE}
  claude plugin install ${PLUGIN} --scope <scope>

Default scope is user. Needs Claude Code on PATH.
`;

function run(args, { quiet = false } = {}) {
  const env = { ...process.env, CLAUDE_CODE_PLUGIN_PREFER_HTTPS: process.env.CLAUDE_CODE_PLUGIN_PREFER_HTTPS || '1' };
  if (!quiet) console.log('$ claude ' + args.join(' '));
  const r = spawnSync('claude', args, { env, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'], timeout: 180000 });
  if (r.error) return { code: 127, out: '', err: String(r.error.message || r.error) };
  return { code: r.status === null ? 1 : r.status, out: r.stdout || '', err: r.stderr || '' };
}

function show(r) {
  const text = (r.out + r.err).trim();
  if (text) console.log(text.split('\n').map((l) => '  ' + l).join('\n'));
}

function fail(msg) {
  console.error('skillkeel-starter: ' + msg);
  process.exit(1);
}

function parse(argv) {
  let cmd = 'install';
  let scope = 'user';
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '-h' || a === '--help') { console.log(HELP); process.exit(0); }
    if (a === '-v' || a === '--version') { console.log(VERSION); process.exit(0); }
    if (a === '--scope' || a === '-s') { scope = argv[++i]; continue; }
    if (a.startsWith('--scope=')) { scope = a.slice(8); continue; }
    if (['install', 'update', 'uninstall'].includes(a)) { cmd = a; continue; }
    fail(`unknown argument "${a}". Try --help.`);
  }
  if (!SCOPES.includes(scope)) fail(`--scope must be one of ${SCOPES.join(', ')}.`);
  return { cmd, scope };
}

function main() {
  const { cmd, scope } = parse(process.argv.slice(2));

  const probe = run(['--version'], { quiet: true });
  if (probe.code !== 0) fail('the claude command was not found. Install Claude Code first: https://code.claude.com/docs/en/setup');

  if (cmd === 'uninstall') {
    const r = run(['plugin', 'uninstall', PLUGIN, '--scope', scope]);
    show(r);
    if (r.code !== 0) fail('uninstall failed (exit ' + r.code + ').');
    console.log('\nRemoved. The marketplace entry stays; drop it with: claude plugin marketplace remove ' + MARKETPLACE);
    return;
  }

  let r = run(['plugin', 'marketplace', 'add', MARKETPLACE_SOURCE]);
  show(r);
  if (r.code !== 0) fail('adding the marketplace failed (exit ' + r.code + ').');

  if (cmd === 'update') {
    r = run(['plugin', 'marketplace', 'update', MARKETPLACE]);
    show(r);
    r = run(['plugin', 'update', PLUGIN, '--scope', scope]);
    show(r);
    if (r.code !== 0) fail('update failed (exit ' + r.code + ').');
    console.log('\nUpdated. Restart Claude Code sessions to load the new version.');
    return;
  }

  r = run(['plugin', 'install', PLUGIN, '--scope', scope]);
  show(r);
  if (r.code !== 0) fail('install failed (exit ' + r.code + ').');
  console.log(`
Installed ${PLUGIN} (scope: ${scope}). New Claude Code sessions load it.
Check it: start claude and ask it to run "git push --force" in a scratch repo; guard-bash refuses.
Off switch for one session: SKILLKEEL_ALLOW_DANGEROUS=1 claude
Docs: https://github.com/${MARKETPLACE_SOURCE}`);
}

main();
