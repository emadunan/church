document.addEventListener('DOMContentLoaded', function () {

    function search(e) {
        console.log('hi')
        let searched = document.getElementById("id_search-books__heading").dataset.criteria.trim();
        console.log(searched)
        if (searched !== "") {
            let text = document.querySelector("#id_search-results__preview ul li").innerText;
            text = text.replace(/([^ء-ي]searched[^ء-ي])/g, '<span style="color:red">searched</span>');
            document.querySelector("#id_search-results__preview ul li").innerHTML = text;
        }
    }
})