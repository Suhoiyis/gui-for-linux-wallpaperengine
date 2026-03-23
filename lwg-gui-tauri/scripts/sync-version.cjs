#!/usr/bin/env node

/**
 * sync-version.js
 * 
 * Syncs version number from tauri.conf.json to package.json and Cargo.toml
 * This ensures a single source of truth for the version number.
 * 
 * Usage: node scripts/sync-version.js
 */

const fs = require('fs');
const path = require('path');

const ROOT_DIR = path.join(__dirname, '..');
const TAURI_CONF_PATH = path.join(ROOT_DIR, 'src-tauri', 'tauri.conf.json');
const PACKAGE_JSON_PATH = path.join(ROOT_DIR, 'package.json');
const CARGO_TOML_PATH = path.join(ROOT_DIR, 'src-tauri', 'Cargo.toml');

function main() {
  console.log('[sync-version] Starting version sync...\n');

  // 1. Read version from tauri.conf.json
  const tauriConf = JSON.parse(fs.readFileSync(TAURI_CONF_PATH, 'utf-8'));
  const version = tauriConf.version;

  if (!version) {
    console.error('[sync-version] ERROR: No version found in tauri.conf.json');
    process.exit(1);
  }

  console.log(`[sync-version] Source version: ${version} (from tauri.conf.json)`);

  // 2. Sync to package.json
  const packageJson = JSON.parse(fs.readFileSync(PACKAGE_JSON_PATH, 'utf-8'));
  const oldPackageVersion = packageJson.version;
  packageJson.version = version;
  fs.writeFileSync(PACKAGE_JSON_PATH, JSON.stringify(packageJson, null, 2) + '\n', 'utf-8');
  console.log(`[sync-version] package.json: ${oldPackageVersion} -> ${version}`);

  // 3. Sync to Cargo.toml
  let cargoToml = fs.readFileSync(CARGO_TOML_PATH, 'utf-8');
  const versionRegex = /^version\s*=\s*"[^"]*"/m;
  const match = cargoToml.match(versionRegex);
  
  if (match) {
    const oldCargoVersion = match[0].match(/"([^"]*)"/)[1];
    cargoToml = cargoToml.replace(versionRegex, `version = "${version}"`);
    fs.writeFileSync(CARGO_TOML_PATH, cargoToml, 'utf-8');
    console.log(`[sync-version] Cargo.toml: ${oldCargoVersion} -> ${version}`);
  } else {
    console.error('[sync-version] ERROR: Could not find version field in Cargo.toml');
    process.exit(1);
  }

  console.log('\n[sync-version] ✅ Version sync completed successfully!');
}

main();