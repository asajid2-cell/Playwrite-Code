# Database Backup & Restore Guide

Complete guide for backing up and restoring OurSpace database and user uploads on the VPS.

## Understanding What Gets Backed Up

### Included in Database Backup:
- **User accounts** (usernames, passwords, login info)
- **User profiles** (all customizations, themes, layouts, settings)
- **Friendships and social connections**
- **Messages** (inbox, sent messages)
- **Friend requests** (pending, accepted, rejected)
- **Blocked users**
- **Profile comments**
- **Admin settings**
- **Uploaded files** (profile pictures, banners, photo walls, backgrounds)

### NOT Included (Managed Separately):
- Application code (managed by git)
- Analysis cache (can be regenerated)
- Audio files (if stored elsewhere)

## Quick Reference Commands

### Create Full Backup
```bash
~/backup_db.sh
```

### Restore Latest Backup
```bash
cd ~/apps/harmonizer/backend
rm -rf ourspace_data
cp -r ~/backups/full_backup_*/ourspace_data ./
chown -R harmonizer:harmonizer ourspace_data
sudo docker compose restart
```

---

## Complete Backup Tutorial

### Step 1: SSH into the VPS

```bash
ssh harmonizer@harminoplet
```

You'll be at your home directory (`~` or `/home/harmonizer`).

### Step 2: Navigate to Backend Directory

```bash
cd ~/apps/harmonizer/backend
```

### Step 3: Create a Backup

#### Option A: Using the Backup Script (Recommended)

```bash
# Run the automated backup script
~/backup_db.sh

# Verify backup was created
ls -lh ~/backups/
```

The script automatically:
- Creates timestamped backup
- Keeps only the last 10 backups
- Backs up both database and uploads

#### Option B: Manual Backup

```bash
# Create backup directory with timestamp
mkdir -p ~/backups/full_backup_$(date +%Y%m%d_%H%M%S)

# Copy database and uploads
cp -r ~/apps/harmonizer/backend/ourspace_data ~/backups/full_backup_$(date +%Y%m%d_%H%M%S)/

# Verify backup
ls -la ~/backups/full_backup_*/
```

### Step 4: Verify Backup Contents

```bash
# List all backups
ls -lh ~/backups/

# Check contents of latest backup
ls -la ~/backups/full_backup_*/ourspace_data/
```

You should see:
- `ourspace.db` - The main database file
- User folders (e.g., `1/`, `2/`) containing uploaded images

---

## Complete Restore Tutorial

### Step 1: SSH into the VPS

```bash
ssh harmonizer@harminoplet
```

### Step 2: Stop the Application

```bash
cd ~/apps/harmonizer
sudo docker compose down
```

Wait for containers to stop completely.

### Step 3: Backup Current State (Optional but Recommended)

Before restoring, back up the current state in case you need to revert:

```bash
mkdir -p ~/backups/pre_restore_$(date +%Y%m%d_%H%M%S)
cp -r ~/apps/harmonizer/backend/ourspace_data ~/backups/pre_restore_$(date +%Y%m%d_%H%M%S)/ 2>/dev/null || true
```

### Step 4: List Available Backups

```bash
ls -lh ~/backups/
```

You'll see entries like:
```
full_backup_20251116_085627
full_backup_20251116_120000
```

### Step 5: Choose and Restore a Backup

#### Option A: Restore Latest Backup

```bash
cd ~/apps/harmonizer/backend

# Remove current database
rm -rf ourspace_data

# Find and copy the latest backup
LATEST_BACKUP=$(ls -td ~/backups/full_backup_* | head -1)
cp -r "$LATEST_BACKUP/ourspace_data" ./

# Fix permissions
chown -R harmonizer:harmonizer ourspace_data
```

#### Option B: Restore Specific Backup by Date

```bash
cd ~/apps/harmonizer/backend

# Remove current database
rm -rf ourspace_data

# Restore specific backup (replace with your timestamp)
cp -r ~/backups/full_backup_20251116_085627/ourspace_data ./

# Fix permissions
chown -R harmonizer:harmonizer ourspace_data
```

### Step 6: Verify Restoration

```bash
# Check that database file exists
ls -lh ourspace_data/

# Should see:
# ourspace.db
# User folders with uploaded files
```

### Step 7: Restart the Application

```bash
cd ~/apps/harmonizer
sudo docker compose up -d
```

### Step 8: Verify Application is Running

```bash
# Check container status
sudo docker compose ps

# Check logs
sudo docker compose logs -f harmonizer
```

Press `Ctrl+C` to exit logs.

### Step 9: Test the Application

1. Visit your site in a browser
2. Try logging in with a known user
3. Verify profile data is restored
4. Check that uploaded images are visible

