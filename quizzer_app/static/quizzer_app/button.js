var checkboxCounter = 0
var checkBoxes = document.querySelectorAll("input[type='checkbox']")
var submitButton = document.getElementById("")
var selectAllCheckbox = document.getElementById("selectAll")
for (var i=1; i < checkBoxes.length; i++) {
    checkBoxes[i].addEventListener("click", countCheck)
}

function countCheck(e) {
    if (e.target.checked) {
        checkboxCounter++
    } else {
        checkboxCounter--
    }
    if (checkboxCounter > 0 && checkboxCounter != checkBoxes.length - 1){
        document.getElementById("btn").disabled = false;
        selectAllCheckbox.checked = false
    } else if (checkboxCounter === checkBoxes.length - 1) {
        selectAllCheckbox.checked = true
    } else {
        document.getElementById("btn").disabled = true;
        selectAllCheckbox.checked = false
    }
    console.log(checkboxCounter)
}

selectAllCheckbox.addEventListener('change', function () {
    if (this.checked) {
        for (var i=0; i < checkBoxes.length; i++) {
            checkBoxes[i].checked = true;
            checkboxCounter = checkBoxes.length - 1
            console.log(checkboxCounter)
            document.getElementById("btn").disabled = false;
        }
    } else {
        for (var i=0; i < checkBoxes.length; i++) {
            checkBoxes[i].checked = false;
            checkboxCounter = 0
            console.log(checkboxCounter)
            document.getElementById("btn").disabled = true;
        }
    }
})