#!/usr/bin/env node
// RU: Простая CLI для управления сервисами и монтированием
const { spawnSync } = require('child_process');

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
    const devPattern = /^\/dev\/[\w/-]+$/;
    const dirPattern = /^\/[\w/.-]+$/;
    if (!dev || !dir || !devPattern.test(dev) || !dirPattern.test(dir)) {
      console.error('Неверный формат устройства или директории');
      return usage();
    }
    const result = spawnSync('mount', [dev, dir], { stdio: 'inherit' });
    if (result.error) {
      console.error(`Ошибка выполнения mount: ${result.error.message}`);
      process.exit(1);
    }
    if (result.status !== 0) {
      console.error(`Не удалось смонтировать ${dev} в ${dir}`);
      process.exit(result.status || 1);
    }
    break;
  }
  case 'service': {
    const svc = args[1];
    const svcPattern = /^[\w-]+$/;
    if (!svc || !svcPattern.test(svc)) {
      console.error('Неверное имя сервиса');
      return usage();
    }
    const result = spawnSync('rc-service', [svc, 'start'], { stdio: 'inherit' });
    if (result.error) {
      console.error(`Ошибка запуска сервиса ${svc}: ${result.error.message}`);
      process.exit(1);
    }
    if (result.status !== 0) {
      console.error(`Сервис ${svc} завершился с кодом ${result.status}`);
      process.exit(result.status || 1);
    }
    break;
  }
  default:
    usage();
}

