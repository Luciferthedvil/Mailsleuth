(async function () {
  const emailContainer = document.querySelector('div.adn');

  if (!emailContainer) {
    alert("⚠️ Please open an email first.");
    return;
  }

  // Try to find the correct "More" button inside the open message (not inbox)
  const allThreeDotButtons = Array.from(document.querySelectorAll('div[role="button"][aria-label*="More"]'));

  const visibleButtons = allThreeDotButtons.filter(btn => {
    const rect = btn.getBoundingClientRect();
    return rect.width > 0 && rect.height > 0;
  });

  if (visibleButtons.length === 0) {
    alert("⚠️ Could not find the correct 'More' menu. Please ensure an email is open.");
    console.warn("Found buttons:", allThreeDotButtons.map(b => b.getAttribute("aria-label")));
    return;
  }

  const moreButton = visibleButtons[0];
  moreButton.click();

  function tryClickShowOriginal(retries = 5) {
    if (retries === 0) {
      alert("⚠️ Could not find 'Show Original' in the menu.");
      const found = Array.from(document.querySelectorAll('div[role="menuitem"]'))
        .map(i => i.innerText.trim())
        .filter(Boolean);
      console.warn("❌ Menu items found:", found);
      return;
    }

    setTimeout(() => {
      const menuItems = Array.from(document.querySelectorAll('div[role="menuitem"]'));
      const showOriginal = menuItems.find(item =>
        item.innerText.toLowerCase().includes("show original")
      );

      if (showOriginal) {
        showOriginal.click();
        console.log("✅ 'Show Original' opened in a new tab. Extracting headers...");
      } else {
        tryClickShowOriginal(retries - 1);
      }
    }, 500);
  }

  tryClickShowOriginal();
})();
