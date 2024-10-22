let onQuiz = true

document.getElementById("submit").addEventListener("click", function(){
    onQuiz = false
} )

window.onbeforeunload = function() {
    if (onQuiz) {
        return "Do you really want to leave our brilliant application?";
}};