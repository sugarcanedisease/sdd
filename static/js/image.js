function showPreview(event) {
    // $('.process').css('visibility', 'visible');

    if (event.target.files.length > 0) {
        var src = URL.createObjectURL(event.target.files[0]);
        var preview = document.getElementById("file-ip-1-preview");
        var process = document.getElementById("process");
        var classify = document.getElementById("classify")
        preview.src = src;
        process.style.display = "inline";        
        classify.style.display = "inline";        
    }
}

