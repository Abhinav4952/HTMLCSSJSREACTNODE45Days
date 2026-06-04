import { describe, expect, it } from 'vitest';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { joinRelativeToModule, moduleDirname } from '../src/pathLab.js';

const here = path.dirname(fileURLToPath(import.meta.url));
const srcDir = path.join(here, '..', 'src');

describe('pathLab', () => {
  it('moduleDirname points at src/', () => {
    const url = pathToFileURL(path.join(srcDir, 'pathLab.js')).href;
    expect(moduleDirname(url)).toBe(srcDir);
  });

  it('joinRelativeToModule resolves fixtures/hello.txt', async () => {
    const url = pathToFileURL(path.join(srcDir, 'pathLab.js')).href;
    const abs = joinRelativeToModule(url, '..', 'fixtures', 'hello.txt');
    const text = await fs.promises.readFile(abs, 'utf8');
    expect(text.trim()).toBe('hello');
  });
});
