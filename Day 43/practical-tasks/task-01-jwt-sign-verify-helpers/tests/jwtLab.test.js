import { describe, expect, it } from 'vitest';
import { signUserToken, verifyUserToken } from '../src/jwtLab.js';

describe('jwtLab', () => {
  const secret = 'unit-test-secret-do-not-reuse';

  it('round-trips subject claim', () => {
    const token = signUserToken('alice', secret);
    expect(typeof token).toBe('string');
    const payload = verifyUserToken(token, secret);
    expect(payload.sub).toBe('alice');
  });

  it('rejects wrong secret', () => {
    const token = signUserToken('bob', secret);
    expect(() => verifyUserToken(token, 'wrong')).toThrow();
  });
});
