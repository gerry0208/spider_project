from playwright.async_api import async_playwright, expect
import asyncio


async def get_data(page, url):
    await page.goto(url)
    await page.wait_for_load_state('load')


async def run(url, page_num):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(url)
        await page.wait_for_load_state()
        if page == 1:
            pass
        else:
            for _ in range(page_num - 1):
                await page.get_by_text('Next').click()
            await page.wait_for_load_state('load')
            a = page.locator('//h2/a')
            num = await a.count()
            for i in range(num):
                detail_url = 'https://www.amazon.co.uk' + await a.nth(i).get_attribute('href')
                detail_page = await context.new_page()
                await asyncio.create_task(get_data(detail_page, detail_url))

            await asyncio.sleep(10)


loop = asyncio.get_event_loop()
loop.run_until_complete(run('https://www.amazon.co.uk/s?me=A1A8TOSJMUGK5U', 3))
loop.close()
