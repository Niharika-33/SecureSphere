// background.js

const apiUrl = "https://f3388d55-591e-442b-a337-04fd2a053ea1-00-3ppgx536jamqg.pike.replit.dev/predict";

browser.runtime.onInstalled.addListener(() => {
  browser.tabs.create({ url: "popup.html" });
});
const staticData = {
  Time_Taken: 5.2,
  Failed_Attempts: 7,
  IP_Change: 8,
  Typing_Speed: 80,
  Device_Type: 0,
  Browser_Type: 1,
  Login_Hour: 14,
  Weekend_Login: 7,
};

// Monitor interactions on the Salesforce login page
let failedAttempts = 0;

// Listen for active tab updates
browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url.includes("salesforce.com")) {
    browser.scripting.executeScript({
      target: { tabId: tabId },
      func: monitorSalesforceLogin,
    });
  }
});

function monitorSalesforceLogin() {
  // Identify password input field on the Salesforce page
  const passwordField = document.querySelector("#password");
  const loginButton = document.querySelector("#Login");

  if (passwordField && loginButton) {
    passwordField.addEventListener("input", () => {
      // Track failed login attempts
      loginButton.addEventListener("click", () => {
        if (passwordField.value === "") {
          failedAttempts++;
        }
        if (failedAttempts === 2) {
          // Send message to background script to trigger anomaly detection
          browser.runtime.sendMessage({ action: "triggerAnomalyCheck" });
        }
      });
    });
  }
}

// Listen for messages from content scripts
browser.runtime.onMessage.addListener((message) => {
  if (message.action === "triggerAnomalyCheck") {
    triggerAnomalyCheck();
  }
});

// Trigger the ML model API
async function triggerAnomalyCheck() {
  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(staticData),
    });

    const result = await response.json();

    if (result.prediction === "Anomaly") {
      console.log("Anomaly detected! Prompting security question.");
      browser.action.openPopup();
    } else {
      console.log("Normal behavior detected.");
    }
  } catch (error) {
    console.error("Error connecting to the ML model API:", error);
  }
}

