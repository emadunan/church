document.addEventListener("DOMContentLoaded", function () {
//   const criteriaEl = document.getElementById("id_search-criteria");
//   if (criteriaEl) {
//     const mainStr = criteriaEl.textContent;
//     const strArr = mainStr.split(" ");
//     console.log(strArr);
//     strArr.forEach(element => {
//         highlight(element);
//         console.log(element);
//     });
//   }
});

// لا تعمل بسبب التشكيل
function highlight(text) {
  var inputTexts = document.querySelectorAll(".cc_verse-textf");
  inputTexts.forEach(inputText => {
    console.log(inputText);
    var innerHTML = inputText.innerHTML;
    var index = innerHTML.indexOf(text);
    if (index >= 0) {
      innerHTML =
        innerHTML.substring(0, index) +
        "<span class='highlight'>" +
        innerHTML.substring(index, index + text.length) +
        "</span>" +
        innerHTML.substring(index + text.length);
      inputText.innerHTML = innerHTML;
    }
  });
}
