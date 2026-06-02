from itertools import count

from playwright.sync_api import sync_playwright
import os
from datetime import datetime

def screenshot_specific_element_playwright(
    url, selector, output_file=None, folder_name='screenshots',
    wait_time=15, tab=None, wait_for=None
):
    if output_file is None:
        os.makedirs(folder_name, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(folder_name, f"dashboard_{timestamp}.png")
    else:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()
        page.goto(url)
        for frame in page.frames:
            print(frame.url)
        # apply_date_filter_last_month(page)
        
        page.wait_for_timeout(wait_time * 1000)

        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(5000)

        page.screenshot(
            path="debug_full_page.png",
            full_page=True
        )

        # Klik tab jika diminta
        if tab:
            try:
                print(f"👉 Klik tab: {tab}")
                page.click(tab, timeout=10000)
                page.wait_for_timeout(3000)
            except Exception as e:
                print(f"⚠️ Tidak bisa klik tab {tab}: {e}")

        # Tunggu elemen tertentu jika diminta
        if wait_for:
            try:
                print(f"⏳ Menunggu munculnya: {wait_for}")
                page.wait_for_selector(wait_for, timeout=10000)
            except Exception as e:
                print(f"⚠️ Teks '{wait_for}' tidak muncul: {e}")

        # Screenshot elemen utama
        try:
            count = page.locator(selector).count()
            print(f"Found {count} elements")

            element = None
            if count and count > 0:
                element = page.locator(selector).first
            else:
                # Fallback: search inside frames
                for frame in page.frames:
                    try:
                        fcount = frame.locator(selector).count()
                        if fcount and fcount > 0:
                            print(f"Found {fcount} elements in frame: {frame.url}")
                            element = frame.locator(selector).first
                            break
                    except Exception:
                        continue

            if not element:
                raise Exception("Selector not found on page or in any frame")

            element.wait_for(state="visible", timeout=10000)

            # If element is on main page, ensure not blurred via global function
            try:
                if page.locator(selector).count() and page.locator(selector).count() > 0:
                    page.wait_for_function(
                        """(selector) => {
                            const el = document.querySelector(selector);
                            if (!el) return false;
                            const style = window.getComputedStyle(el);
                            return style.opacity === '1' && style.filter === 'none';
                        }""",
                        arg=selector,
                        timeout=10000,
                    )
            except Exception:
                # ignore, continue to screenshot the element
                pass

            page.wait_for_timeout(2000)
            element.screenshot(path=output_file)
            print(f"✅ Screenshot elemen berhasil disimpan: {output_file}")

        except Exception as e:
            page.screenshot(
                path=f"error_{datetime.now().strftime('%H%M%S')}.png",
                full_page=True
            )

            print(f"❌ Gagal screenshot elemen: {e}")

