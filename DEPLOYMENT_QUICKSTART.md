# Server Deployment - Quick Start

## TL;DR - 3 Steps to Deploy

### 1. Export Cookies (On Your Local Machine)

```bash
# Close Chrome
python export_cookies.py
# This creates: backend/youtube_cookies.txt
```

### 2. Deploy Cookie File

**Option A: Add to Git (Private Repos Only)**
```bash
git add backend/youtube_cookies.txt
git commit -m "Add YouTube auth"
git push
```

**Option B: Platform-Specific Secret (Recommended)**

**Render:**
1. Dashboard → Your Service → Secret Files
2. Add: `filename: youtube_cookies.txt`, `contents: <paste file content>`

**Heroku:**
```bash
heroku config:set YOUTUBE_COOKIES_BASE64="$(base64 < backend/youtube_cookies.txt)"
```

**Docker:**
```dockerfile
COPY backend/youtube_cookies.txt /app/youtube_cookies.txt
```

### 3. Deploy Your App

```bash
git push # or your deployment command
```

## That's It!

The code **already supports** reading cookies from:
- ✅ `backend/youtube_cookies.txt`
- ✅ `YOUTUBE_COOKIES_PATH` environment variable
- ✅ `/app/youtube_cookies.txt` (containers)

## When Cookies Expire (2-3 Months)

Just re-run step 1 and 2:
```bash
python export_cookies.py
# Re-deploy with new cookies
```

## Testing

Check your server logs for:
```
[YouTube Download] Using cookies from: /app/youtube_cookies.txt
[YouTube Download] Using cookie file for authentication
```

If you see these → ✅ Working!

## Alternative: User Authentication

See [OAUTH_IMPLEMENTATION.md](OAUTH_IMPLEMENTATION.md) for letting users sign in with Google.

**Only needed if:**
- High traffic site
- Want per-user rate limiting
- Don't want to manage cookies

For most cases, the cookie file approach (above) is perfect!

## Security Notes

- 🔒 Keep repository **private** if cookies are in git
- 🔄 Rotate cookies monthly
- 🚫 Never commit cookies to public repos
- ✅ Use environment variables for production

## Full Guides

- **[SERVER_DEPLOYMENT.md](SERVER_DEPLOYMENT.md)** - Complete deployment guide
- **[OAUTH_IMPLEMENTATION.md](OAUTH_IMPLEMENTATION.md)** - OAuth alternative
- **[YOUTUBE_SETUP.md](YOUTUBE_SETUP.md)** - Local development setup
