chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (
    changeInfo.status === "complete" &&
    tab.url.includes("view=om") // This is true for Gmail's "Show Original" page
  ) {
    chrome.scripting.executeScript({
      target: { tabId },
      files: ["extractor.js"]
    });
  }
});
