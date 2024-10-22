var checkboxCounter = 0
var checkBoxes = document.querySelectorAll("input[type='checkbox']")
var submitButton = document.getElementById("")
for (var i=0; i < checkBoxes.length; i++) {
    checkBoxes[i].addEventListener("click", countCheck)
}

function countCheck(e) {
    if (e.target.checked) {
        checkboxCounter++
    } else {
        checkboxCounter--
    }
    if (checkboxCounter > 0){
        document.getElementById("btn").disabled = false;
    } else {
        document.getElementById("btn").disabled = true;
    }
}
