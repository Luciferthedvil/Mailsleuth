chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'openTab' && message.url) {
    chrome.tabs.create({ url: message.url });
  }
});
