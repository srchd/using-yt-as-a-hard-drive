// content.js

SCOPES = "https://www.googleapis.com/auth/youtube\n\
https://www.googleapis.com/auth/youtube.channel-memberships.creator\n\
https://www.googleapis.com/auth/youtube.force-ssl\n\
https://www.googleapis.com/auth/youtube.readonly\n\
https://www.googleapis.com/auth/youtube.upload\n\
https://www.googleapis.com/auth/youtubepartner\n\
https://www.googleapis.com/auth/youtubepartner-channel-audit"


chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if (request.action == "create_clicked") {
            create_project();
        }
    }
);

async function create_project() {
    console.log("Button Pressed");
    let found;
    let bttn;
    let email;
    let inputField;
    let textArea;
    let name = "testname";
    let stage = "create";


    console.log("Select a project")
    bttn = getButtonByInnerText("Select a project");
    if(!bttn) bttn = getButtonByInnerText("You're currently working");
    console.log(bttn)
    if(bttn) bttn.click();
    
    console.log("NEW PROJECT");
    bttn = getButtonByInnerText("NEW PROJECT");
    console.log(bttn)
    if(bttn) bttn.click();
    
    await sleep(1000);
    
    // input name
    name = "youtubeharddrive" + Math.floor(Math.random() * 1000000);
    console.log("Input Project Name: " + name);
    inputField = document.querySelector("proj-name-id-input input");
    console.log(inputField)
    if(!inputField) {
        console.log("Input field not found");
        return;
    }
    await simulateTyping(inputField, name);
    
    await sleep(500);
    console.log("CREATE");
    bttn = document.querySelector("button[type='submit']");
    console.log(bttn);
    if(bttn) bttn.click();
    
    // Wait for creating progress to finish. Now only sleep for a longer time.
    await sleep(14000);
    
    // Click on projects and select the one that has been just created. (name stored in the variable 'name')
    console.log("Select a project");
    bttn = getButtonByInnerText("Select a project");
    if(!bttn) bttn = getButtonByInnerText("You're currently working");
    console.log(bttn);
    if(bttn) bttn.click();
    
    await sleep(300);
    bttn = getElementByInnerText("a", name);
    if(bttn) bttn.click();
    
    
    // Go to credentials //
    console.log("APIs and services")
    bttn = null
    while(!bttn){
        bttn = getElementByInnerText("a", "APIs and services");
        await sleep(3000);
        
    }
    console.log(bttn)
    if(bttn) bttn.click();
    await sleep(5000);
    
    // OAuth consent screen ////
    console.log("OAuth consent screen")
    bttn=null
    while(!bttn){
        bttn = document.querySelector("a[aria-label='OAuth consent screen, 4 of 5']");
        console.log("search-consent")
        await sleep(2000)
    }
    console.log(bttn)
    if(bttn) bttn.click();
    
    await sleep(1000);
    bttn = null
    console.log("External")
    while(!bttn){
        bttn = getElementByInnerText("mat-radio-button", "External");
        console.log("search-external")
        await sleep(2000);
    }
    console.log(bttn)
    if(bttn) bttn.click();
    
    await sleep(600);
    console.log("CREATE")
    bttn = getElementByInnerText("button", "CREATE");
    console.log(bttn)
    if(bttn) bttn.click();
    
    // App information //
    console.log("AppName");
    inputField = null
    while(!inputField){
        inputField = document.querySelector("input[required][formcontrolname='displayName']");
        await sleep(2000)
    }
    console.log(inputField);
    if(inputField){
        await simulateTyping(inputField, name);
    }
    console.log("Email");
    bttn = document.querySelector('mat-form-field.mat-mdc-form-field-type-cfc-select > div.mat-mdc-text-field-wrapper');
    console.log(bttn);
    if(bttn) bttn.click();
    bttn = document.querySelector("mat-option[role='option']");
    email = bttn.querySelector("span.mat-option-text").textContent;
    console.log(bttn);
    if(bttn) bttn.click();
    
    console.log("DevEmails");
    inputField = document.querySelector("mat-chip-grid[formcontrolname='emails'] input[required]");
    console.log(inputField);
    if (inputField){
        await simulateTyping(inputField, email + " ");
        inputField.dispatchEvent(new Event('input', { bubbles: true }));
        inputField.dispatchEvent(new Event('change', { bubbles: true }));
        inputField.dispatchEvent(new Event('blur', { bubbles: true }));
    } 

    sleep(1000);
    console.log("SaveAndContinue");
    bttn = getElementByInnerText("button", "SAVE AND CONTINUE");
    console.log(bttn);
    if (bttn) bttn.click();
    sleep(1000);
    
    // Scopes //

    console.log("Add or remove scopes");
    bttn = null
    while(!bttn){
        bttn = getElementByInnerText("button", "ADD OR REMOVE SCOPES");
        await sleep(1000)
    }
    console.log(bttn);
    if (bttn) bttn.click();


    console.log("textarea");
    textArea = null
    while(!textArea){
        textArea = document.querySelector("textarea[matinput][formcontrolname='manuallyAddedScopesControl']");
        await sleep(1000)
    }
    console.log(textArea);
    if(textArea){
        await simulateTyping(textArea, SCOPES);
    }

    await sleep(500)
    console.log("Add to table");
    bttn = getElementByInnerText("button", "ADD TO TABLE");
    console.log(bttn);
    if (bttn) bttn.click();

    await sleep(500)
    console.log("UPDATE");
    bttn = document.querySelector("button[mat-raised-button][cfcformsubmit='apis-oauth-app-scope-picker-form']");
    console.log(bttn);
    if (bttn) bttn.click();

    await sleep(500)
    console.log("SaveAndContinue");
    bttn = getElementByInnerText("button", "SAVE AND CONTINUE");
    console.log(bttn);
    if (bttn) bttn.click();

    // Test Users //


    console.log("Add Users");
    bttn = null
    while(!bttn){
        bttn = getElementByInnerText("button", "ADD USERS");
        await sleep(1000)
    }
    console.log(bttn);
    if (bttn) bttn.click();

    await sleep(500)
    console.log("Emails-textfield");
    textField = document.querySelector("input[aria-label='Text field for emails']");
    console.log(textField);
    if(textField){
        await simulateTyping(textField, email);
        inputField.dispatchEvent(new Event('input', { bubbles: true }));
        inputField.dispatchEvent(new Event('change', { bubbles: true }));
        inputField.dispatchEvent(new Event('blur', { bubbles: true }));
    }

    await sleep(500)
    console.log("add");
    bttn = getElementByInnerText("button", "ADD");
    console.log(bttn);
    if (bttn) bttn.click();

    console.log("SaveAndContinue");
    bttn = getElementByInnerText("button", "SAVE AND CONTINUE");
    console.log(bttn);
    if (bttn) bttn.click();
    sleep(1000)


    //// Credentials ////


    console.log("Credentials");
    bttn = null
    while(!bttn){
        bttn = getElementByInnerText("a", "Credentials");
        await sleep(1000)
    }
    console.log(bttn);
    if(bttn) bttn.click();
    sleep(4000);

    console.log("CREATE CREDENTIALS");
    bttn=null
    while(!bttn){
        bttn = getElementByInnerText("button", "CREATE CREDENTIALS");
        await sleep(1000)
    }
    console.log(bttn);
    if(bttn) bttn.click();

    await sleep(500)
    console.log("OAuth client ID");
    bttn = getElementByInnerText("a", "OAuth client ID");
    console.log(bttn);
    if(bttn) bttn.click();
    sleep(4000);

    // Create OAuth client ID //

    console.log("Application Type");
    bttn = null
    while(!bttn){
        bttn = document.querySelector('mat-form-field.mat-mdc-form-field-type-cfc-select > div.mat-mdc-text-field-wrapper');
        await sleep(1000)
    }
    console.log(bttn);
    if (bttn) {
        bttn.click();
    }

    await sleep(1500)
    console.log("Desktop app");
    bttn = null
    while(!bttn){
        bttn = getElementByInnerText("mat-option", "Desktop app");
        await sleep(1000)
    }
    console.log(bttn);
    if(bttn){
        bttn.click();
    }

    await sleep(500)
    console.log("Enter name");
    inputField = document.querySelector("input[formcontrolname='displayName']");
    console.log(inputField);
    if (inputField){
        await simulateTyping(inputField, name);

    }

    await sleep(500)
    console.log("CREATE");
    bttn = document.querySelector("button[mat-raised-button][color='primary'][type='submit']");
    console.log(bttn);
    if(bttn){
        bttn.click();
    }
    sleep(4000)

    // Download JSON
    console.log("Download JSON");
    bttn=null
    while(!bttn){
        bttn = getElementByInnerText("button", "DOWNLOAD JSON");
        await sleep(1000)
    }
    console.log(bttn);
    if(bttn){
        bttn.click();
    }

}


