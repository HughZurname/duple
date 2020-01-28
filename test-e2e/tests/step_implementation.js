/* globals gauge*/
"use strict";
const {
  openBrowser,
  write,
  closeBrowser,
  goto,
  press,
  screenshot,
  text,
  focus,
  textBox,
  toRightOf,
  button,
  click
} = require("taiko");
const assert = require("assert");
const headless = process.env.headless_chrome.toLowerCase() === "true";

beforeSuite(async () => {
  await openBrowser({ headless: headless });
});

afterSuite(async () => {
  await closeBrowser();
});

gauge.screenshotFn = async function() {
  return await screenshot({ encoding: "base64" });
};

step("Go to <page>", async page => {
  await goto(page);
});

step("Click the <button> button", async button => {
  await click(button(button));
});

step("Select a pre-trained model and start", async page => {
  await click("Use a pre-trained model");
  await click("Start");
});

step("Upload the <file> data file", async file => {
  await attach(file, to(fileField('[data-testid="file-upload"]')));
});
