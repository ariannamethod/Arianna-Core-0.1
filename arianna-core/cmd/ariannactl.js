#!/usr/bin/env node
// RU: Простая CLI для управления сервисами и монтированием
const { execSync } = require('child_process');

function usage() {
  console.log('Использование: ariannactl <mount|service> ...');
}

const args = process.argv.slice(2);
if (args.length === 0) {
  usage();
  process.exit(1);
}

switch (args[0]) {
  case 'mount': {
    const dev = args[1];
    const dir = args[2];
    if (!dev || !dir) {
      return usage();
    }
    execSync(`mount ${dev} ${dir}`, { stdio: 'inherit' });
    break;
  }
  case 'service': {
    const svc = args[1];
    if (!svc) return usage();
    execSync(`rc-service ${svc} start`, { stdio: 'inherit' });
    break;
  }
  default:
    usage();
}
