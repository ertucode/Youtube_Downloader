
const allSites = ["<all_urls>","https://*/*"]

// Search link //
createContext("SingleL","Single Video",["link"],allSites)
    createChild("SL_Video","Video","SingleL")
    createChild("SL_Audio","Audio","SingleL")
    createChild("SL_Subtitle","Subtitle","SingleL")
    createChild("SL_Combinations","Combinations","SingleL")
        createChild("SL_Video_Audio","Video + Audio","SL_Combinations")
        createChild("SL_Audio_Subtitle","Audio + Subtitle","SL_Combinations")
        createChild("SL_Video_Subtitle","Video + Subtitle","SL_Combinations")
        createChild("SL_Video_Audio_Subtitle","All","SL_Combinations")   


createContext("PlaylistL","Playlist",["link"],allSites)
    createChild("PL_Video","Video","PlaylistL")
    createChild("PL_Audio","Audio","PlaylistL")
    createChild("PL_Subtitle","Subtitle","PlaylistL")
    createChild("PL_Combinations","Combinations","PlaylistL")
        createChild("PL_Video_Audio","Video + Audio","PL_Combinations")
        createChild("PL_Audio_Subtitle","Audio + Subtitle","PL_Combinations")
        createChild("PL_Video_Subtitle","Video + Subtitle","PL_Combinations")
        createChild("PL_Video_Audio_Subtitle","All","PL_Combinations")   


// Search selection //
createContext("SingleS","Single Video",["selection"],allSites)
    createChild("SS_Video","Video","SingleS")
    createChild("SS_Audio","Audio","SingleS")
    createChild("SS_Subtitle","Subtitle","SingleS")
    createChild("SS_Combinations","Combinations","SingleS")
        createChild("SS_Video_Audio","Video + Audio","SS_Combinations")
        createChild("SS_Audio_Subtitle","Audio + Subtitle","SS_Combinations")
        createChild("SS_Video_Subtitle","Video + Subtitle","SS_Combinations")
        createChild("SS_Video_Audio_Subtitle","All","SS_Combinations")   
        
createContext("PlaylistS","Playlist",["selection"],allSites)
    createChild("PS_Video","Video","PlaylistS")
    createChild("PS_Audio","Audio","PlaylistS")
    createChild("PS_Subtitle","Subtitle","PlaylistS")
    createChild("PS_Combinations","Combinations","PlaylistS")
        createChild("PS_Video_Audio","Video + Audio","PS_Combinations")
        createChild("PS_Audio_Subtitle","Audio + Subtitle","PS_Combinations")
        createChild("PS_Video_Subtitle","Video + Subtitle","PS_Combinations")
        createChild("PS_Video_Audio_Subtitle","All","PS_Combinations")   



// Search copied //
createContext("DownloadWithCopied","Download With Copied",["all"],allSites)

    createChild("SingleC","Single Video","DownloadWithCopied")
        createChild("SC_Video","Video","SingleC")
        createChild("SC_Audio","Audio","SingleC")
        createChild("SC_Subtitle","Subtitle","SingleC")
        createChild("SC_Combinations","Combinations","SingleC")
            createChild("SC_Video_Audio","Video + Audio","SC_Combinations")
            createChild("SC_Audio_Subtitle","Audio + Subtitle","SC_Combinations")
            createChild("SC_Video_Subtitle","Video + Subtitle","SC_Combinations")
            createChild("SC_Video_Audio_Subtitle","All","SC_Combinations")   

    createChild("PlaylistC","Playlist","DownloadWithCopied")
        createChild("PC_Video","Video","PlaylistC")
        createChild("PC_Audio","Audio","PlaylistC")
        createChild("PC_Subtitle","Subtitle","PlaylistC")
        createChild("PC_Combinations","Combinations","PlaylistC")
            createChild("PC_Video_Audio","Video + Audio","PC_Combinations")
            createChild("PC_Audio_Subtitle","Audio + Subtitle","PC_Combinations")
            createChild("PC_Video_Subtitle","Video + Subtitle","PC_Combinations")
            createChild("PC_Video_Audio_Subtitle","All","PC_Combinations")   


ops = ["Video","Audio","Subtitle","Video_Audio","Audio_Subtitle","Video_Subtitle","Video_Audio_Subtitle"]

chrome.contextMenus.onClicked.addListener(handleClick)

function handleClick(link,tab){
    // Search Selection
    
    if (typeof link.selectionText !== 'undefined'){
        if (startsWith(link.menuItemId,"SS_") || startsWith(link.menuItemId,"PS_")){
            if(validateYouTubeUrl(link.selectionText)){
                ops.forEach((element)=>{
                    if (link.menuItemId.slice(3) == element){
                        if (element.includes("Subtitle")){
                            chrome.tabs.sendMessage(tab.id,"Ask for subtitle" + link.selectionText +","+ link.menuItemId)
                        }  else {
                        openApp(link.selectionText,link.menuItemId)
                        }
                    }
                })

            }
        }
    }
    // Link or Copied or CopyToClipboard

    else {
        chrome.tabs.sendMessage(tab.id, link.menuItemId)
    }


}  


function createChild(id,title,parentId){
    chrome.contextMenus.create({
        "id": id,
        "title": title,
        "parentId": parentId,
        "contexts":["all"]
    })
}

function createContext(id,title,contexts,patterns){
    chrome.contextMenus.create({
        "id": id,
        "title": title,
        "contexts" : contexts,
        "documentUrlPatterns": patterns
    })
}

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

function openApp(text,options){
    window.open(`cavit://${text},${options}`, '_blank')
}