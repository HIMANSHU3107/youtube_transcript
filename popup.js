const summaryForm = document.getElementById("summary-form");
//const videoURL = document.getElementById("url");
summaryForm.onsubmit = function(){
    console.log(url)
}

summaryForm.onsubmit = function(e){
    e.preventDefault();
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        chrome.tabs.sendMessage(tabs[0].id, {action: "SUMMARY"});
				window.close();
    });
}