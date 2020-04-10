const puppeteer = require('puppeteer-core');

(async () => {
	const browser = await puppeteer.launch({defaultViewport: {height: 1080, width: 1920}, headless: true, args: ['--display=:1', '--no-sandbox', '--disable-extensions'], executablePath: '/usr/bin/chromium-browser'});
	const page = await browser.newPage();
	await page.goto('http://www.google.com', { waitUntil: 'networkidle0'});
	const title = await page.title();
	console.log(title);
	await page.screenshot({ path: 'toucom.png', fullpage: true});
	await browser.close();
})();
