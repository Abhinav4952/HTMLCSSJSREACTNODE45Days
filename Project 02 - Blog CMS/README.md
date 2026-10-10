# Blog CMS (InkBoard)

Full-stack capstone project after **Day 45** of the HTML/CSS/React/Node course.

## What you are building

A production-style **Blog CMS** with:

- React (Vite) + React Router + Bootstrap frontend
- Express + Mongoose + JWT backend
- MongoDB Atlas (you supply the connection string)
- React Context API is required for auth (no Redux in this project).

Read these files **in order**:

1. This **README.md** — setup and run
2. **[PROJECT_INSTRUCTIONS.md](./PROJECT_INSTRUCTIONS.md)** — full product + API + UI spec (includes mockup links)
3. **[DATA_MODEL.md](./DATA_MODEL.md)** — MongoDB collections and document shapes
4. **[GRADING_CRITERIA.md](./GRADING_CRITERIA.md)** — how the project is scored /100

Mockups live in [`docs/mockups/`](./docs/mockups/).

## Prerequisites

- Node.js **18+**
- npm
- A **MongoDB Atlas** cluster (or any MongoDB you can reach with a connection string)
- Completed course Days **01–45** (or equivalent knowledge)

## Critical: MongoDB connection string

The backend **will not stay running** until you set a real URI.

1. Copy the example env file:

```bash
cd backend
cp .env.example .env
```

2. Edit `backend/.env` and replace the placeholder:

```env
MONGO_URI=mongodb+srv://<username>:<password>@<cluster-host>/<database-name>?retryWrites=true&w=majority
PORT=5002
JWT_SECRET=replace-with-a-long-random-string
CLIENT_ORIGIN=http://localhost:5173
```

### Format notes

- Use the Atlas **Connect → Drivers** string.
- Replace `<username>` and `<password>` (URL-encode special characters in the password).
- Replace `<cluster-host>` (example shape: `cluster0.xxxxx.mongodb.net`).
- Replace `<database-name>` with a dedicated DB name for this project.
- Keep `?retryWrites=true&w=majority` (or Atlas defaults).

If `MONGO_URI` is missing or invalid, `connectDB` logs `MongoDB Connection Failed 💥` and **`process.exit(1)`**.

**Never commit `.env`.** Only `.env.example` is tracked.

## Project structure

```
Blog CMS/
  README.md
  PROJECT_INSTRUCTIONS.md
  DATA_MODEL.md
  GRADING_CRITERIA.md
  docs/mockups/
  backend/          Express API (ES modules)
  frontend/         Vite + React app
```

### Styling convention (follow this for new components)

- Put each component in its own folder: `ComponentName/ComponentName.jsx` + `ComponentName.css`
- Import the CSS file at the top of the JSX file
- Use **Bootstrap** classes for layout (`container`, `row`, `col-*`, `card`, `btn`, `navbar`, forms)
- Put **custom** visual rules only in the component CSS, with a component prefix (example: `.home-hero`, `.navbar-brand-logo`)

### State management

- Use **React Context** for auth (boilerplate `AuthContext.jsx`).
- Use local component state / `useReducer` for forms and lists — **do not add Redux** unless as stretch.


## Run the backend

```bash
cd backend
cp .env.example .env   # first time only; then edit MONGO_URI
npm install
npm run dev            # nodemon on PORT from .env (default 5002)
```

Smoke checks:

- `GET http://localhost:5002/api/health` → `{ "status": "ok" }`
- `GET http://localhost:5002/api/welcome` → welcome JSON

```bash
cd backend
npm test
```

## Run the frontend

In a **second** terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the URL Vite prints (usually `http://localhost:5173`).

The Home page calls **`GET /api/welcome`** through the Vite proxy (`vite.config.js` → `http://localhost:5002`).

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Backend exits immediately | Set a valid `MONGO_URI` in `backend/.env` |
| Home shows API error | Start backend; confirm proxy port matches `PORT` |
| CORS errors | Set `CLIENT_ORIGIN=http://localhost:5173` |
| 401 on every request | Attach `Authorization: Bearer <token>` after login |

## Production-readiness expectations

Treat this like a junior engineer deliverable: env-based config, clear folders, consistent API errors, authZ on mutating routes, loading/empty/error UI states, and a README another developer can follow.
