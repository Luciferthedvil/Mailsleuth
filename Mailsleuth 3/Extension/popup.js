document.addEventListener('DOMContentLoaded', function () {
  const scanBtn = document.getElementById('scanBtn');

  if (!scanBtn) {
    console.error("❌ scanBtn not found in DOM!");
    alert("Button not found. Please check popup.html.");
    return;
  }

  scanBtn.addEventListener('click', function () {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
      const tab = tabs[0];

      // Safety check: avoid running on restricted/internal browser pages
      if (
        !tab ||
        !tab.url ||
        tab.url.startsWith('chrome://') ||
        tab.url.startsWith('chrome-extension://') ||
        tab.url.startsWith('edge://') ||
        tab.url.startsWith('about:')
      ) {
        alert('❌ MailSleuth cannot run on this page. Please open Gmail or a supported email client.');
        //console.warn('Blocked attempt on unsupported URL:', tab?.url);
        return;
      }

      // Inject the content script
      chrome.scripting.executeScript(
        {
          target: { tabId: tab.id },
          files: ['content.js']
        },
        () => {
          if (chrome.runtime.lastError) {
            console.error('⚠️ Script injection failed:', chrome.runtime.lastError.message);
            alert('⚠️ Failed to inject script. Make sure you are on a Gmail page.');
          } else {
            console.log('✅ Script injected successfully.');
          }
        }
      );
    });
  });
});
