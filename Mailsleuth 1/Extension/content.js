(function () {
  // Step 1: Wait for the opened email container (Gmail loads parts of DOM lazily)
  const waitForEmailAndClickMore = () => {
    const emailContainer = document.querySelector('div[role="main"] .adn'); // typically where email body lives

    if (!emailContainer) {
      console.warn("⏳ Waiting for email to load...");
      setTimeout(waitForEmailAndClickMore, 500);
      return;
    }

    // Step 2: Find the correct 3-dot More button inside the email
    const moreButton = emailContainer.querySelector('div[role="button"][aria-label*="More"]');

    if (!moreButton) {
      alert("⚠️ Could not find the correct 'More' menu. Please ensure an email is open.");
      console.warn("❌ No 'More' button found inside opened email.");
      return;
    }

    console.log("✅ Found 'More' button:", moreButton);
    moreButton.click();

    // Step 3: Wait for the dropdown menu and find the "Show Original" item
    setTimeout(() => {
      const menuItems = Array.from(document.querySelectorAll('div[role="menuitem"]'));
      const showOriginal = menuItems.find(item =>
        item.innerText?.toLowerCase().includes("show original")
      );

      if (!showOriginal) {
        alert("⚠️ Could not find 'Show Original' in the menu.");
        console.warn("Menu items found:", menuItems.map(i => i.innerText));
        return;
      }

      showOriginal.click();

      setTimeout(() => {
        alert("✅ 'Show Original' opened in a new tab. You can now copy the header.");
      }, 1000);
    }, 600); // Gmail dropdown needs some time to render
  };

  waitForEmailAndClickMore();
})();
