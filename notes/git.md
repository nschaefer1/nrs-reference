
## Git Command Reference

### Repo Setup

- Initialize repository `git init`
- Clone repository `git clone <repo_url>`

---

### Staging & Commits

- Check status `git status`
- Stage file `git add <file>`
- Stage all changes `git add .`
- Commit `git commit -m "message"`
- Amend last commit `git commit --amend`
- Amend last commit, no edits `git commit --amend --no-edit`

---

### Branching

- List branches `git branch`
- Create brnach `git branch <branch_name>`
- Switch branch `git checkout <branch_name>`
- Create and switch `git checkout -b <branch_name>`
- Delete branch `git branch -d <branch_name>`

---

### Remote

- View remotes `git remote -v`
- Add remote `git remote add origin <url>`
- Push `git push origin <branch>`
- Pull `git pull`
- Fetch `git fetch`

---

### Merging & rebasing

- Merge branch `git merge <branch>`
- Rebase `git rebase <branch>`
- Abort rebase `git rebase --abort`

---

### Undo / Fix

- Unstage file `git restore --staged <file>`
- Discard changes `git restore <file>`
- Reset to last commit `git reset --hard`
- Soft reset to last commit `git reset --soft <commit>`
- Reset to specific commit `git reset --hard <commit>`

---

### History

- Log `git log`
- Compact log `git log --oneline`
- Show changes `git diff`

---

### Stashing

- Stash changes `git stash`
- List stashes `git stash lists`
- Apply stash `git stash apply`
- Pop stash `git stash pop`

### Tags

- Create tag `git tag <tag>`
- Push tag `git push origin <tag>`
- List tags `git tag`