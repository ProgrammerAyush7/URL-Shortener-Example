function copy() {
    var copyText = document.getElementById("url");
    copyText.select();
    copyText.setSelectionRange(0, 99999);
    document.execCommand("copy");
    alert("URL Copied to Clipboard!")
}