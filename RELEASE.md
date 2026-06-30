# Release Guide

## First public release

1. Create a new GitHub repository under your own account, for example `audiototext`.
2. Add the new remote:

```bash
git remote add origin https://github.com/<your-account>/audiototext.git
```

3. Review:

```bash
python -m pytest
python -m audiototext --help
git status
```

4. Commit the rebuilt project:

```bash
git add .
git commit -m "Rebuild project as audiototext CLI"
```

5. Rename the primary branch if needed:

```bash
git branch -M main
```

6. Push:

```bash
git push -u origin main
```

7. Tag the first release:

```bash
git tag v0.1.0
git push origin v0.1.0
```

## Before tagging

- Replace placeholder example content with files you can legally distribute.
- Review author, package, and license metadata.
- Decide whether you want `whisper-1` to remain the default OpenAI API path or whether you want to revise provider defaults against the current official docs before release.
