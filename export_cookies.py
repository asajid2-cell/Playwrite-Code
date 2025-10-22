#!/usr/bin/env python3
"""
Export YouTube cookies from Chrome to youtube_cookies.txt

IMPORTANT: Close Chrome completely before running this script!
"""

import sys
import http.cookiejar as cookielib
from pathlib import Path

# Check if yt-dlp is installed
try:
    from yt_dlp.cookies import extract_cookies_from_browser
except ImportError:
    print("ERROR: yt-dlp is not installed. Run: pip install yt-dlp")
    sys.exit(1)

def export_cookies():
    """Export cookies from Chrome to youtube_cookies.txt"""
    output_file = Path(__file__).parent / "backend" / "youtube_cookies.txt"

    print("Exporting YouTube cookies from Chrome...")
    print(f"Output file: {output_file}")
    print()
    print("IMPORTANT: Make sure Chrome is COMPLETELY CLOSED!")
    print("Press Enter to continue, or Ctrl+C to cancel...")
    input()

    try:
        # Create a cookie jar
        cookie_jar = cookielib.MozillaCookieJar(str(output_file))

        # Extract cookies from Chrome
        print("Extracting cookies from Chrome...")
        extract_cookies_from_browser(
            "chrome",
            cookie_jar,
            logger=None,
            keyring=None,
        )

        # Save cookies to file
        print(f"Saving cookies to {output_file}...")
        cookie_jar.save(ignore_discard=True, ignore_expires=True)

        print()
        print(f"SUCCESS! Cookies exported to: {output_file}")
        print()
        print("You can now use the app to download YouTube videos!")
        print("The cookies will be used automatically.")

    except Exception as e:
        print(f"\nERROR: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure Chrome is completely closed")
        print("2. Make sure you're logged into YouTube in Chrome")
        print("3. Try restarting your computer if Chrome won't close")
        sys.exit(1)

if __name__ == "__main__":
    export_cookies()
