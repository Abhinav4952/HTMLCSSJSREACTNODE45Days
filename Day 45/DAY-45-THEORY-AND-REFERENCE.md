# Day 45 — Capstone API: Express + Auth + Mongoose

**Primary theme:** Ship a small but realistic **authenticated JSON API** with **Mongo persistence**.  
**Estimated study time:** 2–4 hours theory + 5–8 hours tasks  
**Related tasks:** `task-01-capstone-users-register`, `task-02-capstone-login-jwt-profile`, `task-03-capstone-notes-crud`, `task-04-capstone-notes-ownership-and-errors`  
**Instruction alignment:** Maps to **Express + JWT + Mongo (Mongoose)** integration outcomes.

---

## Overview

You will model **users**, issue **JWTs**, and persist **notes** scoped to a user. The capstone stresses **ownership checks** (mutations must prove the `userId` on the document matches the authenticated subject) and **clean HTTP errors** (avoid leaking stack traces to clients while logging server-side).

---

## Day roadmap

1. Threat model refresher (labs vs production)
2. Password storage with **bcrypt** hashes
3. JWT claims for `sub` / user identity
4. Ownership modeling with `ObjectId` refs
5. Error middleware patterns
6. Further reading & glossary

---

## 1. Password storage (labs)

### What it is

Store **bcrypt** hashes (`passwordHash`), never plaintext passwords, in the database.

#### Why it exists / why it matters

Database leaks happen; hashes buy time.

#### Examples

```js
import bcrypt from 'bcryptjs';

const passwordHash = await bcrypt.hash(password, 10);
const ok = await bcrypt.compare(password, passwordHash);
```

#### Quick checks

1. Why is `bcrypt.compare` used at login instead of re-hashing and comparing strings?

---

## 2. Ownership with Mongo references

### What it is

Store `userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true }` on child documents.

#### Why it exists / why it matters

Authorization becomes “does `doc.userId` match `req.user.sub`?” (lab simplification).

#### Quick checks

1. Why is trusting client-sent `userId` in POST bodies dangerous?

---

## 3. Centralized errors

### What it is

Map known failures (`CastError`, validation) to **400/404** and unknowns to **500** with a generic client body.

#### Quick checks

1. Why avoid returning `err.message` verbatim for 500 responses?

---

## Common mistakes & debugging

- Returning **`passwordHash`** in JSON responses.
- Forgetting **`select:false`** and accidentally loading hashes.
- Treating JWT `sub` as display name—here it should be a **stable user id**.

---

## Further reading

- [OWASP — Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Mongoose — Populate](https://mongoosejs.com/docs/populate.html)

---

## Glossary

| Term | Meaning |
|------|---------|
| **Ownership** | Only the creating user may mutate their rows (lab rule). |

---

## Answers

**§1:** Constant-time comparison + salt embedded in hash string.  
**§2:** Clients could impersonate other users.  
**§3:** Information disclosure + harder client UX; log details server-side only.
