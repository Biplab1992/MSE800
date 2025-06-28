
function changeImage() {
    const imgElement = document.getElementById('loadedImage');
    if (imgElement.src.includes("example.jpg")) {
        imgElement.src = "/static/images/another_example.jpg";
    } else {
        imgElement.src = "/static/images/example.jpg";
    }
}
