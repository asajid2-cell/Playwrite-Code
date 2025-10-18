import subprocess, time, sys
from pathlib import Path

repo = Path(r"z:\328\CMPUT328-A2\codexworks\301\harmonizer")
server = subprocess.Popen([sys.executable, "app.py"], cwd=repo)
print("Started server PID", server.pid)
try:
    time.sleep(5)
    import asyncio
    from playwright.async_api import async_playwright

    async def main():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto('http://127.0.0.1:5000/?trid=TESTTRACK&mode=canon', wait_until='networkidle')
            await page.wait_for_timeout(1000)
            await page.click('#advanced-toggle')
            await page.wait_for_timeout(500)
            sliders = await page.query_selector_all('input[type="range"]')
            print('Sliders found:', len(sliders))
            for idx, slider in enumerate(sliders):
                disabled = await slider.is_disabled()
                bbox = await slider.bounding_box()
                print(f'Slider {idx} disabled? {disabled} bbox={bbox}')
                if not disabled and bbox:
                    await slider.hover()
                    await page.mouse.down()
                    await page.mouse.move(bbox['x'] + bbox['width'] - 5, bbox['y'] + bbox['height']/2, steps=5)
                    await page.mouse.up()
                    val = await slider.get_attribute('value')
                    print(f' after drag value={val}')
            await browser.close()
    asyncio.run(main())
finally:
    server.terminate()
    try:
        server.wait(timeout=5)
    except subprocess.TimeoutExpired:
        server.kill()
