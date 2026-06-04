import jwt from 'jsonwebtoken';

export function signUserToken(subject, secret) {
  // TODO(Day43-task01): sign a JWT with HS256, payload { sub: subject }, expiresIn `1h`.
  throw new Error('TODO(Day43-task01): implement signUserToken');
}

export function verifyUserToken(token, secret) {
  // TODO(Day43-task01): verify token and return decoded payload object (throw on invalid token).
  throw new Error('TODO(Day43-task01): implement verifyUserToken');
}
