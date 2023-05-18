document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('openGCP').addEventListener('click', openGCP);
    document.getElementById('createProject').addEventListener('click', createProject);
  
    function openGCP() {
        console.log("clicked");
        chrome.tabs.create({ url: 'https://console.cloud.google.com/' });
    }
  
    function createProject() {
        console.log("clicked");
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            chrome.tabs.sendMessage(tabs[0].id, {action: "create_clicked"});
        });
    }
  });
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
if (request.from === 'background') {
    console.log(request.message);
}
});