================================================================================
🏢 WEYLAND-YUTANI TRANSMUTE TOOL - GIT WORKFLOW
================================================================================

STEP-BY-STEP GUIDE TO PUSH TO GITHUB

================================================================================
STEP 1: INITIALIZE GIT REPOSITORY
================================================================================

Open Command Prompt in project folder:
    cd C:\Users\ezrashiv\Desktop\Weyland-Yutani-Transmute-Tool

Initialize git:
    git init

Expected output:
    Initialized empty Git repository in ...

================================================================================
STEP 2: ADD ALL FILES
================================================================================

Add all files to staging:
    git add .

Check what will be committed:
    git status

Expected output:
    On branch master
    Changes to be committed:
      new file: README.md
      new file: src/main.py
      ... (all your files)

================================================================================
STEP 3: CREATE INITIAL COMMIT
================================================================================

Option A - Simple commit message:
    git commit -m "Initial commit: Weyland-Yutani Transmute Tool v0.1.0"

Option B - Detailed commit message:
    git commit -m "Initial commit: Weyland-Yutani Transmute Tool v0.1.0" -m "Professional STL mesh repair and STEP conversion utility for 3D printing. Automatically detects and fixes mesh defects that cause hollow slicing."

Option C - Multi-line commit (recommended):
    git commit -m "Initial commit: Weyland-Yutani Transmute Tool v0.1.0

Professional STL mesh repair and STEP conversion utility for 3D printing.

Features:
- Mesh analysis and defect detection
- Automatic repair of non-manifold geometry
- STL export for 3D printing
- STEP conversion for CAD software
- User-friendly GUI interface

Tech stack: Python 3.8+, trimesh, tkinter, FreeCAD API
License: MIT"

Expected output:
    [master (root-commit) abc1234] Initial commit: ...
    XX files changed, XXXX insertions(+)
    create mode 100644 README.md
    ...

================================================================================
STEP 4: RENAME BRANCH TO MAIN (GitHub standard)
================================================================================

Rename master to main:
    git branch -M main

================================================================================
STEP 5: CREATE GITHUB REPOSITORY
================================================================================

Go to GitHub.com and:
1. Click "+" in top right → "New repository"
2. Repository name: Weyland-Yutani-Transmute-Tool
3. Description: Professional STL mesh repair and STEP conversion tool for 3D printing
4. Visibility: Public (recommended)
5. DO NOT initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

================================================================================
STEP 6: CONNECT LOCAL REPO TO GITHUB
================================================================================

Copy the repository URL from GitHub (looks like):
    https://github.com/YOUR_USERNAME/Weyland-Yutani-Transmute-Tool.git

Add remote:
    git remote add origin https://github.com/YOUR_USERNAME/Weyland-Yutani-Transmute-Tool.git

Verify remote:
    git remote -v

Expected output:
    origin  https://github.com/YOUR_USERNAME/... (fetch)
    origin  https://github.com/YOUR_USERNAME/... (push)

================================================================================
STEP 7: PUSH TO GITHUB
================================================================================

Push to GitHub:
    git push -u origin main

You may be prompted for GitHub credentials.

Expected output:
    Enumerating objects: XX, done.
    Counting objects: 100% (XX/XX), done.
    ...
    To https://github.com/YOUR_USERNAME/Weyland-Yutani-Transmute-Tool.git
     * [new branch]      main -> main

================================================================================
STEP 8: VERIFY ON GITHUB
================================================================================

Go to: https://github.com/YOUR_USERNAME/Weyland-Yutani-Transmute-Tool

You should see:
✅ All your files
✅ README.md displayed on the main page
✅ License badge
✅ File structure

================================================================================
FUTURE COMMITS (After making changes)
================================================================================

1. Check what changed:
    git status

2. Add changed files:
    git add .
    OR add specific files:
    git add src/main.py

3. Commit changes:
    git commit -m "Description of changes"

4. Push to GitHub:
    git push

================================================================================
USEFUL GIT COMMANDS
================================================================================

Check status:
    git status

View commit history:
    git log
    git log --oneline

View changes before committing:
    git diff

Undo changes (before commit):
    git checkout -- filename

Create a new branch:
    git checkout -b feature-name

Switch branches:
    git checkout main

Merge branch:
    git merge feature-name

Pull latest changes:
    git pull

================================================================================
GITHUB REPOSITORY SETTINGS (After pushing)
================================================================================

Add Topics/Tags:
1. Go to repository on GitHub
2. Click "⚙️ Settings" (or the gear icon near About)
3. Add topics: 3d-printing, stl, mesh-repair, python, cad

Add Description:
1. Click "⚙️" next to About
2. Add: "Professional STL mesh repair and STEP conversion tool for 3D printing"
3. Add website (optional)
4. Save changes

Enable Features:
1. Go to Settings → General
2. Enable: Issues, Wiki (optional), Discussions (optional)

================================================================================
TROUBLESHOOTING
================================================================================

Error: "git: command not found"
Fix: Install Git from https://git-scm.com/downloads

Error: "Permission denied (publickey)"
Fix: Set up SSH keys or use HTTPS with personal access token

Error: "Updates were rejected"
Fix: Pull first: git pull origin main --rebase
     Then push: git push origin main

Error: "Large files"
Fix: Add to .gitignore or use Git LFS for files >100MB

================================================================================
QUICK REFERENCE
================================================================================

Initial Setup:
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin URL
    git push -u origin main

Regular Workflow:
    git add .
    git commit -m "Description"
    git push

================================================================================

Ready to share your work with the world! 🚀

================================================================================
