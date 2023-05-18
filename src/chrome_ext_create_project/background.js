// background.js
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.from === 'content') {
      chrome.runtime.sendMessage({from: 'background', message: request.message});
    }
  });