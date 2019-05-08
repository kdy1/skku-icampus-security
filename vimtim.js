const puppeteer = require("puppeteer");

(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: ["--proxy-server=127.0.0.1:9999"]
  });
  const page = await browser.newPage();
  await page.goto("http://icampus.ac.kr");
  await page.screenshot({ path: "example.png" });
})();
