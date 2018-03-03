function summarize(surl, n) {
    console.log(surl)
    console.log(n)
    var url = "http://localhost:5000/abridge"
    /*var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET",url,false);
    xmlHttp.send(null);*/
    //document.getElementById("op").innerHTML = xmlHttp.responseText;
    var params = surl + '~' + n;
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("POST", url, false);
    xmlHttp.send(params);
    return xmlHttp.responseText;
}
document.addEventListener('DOMContentLoaded', function() {

    var link = document.getElementById('pop');
    link.addEventListener('click', function() {
        var lines = parseInt(document.getElementById('lines').value);
        if (lines < 0) {
            alert('Please enter positive number lines to summarize')
        } else {
            chrome.tabs.query({
                    'active': true,
                    'windowId': chrome.windows.WINDOW_ID_CURRENT
                },
                function(tabs) {
                    var url = tabs[0].url;
                    var html = summarize(url, lines);
                    var width;
                    if (lines < 5) {
                        width = 5;
                    } else {
                        width = lines;
                    }
                    //var strWindowFeatures = "menubar=yes,location=yes,resizable=yes,scrollbars=yes,status=yes,width=500,height=500";
                    var windowObjectReference = window.open("", "_blank", "width=" + (width + 5) * 100 + ",height=" + width * 100 + ",top=100,left=300,location=1,status=1,scrollbars=1,resizable=1");
                    //var windowObjectReference = window.open("","_blank", strWindowFeatures); 
                    windowObjectReference.document.open()
                    windowObjectReference.document.write(html)
                    windowObjectReference.document.close()
                });
        }
    });
});