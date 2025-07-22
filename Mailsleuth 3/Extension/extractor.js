(async function () {
  const preTag = document.querySelector('pre');

  if (!preTag || !preTag.innerText.trim()) {
    console.warn("❌ <pre> tag missing or empty.");
    alert("⚠️ Could not extract headers from the 'Show Original' page.");
    return;
  }

  const headers = preTag.innerText.trim();

  console.log("✅ Extracted headers:", headers.slice(0, 500)); // show preview
  
  try {
    const response = await fetch("http://localhost:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headers }),
    });

    const result = await response.json();
    console.log("✅ Server response:", result);
    alert("✅ Headers sent! Verdict: " + result.verdict);
  } catch (err) {
    console.error("❌ Failed to send headers:", err);
    alert("❌ Failed to send headers to Flask.");
  }
})();