async function simulateTyping(inputField, textToType) {
    return new Promise(async (resolve) => {
        inputField.focus();
        inputField.value = ""; // clear the input field

        let textToTypeArray = textToType.split('');

        for (let index = 0; index < textToTypeArray.length; index++) {
            const char = textToTypeArray[index];
            inputField.value += char;
            // Dispatch input event after adding each character
            let inputEvent = new Event('input', { bubbles: true });
            inputField.dispatchEvent(inputEvent);

            // Wait for typing speed delay
            await new Promise((r) => setTimeout(r, 10));

            // Dispatch change event and blur after the whole text has been 'typed'
            if (index === textToTypeArray.length - 1) {
                inputField.dispatchEvent(new Event('input', { bubbles: true }));
                inputField.dispatchEvent(new Event('change', { bubbles: true }));
                inputField.dispatchEvent(new Event('blur', { bubbles: true }));

                // blur the input field
                inputField.blur();
            }
        }

        resolve();
    });
}

function searchBttnClick(classValue) {
    let button = document.getElementsByClassName(classValue);
    console.log(button)
    if (button[0]){
        button[0].click();
        return true;
    }
    return false;
}

function getElementByInnerText(element, text) {
    // Get all buttons on the page
    let buttons = document.getElementsByTagName(element);

    // Iterate through all buttons
    for (let i = 0; i < buttons.length; i++) {
        // Check if the button's text includes the desired text
        if (buttons[i].outerHTML.toLowerCase().includes(text.toLowerCase())) {
            // If it does, return the button
            return buttons[i];
        }
    }

    // If no button was found that includes the desired text, return null
    return null;
}

function getButtonByInnerText(text) {
    // Get all buttons on the page
    let buttons = document.getElementsByTagName('button');

    // Iterate through all buttons
    for (let i = 0; i < buttons.length; i++) {
        // Check if the button's text includes the desired text
        if (buttons[i].outerHTML.toLowerCase().includes(text.toLowerCase())) {
            // If it does, return the button
            return buttons[i];
        }
    }

    // If no button was found that includes the desired text, return null
    return null;
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

// for debug
function send_log(_message) {
    chrome.runtime.sendMessage({from: 'content', message: _message});
}