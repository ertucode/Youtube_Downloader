//content script  "name": "▷ Youtube Downloader",
var desiredText = null;
var url = null;

// desiredText'i tanımla
document.addEventListener("contextmenu", function(event){
    target = event.target
    url = target.href
    trying = 0
    while (typeof url === "undefined"){
        trying += 1
        try {
        target = target.parentElement
        url = target.href
        }
        catch (err){
            
        } 
        if (trying > 50){
            break
        }
    }
}, true);

ops = ["Video","Audio","Subtitle","Video_Audio","Audio_Subtitle","Video_Subtitle","Video_Audio_Subtitle"]

chrome.runtime.onMessage.addListener(function(request,a,s) {

    // Link
    if (startsWith(request,"SL_") || startsWith(request,"PL_")){
        if(validateYouTubeUrl(url)){
            ops.forEach((element)=>{
                if (request.slice(3) == element){
                    if (element.includes("Subtitle")){
                        sub = prompt("Which language for the subtitle [en for English, tr for Turkish","en")
                        openApp(url,request + "_" + sub)
                    } else {
                        openApp(url,request)
                    }
                }
            })
        }
    }
    if (startsWith(request,"SC_") || startsWith(request,"PC_")){
        
            ops.forEach((element)=>{
                if (request.slice(3) == element){
                    navigator.clipboard.readText()
                    .then(text => {
                        console.log("text: " + text)
                        if(validateYouTubeUrl(text)){
                            if (element.includes("Subtitle")){
                                sub = prompt("Which language for the subtitle [en for English, tr for Turkish","en")
                                openApp(text,request + "_" + sub)
                            } else {
                                openApp(text,request)
                            }
                        } else {
                            alert("Invalid URL : " + text)
                        }}
                        )
                    .catch(err => {
                        
                    });  
                }
            })
        
    }

    if (startsWith(request,"Ask for subtitle")){
        sub = prompt("Which language for the subtitle [en for English, tr for Turkish","en")
        splits = request.slice(16).split(",")
        openApp(splits[0],splits[1] + "_" + sub)
    }


    
});

function validateYouTubeUrl(url) { 
    if (url != undefined || url != '') {        
        var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=|\?v=)([^#\&\?]*).*/;
        var match = url.match(regExp);
        if (match && match[2].length == 11) {
            // Do anything for being valid
            // if need to change the url to embed url then use below line            
            return true
        } else if (url.includes("youtube.com/playlist")){
        		return true
        }
        else {
            return false
        }
    }
}

function startsWith(text,other){
    return  text.slice(0,other.length) === other
}

function openApp(url,options){
    window.open(`cavit://${url},${options}`, '_blank')
}