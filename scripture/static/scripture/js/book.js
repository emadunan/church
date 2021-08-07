document.addEventListener("DOMContentLoaded", function () {
  highlightVerse();

  fetch("/getUserState")
    .then((response) => {
      if (!response.ok) throw new Error("Failed to load user state!");

      return response.json();
    })
    .then((responseData) => {
      // console.log(responseData);
      const flagVerse = document.querySelector(
        `#verse-${responseData.location}`
      );

      if (flagVerse) {
        showFlag(flagVerse);
      }
    });

  fetch("/getFavVersesIdForUser")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Can't return your fav verses");
      }
      return response.json();
    })
    .then((responseData) => {
      HighlightUserStatus(responseData);
    });
});

//getFavVersesForUser

function HighlightUserStatus(responseData) {
  console.log(responseData);

  responseData.items.forEach((id) => {
    favVerse = document.getElementById(`verse-${id}`);

    if (favVerse) {
      favVerse.style.backgroundColor = "#e9ff32";
    }

  });
}

// JAVASCRIPT FUNCTIONS

function addtoFavoriteSelection() {
  if (window.getSelection().toString() != "") {
    var selection = window.getSelection();
    var range = selection.getRangeAt(0);

    var allSelected = [];

    if (!range.commonAncestorContainer.innerHTML) {
      var allWithinRangeParent = [range.commonAncestorContainer.parentElement];
      console.log(allWithinRangeParent);
    } else {
      var allWithinRangeParent =
        range.commonAncestorContainer.getElementsByTagName("*");
    }

    for (var i = 0, el; (el = allWithinRangeParent[i]); i++) {
      // The second parameter says to include the element
      // even if it's not fully selected
      if (selection.containsNode(el, true) && el.className === "cc_verse-txt") {
        elId = el.id.substr(6);
        allSelected.push(elId);
      }
    }

    fetch("/addVerseToFavorites", {
      method: "POST",
      headers: {
        "Content-Type": "multipart/form-data",
      },
      body: JSON.stringify({ items: allSelected }),
    })
      .then((response) => {
        if (!response.ok) throw new Error("Failed to add your Favorites!");
        return response.json();
      })
      .then((responseData) => {
        console.log(responseData);

        responseData.items.forEach((id) => {
          document.getElementById(`verse-${id}`).style.backgroundColor =
            "#e9ff32";
        });
      });
  }
}

// HIGHLIGHT SEARCH RESULT
function highlightVerse() {
  const urlString = window.location.href;
  const verseId = urlString.substring(
    urlString.indexOf("=") + 1,
    urlString.indexOf("#")
  );

  const verse = document.querySelector(`#verse-${verseId}`);
  if (verse) {
    verse.style.background = "#e9ff32";
  }
}

// HIGHLIGHT FUNCTIONALITY
function highlightSelection() {
  if (window.getSelection().toString() != "") {
    var selection = window.getSelection();
    var range = selection.getRangeAt(0);

    var allSelected = [];

    if (!range.commonAncestorContainer.innerHTML) {
      var allWithinRangeParent = [range.commonAncestorContainer.parentElement];
      console.log(allWithinRangeParent);
    } else {
      var allWithinRangeParent =
        range.commonAncestorContainer.getElementsByTagName("*");
    }

    for (var i = 0, el; (el = allWithinRangeParent[i]); i++) {
      // The second parameter says to include the element
      // even if it's not fully selected
      if (selection.containsNode(el, true)) {
        allSelected.push(el);
      }
    }

    allSelected.forEach((element) => {
      element.style.background = "#e9ff32";
    });
  }
}

// EREASE SELECTION
function ereaseAllSelections() {
  if (window.getSelection().toString() != "") {
    var selection = window.getSelection();
    var range = selection.getRangeAt(0);

    var allSelected = [];
    if (!range.commonAncestorContainer.innerHTML) {
      var allWithinRangeParent = [range.commonAncestorContainer.parentElement];
      console.log(allWithinRangeParent);
    } else {
      var allWithinRangeParent =
        range.commonAncestorContainer.getElementsByTagName("*");
    }

    for (var i = 0, el; (el = allWithinRangeParent[i]); i++) {
      // The second parameter says to include the element
      // even if it's not fully selected
      if (selection.containsNode(el, true)) {
        allSelected.push(el);
      }
    }

    allSelected.forEach((element) => {
      element.style.background = "#ffffff";
    });
  }
}

function setAsLastLocation() {
  if (window.getSelection().toString() != "") {
    var selection = window.getSelection();
    let selectedLocation = selection.getRangeAt(0).startContainer;

    if (selectedLocation.length < 4) {
      selectedLocation = selectedLocation.parentElement.parentElement;
    } else {
      selectedLocation = selectedLocation.parentElement;
    }

    if (!selectedLocation.classList.contains("cc_verse-txt")) {
      return;
    }

    verseId = selectedLocation.id.substring(
      selectedLocation.id.indexOf("-") + 1
    );
    console.log(verseId);

    fetch("/setLocation", {
      method: "PUT",
      headers: {
        "Content-Type": "text/plain",
      },
      body: verseId,
    }).then((vid) => {
      // Clear up
      const oldFlagVerse = document.querySelector(".flagged");
      if (oldFlagVerse) {
        oldFlagVerse.style.borderBottom = "";
        oldFlagVerse.classList.remove("flagged");
      }

      const oldFlag = document.querySelector("#id_location-flag");
      if (oldFlag) oldFlag.remove();

      showFlag(selectedLocation);
    });
  }
}

function showFlag(verseEl) {
  locationFlag = document.createElement("img");
  locationFlag.id = "id_location-flag";
  locationFlag.src = "/static/scripture/img/achievement.png";
  locationFlag.style.width = "2rem";

  // Add flaged Class
  verseEl.classList.add("flagged");

  //
  verseEl.parentElement.insertBefore(locationFlag, verseEl);
  verseEl.style.borderBottom = "1px solid #000";
}
