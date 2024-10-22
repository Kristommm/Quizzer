let hour = 3;
let minute = 30;
let second = 0;

function count() {
  if (second < 0 && minute == 0){
    second = 59;
    minute = 59;
    hour--;
  }
  else if (second < 0) {
    second = 59;
    minute --;
  }
  if (second < 10){
    second = "0" + second
  }
  if (minute < 10 && second == 0) {
    minute = "0" + minute
  }
  if (hour < 0){
    document.getElementById('submit').click();
  }
  document.getElementById('timer').innerHTML = hour + ":" + minute + ":" + second;
  second--;
}

setInterval(count, 1000);
