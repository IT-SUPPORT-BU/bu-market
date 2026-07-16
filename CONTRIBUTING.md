# Contributing Guide — BU-MARKET

Welcome! As a developer on the BU-MARKET team, please review this guide to understand our git branch workflow, pull request guidelines, and code review standards.

---

## 🌿 Git Branch Strategy

We use a Git branching workflow to allow multiple developers and teams to work on the codebase simultaneously without merge conflicts.

### Branch Structure
1. `main` — Production branch. Only contains stable, working code.
2. `develop` — Integration branch. All features are merged here and verified before going to main.
3. `feature/` — Team feature branches. Created from `develop` and merged back via Pull Request.
   - `feature/authentication` (Authentication team)
   - `feature/marketplace` (Marketplace team)
   - `feature/subscriptions` (Subscriptions team)
   - `feature/payments` (Payments team)
   - `feature/moderation` (Moderation team)
   - `feature/frontend` (Frontend team)
   - `feature/testing` (Testing team)
   - `feature/deployment` (Deployment team)
4. `docs/project` — Documentation updates.

---

## 🛠️ Contribution Workflow

1. **Pull the latest changes:**
   Always start by updating your local `develop` branch:
   ```bash
   git checkout develop
   git pull origin develop
   ```

2. **Create your feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Write code & run tests:**
   Verify that all unit tests pass before committing:
   ```bash
   python manage.py test
   ```

4. **Commit & Push:**
   Commit code with descriptive, professional messages:
   ```bash
   git add .
   git commit -m "feat: implement seller limits verification clean check"
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request:**
   Submit a Pull Request (PR) from your feature branch to `develop`. A teammate must review and approve your PR before merging.
