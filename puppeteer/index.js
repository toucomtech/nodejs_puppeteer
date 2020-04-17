/**
 * @name get title
 *
 * @desc Get the title of a page and print it to the console.
 *
 * @see {@link https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md#pagetitle}
 */
const puppeteer = require('puppeteer-core');

(async () => {
  const browser = await puppeteer.launch({defaultViewport: {height: 1080, width: 1920}, headless: true, args: ['--display=:1', '--no-sandbox', '--disable-extensions'], executablePath: '/usr/bin/chromium-browser'});
  const page = await browser.newPage()
  await page.goto('http://www.toucomtech.com/')
  const title = await page.title()
  console.log(title)
  await browser.close()
})()
