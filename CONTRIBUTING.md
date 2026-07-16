# Contributing Guide — BU-MARKET (Forking Workflow)

Welcome! Because we are a large team, we use the **Forking Workflow**. This allows you to work on your own copy of the codebase and submit Pull Requests without needing direct write access to the main organization repository.

---

## 🌿 The Forking Workflow

### Step 1: Fork the Repository
1. Navigate to the main repository: [https://github.com/IT-SUPPORT-BU/bu-market](https://github.com/IT-SUPPORT-BU/bu-market)
2. In the top-right corner of the page, click the **Fork** button.
3. This creates a copy of the repository in your personal GitHub account (e.g., `https://github.com/your-username/bu-market`).

### Step 2: Clone Your Fork
Clone your personal fork to your local machine:
```bash
git clone https://github.com/your-username/bu-market.git
cd bu-market
```

### Step 3: Configure Remote Upstream
To keep your fork in sync with the main repository, add the original repository as a remote named `upstream`:
```bash
git remote add upstream https://github.com/IT-SUPPORT-BU/bu-market.git
```
Verify your remotes:
```bash
git remote -v
# Should show 'origin' pointing to your fork, and 'upstream' pointing to IT-SUPPORT-BU
```

### Step 4: Sync Your Fork
Before starting any new work, always pull the latest changes from the upstream `develop` branch:
```bash
git checkout develop
git pull upstream develop
```

### Step 5: Create a Feature Branch
Create a new branch for the feature or issue you are working on:
```bash
git checkout -b feature/your-feature-name
```

### Step 6: Commit and Push
1. Write your code and verify it passes tests:
   ```bash
   python manage.py test
   ```
2. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: implement seller limits verification clean check"
   ```
3. Push your feature branch to your personal fork (`origin`):
   ```bash
   git push origin feature/your-feature-name
   ```

### Step 7: Submit a Pull Request
1. Go to your fork page on GitHub.
2. Click **Compare & pull request** next to your feature branch.
3. Set the base repository to `IT-SUPPORT-BU/bu-market` and the base branch to `develop`.
4. Submit the Pull Request!
