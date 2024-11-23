// background.js

// Open the form on extension installation
browser.runtime.onInstalled.addListener(() => {
  browser.tabs.create({ url: "popup.html" });
});

// List of suspected phishing sites
const suspectedPhishingSites = ["example-phish.com", "phishy-site.net"];

// Monitor web requests for phishing attempts
browser.webRequest.onBeforeRequest.addListener(
  (details) => {
    const url = new URL(details.url);

    if (suspectedPhishingSites.includes(url.hostname)) {
      browser.notifications.create({
        type: "basic",
        iconUrl: "assets/warning.png",
        title: "Phishing Alert",
        message: `The site ${url.hostname} is suspected of phishing. Access has been blocked.`,
      });

      return { cancel: true }; // Block the request
    }
  },
  { urls: ["<all_urls>"] }, // Apply to all URLs
  ["blocking"] // Enable blocking behavior
);

// Track suspicious login behavior (e.g., repeated login failures)
let loginAttempts = {};

// Listen for messages about login attempts
browser.runtime.onMessage.addListener((message) => {
  if (message.type === "loginAttempt") {
    const { username } = message;

    // Increment the count for the username
    loginAttempts[username] = (loginAttempts[username] || 0) + 1;

    if (loginAttempts[username] > 3) {
      // Notify the user if suspicious activity is detected
      browser.notifications.create({
        type: "basic",
        iconUrl: "assets/warning.png",
        title: "Suspicious Login Behavior",
        message: `Multiple failed login attempts detected for ${username}. Please verify your account security.`,
      });
    }
  }
});

// Optional: Reset login attempts periodically (e.g., every hour)
setInterval(() => {
  loginAttempts = {}; // Reset the tracking object
}, 3600000); // 1 hour

