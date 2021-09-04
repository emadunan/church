document.addEventListener('DOMContentLoaded', function() {
    const publishCheckBox = document.getElementById('flexCheckpublish_edit');
    const publishCheckBox_isChecked = publishCheckBox.dataset.checkvalue;
    console.log(publishCheckBox);
    console.log(publishCheckBox_isChecked);

    publishCheckBox_isChecked? publishCheckBox.checked = "True" : publishCheckBox.checked = "False";

})