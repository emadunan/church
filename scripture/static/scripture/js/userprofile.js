document.addEventListener('DOMContentLoaded', function () {

    // Fill the gender, birthdate fields
    fillGenderRadios();
    fillBirthdateField();
});

// Fill Birthdate Field Fn
function fillBirthdateField() {
    const bdInput = document.querySelector('#id_birthdate');
    const inputDate = bdInput.dataset.birthdate;
    bdInput.value = formatDate(inputDate);
}

// Fill Gender Fields Fn
function fillGenderRadios() {
    const genderDiv = document.querySelector('#id_regform__last > div');
    const gender = genderDiv.dataset.gender;

    if (gender === 'male') {
        document.querySelector('#id_male-radioBox').checked = true;
        document.querySelector('#id_female-radioBox').checked = false;
    } else {
        document.querySelector('#id_male-radioBox').checked = false;
        document.querySelector('#id_female-radioBox').checked = true;
    }
}


function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}