---

## Creating Automated Backup Script

If you haven't already set up the automated backup script:

### Step 1: Create the Script

```bash
cat > ~/backup_db.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=~/backups
mkdir -p $BACKUP_DIR
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create timestamped backup
if [ -d ~/apps/harmonizer/backend/ourspace_data ]; then
    cp -r ~/apps/harmonizer/backend/ourspace_data $BACKUP_DIR/full_backup_$TIMESTAMP/
    echo "✓ Backup created: $BACKUP_DIR/full_backup_$TIMESTAMP"
else
    echo "✗ Error: Database directory not found"
    exit 1
fi

# Keep only last 10 backups
ls -t $BACKUP_DIR/full_backup_* -d 2>/dev/null | tail -n +11 | xargs rm -rf 2>/dev/null

echo "✓ Cleanup complete - keeping last 10 backups"
ls -lh $BACKUP_DIR/
EOF
```

### Step 2: Make Script Executable

```bash
chmod +x ~/backup_db.sh
```

### Step 3: Test the Script

```bash
~/backup_db.sh
```

---

## Downloading Backups to Local Machine

To download backups from the VPS to your local computer:

### From Your Local Terminal (Not SSH):

```bash
# Download specific backup
scp -r harmonizer@harminoplet:~/backups/full_backup_20251116_085627 ./local_backups/

# Download all backups
scp -r harmonizer@harminoplet:~/backups ./local_backups/

# Download just the database file
scp harmonizer@harminoplet:~/apps/harmonizer/backend/ourspace_data/ourspace.db ./ourspace_backup.db
```

---

## Troubleshooting

### Permission Denied Errors

If you get "Permission denied" when restoring:

```bash
# Fix ownership
sudo chown -R harmonizer:harmonizer ~/apps/harmonizer/backend/ourspace_data

# Or if that doesn't work
cd ~/apps/harmonizer/backend
sudo rm -rf ourspace_data
cp -r ~/backups/full_backup_*/ourspace_data ./
sudo chown -R harmonizer:harmonizer ourspace_data
```

### Database Connection Issues After Restore

```bash
# Restart the application
cd ~/apps/harmonizer
sudo docker compose down
sudo docker compose up -d

# Check logs for errors
sudo docker compose logs -f harmonizer
```

### Backup Directory Not Found

```bash
# Create backups directory
mkdir -p ~/backups

# Run backup script again
~/backup_db.sh
```

### Application Won't Start After Restore

```bash
# Check database file integrity
sqlite3 ~/apps/harmonizer/backend/ourspace_data/ourspace.db "PRAGMA integrity_check;"

# Should output: ok

# If corrupted, restore from a different backup
```

---

## Automated Daily Backups (Optional)

To schedule automatic daily backups using cron:

### Step 1: Edit Crontab

```bash
crontab -e
```

### Step 2: Add Daily Backup at 3 AM

```
0 3 * * * /home/harmonizer/backup_db.sh >> /home/harmonizer/backup.log 2>&1
```

### Step 3: Save and Exit

Press `Ctrl+X`, then `Y`, then `Enter`.

### Step 4: Verify Cron Job

```bash
crontab -l
```

---

## Important Notes

1. **Backups are local to the VPS** - They live in `~/backups/` on the server
2. **Download important backups** - Store critical backups on your local machine
3. **Test restores regularly** - Make sure your backup process works
4. **Backups don't include code** - Application code is managed by git
5. **Old backups are auto-deleted** - Script keeps only the last 10 backups
6. **Permissions matter** - Always `chown` files after restoring

---

## Emergency Database Reset

If you need to completely reset the database to a fresh state:

```bash
cd ~/apps/harmonizer/backend

# Stop app
sudo docker compose down

# Remove old database
rm -rf ourspace_data

# Let the app recreate it on next start
sudo docker compose up -d

# Check logs to verify database was created
sudo docker compose logs -f harmonizer
```

Default admin password after reset: `vertexlotto`

---

## Summary Cheat Sheet

| Task | Command |
|------|---------|
| Create backup | `~/backup_db.sh` |
| List backups | `ls -lh ~/backups/` |
| Restore latest | `cd ~/apps/harmonizer/backend && rm -rf ourspace_data && cp -r ~/backups/full_backup_*/ourspace_data ./ && chown -R harmonizer:harmonizer ourspace_data` |
| Download backup | `scp -r harmonizer@harminoplet:~/backups/full_backup_* ./local_backups/` |
| Check backup contents | `ls -la ~/backups/full_backup_*/ourspace_data/` |
| Restart app | `cd ~/apps/harmonizer && sudo docker compose restart` |

---

**Last Updated:** November 2024
