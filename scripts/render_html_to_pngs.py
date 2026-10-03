"""Render every element matching --selector in an HTML file as a PNG via Playwright.

Generic - knows nothing about threads, briefs, posts or content types. Takes an
HTML file and a CSS selector, spits out one PNG per element into the given
directory. Used by skills that produce custom layouts via the design system
(instead of fixed templates).
"""
from __future__ import annotations

import argparse
import asyncio
from pathlib import Path

from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parent.parent


def make_name(seq: int, total: int) -> str:
    """Sequential, zero-padded to the width of `total`, so the files sort in slide order.

    Carousel order is the product: 01.png, 02.png, ... 11.png. The previous
    timestamp scheme sorted by accident and broke whenever the millisecond
    counter wrapped mid-render.
    """
    return f"{seq:0{len(str(total))}d}"


async def render(
    html_path: Path,
    out_dir: Path,
    selector: str,
    width: int,
    height: int,
    device_scale_factor: int,
) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": width + 80, "height": height + 80},
            device_scale_factor=device_scale_factor,
        )
        page = await context.new_page()
        await page.goto(html_path.resolve().as_uri(), wait_until="domcontentloaded")
        await page.evaluate("document.fonts.ready")

        count = await page.locator(selector).count()
        if count == 0:
            raise SystemExit(f"No element '{selector}' found in {html_path}")

        for i in range(count):
            el = page.locator(selector).nth(i)
            out_path = out_dir / f"{make_name(i + 1, count)}.png"
            await el.screenshot(path=str(out_path))
            try:
                display_path = out_path.relative_to(ROOT)
            except ValueError:
                display_path = out_path
            print(f"[{i + 1}/{count}] {display_path}")

        await browser.close()
    return count


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--html", required=True, help="Path to the HTML file to render")
    ap.add_argument("--out", required=True, help="Output directory for the PNGs")
    ap.add_argument("--selector", default=".slide", help="CSS selector (default '.slide')")
    ap.add_argument("--width", type=int, default=1080, help="Slide width in CSS px")
    ap.add_argument("--height", type=int, default=1350, help="Slide height in CSS px")
    ap.add_argument("--scale", type=int, default=3, help="device_scale_factor (default 3)")
    args = ap.parse_args()

    html_path = Path(args.html).resolve()
    out_dir = Path(args.out).resolve()

    if not html_path.is_file():
        raise SystemExit(f"HTML does not exist: {html_path}")

    try:
        rel_html = html_path.relative_to(ROOT)
        rel_out = out_dir.relative_to(ROOT)
    except ValueError:
        rel_html, rel_out = html_path, out_dir

    print(f"Reading: {rel_html}")
    print(f"Saving to: {rel_out}/")
    n = asyncio.run(
        render(html_path, out_dir, args.selector, args.width, args.height, args.scale)
    )
    print(f"OK - {n} slide(s) rendered.")


if __name__ == "__main__":
    main()
