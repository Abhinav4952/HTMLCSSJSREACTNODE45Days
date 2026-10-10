# Grading criteria — Blog CMS (InkBoard)

**Scale:** **/100** for the whole project (not per-task).  
**Audience:** instructor / AI grading agent.  
**Policy:** Leftover `TODO` comments are **not** penalized when the required behavior works (same as course guide v1.2.0). Score **missing or broken behavior** only.

## Weights (/100)

| Category | Points | What instructors check |
|----------|-------:|------------------------|
| Backend API & data model | **30** | Models match `DATA_MODEL.md`; routes implement the API contract; validation; status codes; indexes where specified |
| Frontend features & mockup fidelity | **30** | Pages from `PROJECT_INSTRUCTIONS.md` exist; layout roughly follows `docs/mockups/`; Bootstrap + per-component CSS pattern |
| Auth, roles & security | **15** | Register/login JWT; bcrypt hashing; role guards; protected routes; no secrets committed |
| Context / state & API integration | **10** | AuthContext (or equivalent) holds user/token; pages fetch via api client; no Redux required; welcome Home pattern extended |
| Code quality & structure | **10** | Clear folders; readable names; error/loading states; no silent failures |
| Docs & Git hygiene | **5** | README run steps work; `.env` not committed; sensible commit history if visible |

## Detailed checklist

### Backend API & data model (30)

- [ ] All collections/models from `DATA_MODEL.md` exist with required fields and validation
- [ ] References use ObjectId + `ref` / `populate` (or documented embedding) correctly
- [ ] Public list/detail endpoints work with pagination/filter as specified
- [ ] Authenticated create/update/delete endpoints enforce ownership or role rules
- [ ] Error responses use consistent JSON shape (`error`, `message`) and correct HTTP status codes
- [ ] Seed or manual create path exists so a reviewer can demo the app

### Frontend features & mockup fidelity (30)

- [ ] All required pages/routes from the instructions are present
- [ ] UI uses Bootstrap for layout and component CSS files for custom styles
- [ ] Loading, empty, and error states are visible for async data
- [ ] Forms validate client-side enough to prevent obvious bad submits
- [ ] Layout is recognizably aligned with the mockups (not pixel-perfect required)

### Auth, roles & security (15)

- [ ] Passwords hashed with bcrypt (never stored plain text)
- [ ] JWT issued on login; protected API routes reject missing/invalid tokens with **401**
- [ ] Role-restricted routes return **403** when authenticated but unauthorized
- [ ] Frontend hides/guards admin or role-only UI
- [ ] `.env` / secrets are gitignored; `.env.example` documents placeholders

### Context / state & API integration (10)

- [ ] AuthContext (or equivalent) holds user/token; pages fetch via api client; no Redux required; welcome Home pattern extended

### Code quality & structure (10)

- [ ] Backend keeps routes / controllers / models separation
- [ ] Frontend keeps pages / components / api (and store or context) separation
- [ ] No dead broken entrypoints (`npm run dev` / `npm start` work with valid `MONGO_URI`)

### Docs & Git hygiene (5)

- [ ] Project README run instructions are accurate
- [ ] Candidate did not commit `node_modules` or `.env`

## Banding

| Total | Label |
|------:|-------|
| 90–100 | Excellent — production-ready student project |
| 80–89 | Strong — core complete, minor gaps |
| 70–79 | Satisfactory — main flows work |
| 60–69 | Needs revision — important gaps |
| < 60 | Incomplete / redo |

## Hard-fail gates (automatic needs-revision)

- Real MongoDB / JWT secrets committed to git
- Passwords stored in plain text
- App cannot start even with a valid `MONGO_URI` and documented steps
- Core auth or core CRUD of the main resource is entirely missing

## Instructor evaluation steps

1. Copy `backend/.env.example` → `.env`, set a real `MONGO_URI` and `JWT_SECRET`.
2. `cd backend && npm install && npm run dev`
3. `cd frontend && npm install && npm run dev`
4. Walk the user stories in `PROJECT_INSTRUCTIONS.md` (happy path + one forbidden role action).
5. Spot-check models against `DATA_MODEL.md`.
6. Fill this rubric and leave max **3** prioritized improvement notes.
