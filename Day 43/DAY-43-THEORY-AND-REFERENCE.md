# Day 43 — JWT Authentication (Sign, Verify, Bearer Middleware)

**Primary theme:** Stateless authentication with **JWTs** in an Express API.  
**Estimated study time:** 2–3 hours theory + 3–6 hours tasks  
**Related tasks:** `task-01-jwt-sign-verify-helpers`, `task-02-login-route-bearer-auth`, `task-03-roles-401-vs-403`, `task-04-refresh-free-token-claims`  
**Instruction alignment:** Maps to **JWT-based auth** from the master topic list.

---

## Overview

**JSON Web Tokens (JWTs)** encode signed claims that clients present on later requests. They are **not a database**; they are a **portable proof** the server (or identity provider) issued. You will practice **HS256** signing with a shared secret, attach tokens with **`Authorization: Bearer`**, and reason about **401 vs 403**.

This week is still a **lab**: tokens in `curl` headers, not a polished SPA login. Threat model notes appear in each task’s instructions—**never commit secrets**.

---

## Day roadmap

1. JWT structure: header, payload, signature
2. Signing and verifying with `jsonwebtoken`
3. Express middleware: extracting Bearer tokens
4. Authorization vs authentication
5. Common mistakes & debugging
6. Further reading & glossary

---

## 1. JWT structure (high level)

### What it is

A JWT is `base64url(header).base64url(payload).signature` where the signature proves integrity under a secret or key pair.

#### Why it exists / why it matters

It lets services **avoid server-side sessions** for many APIs (tradeoffs apply).

#### Pros and cons

- **Pros:** Horizontal scaling without sticky sessions; mobile-friendly.
- **Cons:** **Cannot revoke** individual tokens trivially without extra machinery; leaks are dangerous.

#### What happens without it / when misused

Secrets committed to GitHub → world owns your API.

#### Syntax and rules

- Prefer short **exp** (`exp` claim) in real systems.
- Validate **`alg`** where applicable (avoid `none` attacks in custom parsers—libraries help).

#### Examples

**Tiny — decode mentally**

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZSJ9....sig...
```

**Tiny — sign with HS256 (Node)**

```js
import jwt from 'jsonwebtoken';
const token = jwt.sign({ sub: 'alice' }, process.env.JWT_SECRET, { expiresIn: '1h' });
```

**Medium — verify**

```js
const payload = jwt.verify(token, process.env.JWT_SECRET);
```

#### Quick checks

1. Why is a leaked `JWT_SECRET` catastrophic for HS256 tokens?
2. Name one reason **403** is more appropriate than **401** for “logged in but not allowed.”

---

## 2. Express middleware pattern

### What it is

A function `(req, res, next)` that can attach **`req.user = payload`** after verification.

#### Syntax and rules

```js
const auth = (req, res, next) => {
  const header = req.get('authorization') || '';
  const [scheme, token] = header.split(' ');
  if (scheme !== 'Bearer' || !token) return res.status(401).json({ error: 'missing_token' });
  try {
    req.user = jwt.verify(token, process.env.JWT_SECRET);
    next();
  } catch {
    return res.status(401).json({ error: 'invalid_token' });
  }
};
```

#### Quick checks

1. Why read **`Authorization`** header instead of query strings for tokens?

---

## Common mistakes & debugging

- Using **GET** bodies for secrets (don’t).
- Forgetting **`Bearer `** prefix parsing.
- Treating JWT as encryption—it is **encoding + integrity**, not confidentiality.

---

## Further reading

- [JWT.io — Introduction](https://jwt.io/introduction)
- [jsonwebtoken package README](https://github.com/auth0/node-jsonwebtoken)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Claim** | JSON field inside payload (`sub`, `role`, `exp`). |
| **Bearer** | HTTP auth scheme carrying opaque token value. |

---

## Answers

**Section 1:**  
1. Attacker can mint arbitrary tokens.  
2. Identity is known/valid but authorization fails (wrong role).

**Section 2:**  
1. URLs leak via logs, Referer headers, browser history.
