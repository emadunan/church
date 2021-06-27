document.addEventListener('DOMContentLoaded', function () {

    highlightVerse();



})


// JAVASCRIPT FUNCTIONS
function highlightVerse() {

    const urlString = window.location.href;
    const verseId = urlString.substring(urlString.indexOf('=') + 1, urlString.indexOf('#'));

    const verse = document.querySelector(`#verse-${verseId}`);
    verse.style.background = '#e9ff32';
    // const text = verse.innerHTML;
    // verse.innerHTML = `<mark>${text}</mark>`;
}

// HIGHLIGHT FUNCTIONALITY

function highlightSelection() {

    if (window.getSelection().toString() != "") {
        var selection = window.getSelection();
        var range = selection.getRangeAt(0);
        var allWithinRangeParent = range.commonAncestorContainer.getElementsByTagName("*");

        var allSelected = [];
        for (var i = 0, el; el = allWithinRangeParent[i]; i++) {
            // The second parameter says to include the element 
            // even if it's not fully selected
            if (selection.containsNode(el, true)) {
                allSelected.push(el);
            }
        }


        allSelected.forEach(element => {
            element.style.background = '#e9ff32';
        });
    }

}

// EREASE SELECTION

function ereaseAllSelections() {

    if (window.getSelection().toString() != "") {
        var selection = window.getSelection();
        var range = selection.getRangeAt(0);
        var allWithinRangeParent = range.commonAncestorContainer.getElementsByTagName("*");

        var allSelected = [];
        for (var i = 0, el; el = allWithinRangeParent[i]; i++) {
            // The second parameter says to include the element 
            // even if it's not fully selected
            if (selection.containsNode(el, true)) {
                allSelected.push(el);
            }
        }

        allSelected.forEach(element => {
            element.style.background = '#ffffff';
        });
    }

}

