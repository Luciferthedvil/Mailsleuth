(async function () {
  const preTag = document.querySelector('pre');

  if (!preTag) {
    console.warn("❌ Could not find <pre> tag with headers.");
    alert("⚠️ Could not extract headers.");
    return;
  }

  const headers = preTag.innerText;

  console.log("✅ Extracted headers:", headers.slice(0, 300) + "...");

  try {
    const response = await fetch("http://localhost:5000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ headers }),
    });

    const result = await response.json();
    alert("✅ Headers sent! Result:\n" + JSON.stringify(result, null, 2));
  } catch (err) {
    console.error("❌ Failed to send headers:", err);
    alert("❌ Failed to send headers to Flask.");
  }
})();
