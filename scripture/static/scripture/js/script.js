document.addEventListener('DOMContentLoaded', function () {
    console.log('here')
})

function redirectToCurrentLoc() {
    fetch("/getCurrentLocation")
    .then((response) => {
      if (!response.ok) throw new Error("Failed to load user state!");

      return response.json();
    })
    .then((responseData) => {
        console.log(responseData);
        window.location.replace(`/books/${responseData.book}?verse=${responseData.vlocation}#chapter-${responseData.chapter}`);
    });
}