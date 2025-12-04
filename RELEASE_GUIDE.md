# Release Guide v1.1.0

## 📋 Overview

This guide describes the process for releasing version **1.1.0** of Industrace, a **minor release** that includes new features, improvements, and fixes without breaking changes.

## 🎯 Release Type

**Minor Release (1.1.0)** according to [Semantic Versioning](https://semver.org/):
- **MAJOR (1.x.x)**: Breaking changes → Not applicable
- **MINOR (x.1.x)**: Backward compatible new features → ✅ **This is the case**
- **PATCH (x.x.1)**: Bug fixes → Not applicable (there are also fixes, but there are also new features)

## 📦 Release v1.1.0 Contents

### ✨ New Features
1. **Trash Management for Areas**
   - Soft delete for areas
   - Trash, restore, hard delete endpoints
   - UI aligned with Sites and Locations

2. **Multilingual Printed Kit**
   - PDF generation in Italian/English
   - Automatic support based on interface language

3. **Restructured Translation System**
   - Translation file consolidation (40 deleted, 19 new)
   - Complete IT/EN alignment
   - New centralized loader

4. **Improved Global Search**
   - Fixed Locations search with Area join
   - Auto-search when query changes
   - Improved result descriptions

### 🔧 Fixes and Improvements
1. **Filtered Asset Timeline**
   - Shows only changes related to the specific asset
   - `entity_id` filter in backend

2. **Performance**
   - New database indexes
   - Dashboard cache
   - Query optimizations

3. **Documentation**
   - Upgrade guide (`docs/UPGRADE.md`)
   - Performance documentation (`docs/PERFORMANCE_OPTIMIZATIONS.md`)

### 🗄️ Database Migrations
- `f5b3589a115e_add_deleted_at_to_areas.py` - Added `deleted_at` column to `areas`
- `add_performance_indexes.py` - Performance indexes

---

## 📝 Pre-Release Checklist

### 1. Code Verification
- [ ] All tests pass
- [ ] No linting errors
- [ ] Code review completed
- [ ] Database migrations tested

### 2. Update Versions

#### Frontend
```bash
# frontend/package.json
"version": "1.1.0"

# frontend/src/config/app.js
version: '1.1.0'
```

#### Backend
```bash
# If a __version__.py or similar file exists, update it
# Otherwise version can be in main.py or config.py
```

### 3. Update CHANGELOG.md
Move changes from `[Unreleased]` to `[1.1.0]`:

```markdown
## [1.1.0] - 2025-11-XX

### Added
- Trash management for Areas (soft delete, restore, hard delete)
- Multilingual printed kit (Italian/English)
- Restructured and consolidated translation system
- Improved global search with auto-search
- Upgrade guide (`docs/UPGRADE.md`)
- Database indexes for performance
- Dashboard cache

### Changed
- Complete translation system restructuring
  - Translation file consolidation (40 deleted, 19 new)
  - Complete IT/EN translation alignment
  - New centralized loader (`loader-final.js`)
- Asset timeline now shows only changes related to the specific asset
- Improved global search with correct join for Locations

### Fixed
- Asset timeline showed all changes instead of only those of the asset
- Global search didn't find results for Locations
- IT/EN translation alignment

### Migration
- Added `deleted_at` column to `areas` table
- Added indexes to improve query performance
```

### 4. Create Release Notes
Create `RELEASE_NOTES_v1.1.0.md` based on `RELEASE_NOTES_v1.0.0.md`:

```markdown
# 🚀 Industrace v1.1.0 - Minor Release

**Release Date**: November 2025  
**Version**: 1.1.0  
**Type**: Minor Release (backward compatible)

## 🎯 Overview

Industrace v1.1.0 introduces new features, translation system improvements, and important fixes, maintaining full compatibility with version 1.0.0.

## ✨ New Features

### Trash Management for Areas
- Soft delete for areas
- Restore and hard delete
- UI aligned with Sites and Locations

### Multilingual Printed Kit
- PDF generation in Italian/English
- Automatic support based on interface language

### Restructured Translation System
- Complete consolidation and IT/EN alignment
- New centralized loader
- Translation automation scripts

## 🔧 Improvements

- Improved global search
- Asset timeline filtered for specific asset
- Performance optimized with new indexes
- Dashboard cache

## 🐛 Fixes

- Asset timeline showed all changes
- Global search didn't find Locations results
- IT/EN translation alignment

## 📚 Documentation

- Upgrade guide (`docs/UPGRADE.md`)

## 🗄️ Database Migrations

Migrations are applied automatically on startup. See `docs/UPGRADE.md` for details.

## ⬆️ Upgrade from v1.0.0

See `docs/UPGRADE.md` for the complete upgrade guide.
```

### 5. Commit and Tag

```bash
# 1. Add all modified files
git add .

# 2. Commit with descriptive message
git commit -m "chore: prepare release v1.1.0

- Add trash management for Areas
- Add multilingual printed kit
- Restructure translation system
- Improve global search
- Fix asset timeline filtering
- Add upgrade guide
- Add performance documentation
- Add database migrations"

# 3. Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0: New features and improvements"

# 4. Push commit and tag
git push origin main
git push origin v1.1.0
```

### 6. Create GitHub Release

1. Go to GitHub → Releases → "Draft a new release"
2. Select tag `v1.1.0`
3. Title: `v1.1.0 - Minor Release`
4. Description: Copy from `RELEASE_NOTES_v1.1.0.md`
5. Publish the release

---

## 🚀 Release Process

### Step 1: Local Preparation
```bash
# Make sure you're on main and updated
git checkout main
git pull origin main

# Verify status
git status
```

### Step 2: Update Versions
Update manually:
- `frontend/package.json` → `"version": "1.1.0"`
- `frontend/src/config/app.js` → `version: '1.1.0'`

### Step 3: Update CHANGELOG.md
Move changes from `[Unreleased]` to `[1.1.0]` with date

### Step 4: Create RELEASE_NOTES_v1.1.0.md
Copy template and customize

### Step 5: Final Tests
```bash
# Test frontend
cd frontend && npm run build

# Test backend (if there are tests)
cd backend && pytest

# Verify migrations
docker-compose exec backend alembic current
docker-compose exec backend alembic history
```

### Step 6: Commit and Tag
```bash
git add .
git commit -m "chore: release v1.1.0"
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main
git push origin v1.1.0
```

### Step 7: GitHub Release
Create release on GitHub with tag `v1.1.0`

---

## 📋 Post-Release

### 1. Update [Unreleased] in CHANGELOG
Remove moved changes and leave only:
```markdown
## [Unreleased]

### Added
- Future features and improvements
```

### 2. Verify Upgrade
- [ ] Test upgrade from v1.0.0 to v1.1.0
- [ ] Verify migrations apply correctly
- [ ] Test all new features

### 3. Communication
- [ ] Update main documentation if necessary
- [ ] Communicate release to users (if applicable)

---

## 🔄 Rollback (if necessary)

If something goes wrong:

```bash
# Remove local tag
git tag -d v1.1.0

# Remove remote tag
git push origin :refs/tags/v1.1.0

# Revert commit (if not yet pushed)
git reset --hard HEAD~1

# If already pushed, create new fix commit
git revert HEAD
```

---

## 📊 Versions to Update

### Frontend
- ✅ `frontend/package.json` → `"version": "1.1.0"`
- ✅ `frontend/src/config/app.js` → `version: '1.1.0'`

### Backend
- If `backend/__version__.py` or similar exists, update it
- Otherwise version can be in `main.py` or `config.py`

### Documentation
- ✅ `CHANGELOG.md` → Add `[1.1.0]` section
- ✅ `RELEASE_NOTES_v1.1.0.md` → Create new file

---

## ✅ Final Checklist

Before publishing the release:

- [ ] Versions updated in all files
- [ ] CHANGELOG.md updated
- [ ] RELEASE_NOTES_v1.1.0.md created
- [ ] Tests passed
- [ ] Database migrations tested
- [ ] Frontend build works
- [ ] Commit done
- [ ] Tag created
- [ ] Push to GitHub completed
- [ ] GitHub release created

---

## 📝 Notes

- This is a **minor release**, therefore **backward compatible**
- Database migrations are applied automatically
- There are no breaking changes
- Users can upgrade without issues from v1.0.0
