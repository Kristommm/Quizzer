
function getRandomColor() {
    var letters = '0123456789ABCDEF';
    var color = '#';
    for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

const data = JSON.parse(document.getElementById('user_stats').textContent);
const subjects = Object.keys(data)
const colors = []

for (i=0; i<subjects.length; i++) {
    var color = getRandomColor()
    colors.push(color)
}



for (i=1; i < subjects.length + 1; i++) {
    var chartName = 'chart' + i
    const topics = Object.keys(data[subjects[i-1]])
    var scores = []
    for (j=0; j<topics.length; j++) {
        var total = data[subjects[i-1]][topics[j]]['total']
        var totalCorrect = data[subjects[i-1]][topics[j]]['total_correct']
        scores.push(Math.round(totalCorrect/total*100))
    }
    ctx = document.getElementById(chartName);
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topics,
            datasets: [{
            data: scores,
            borderWidth: 1,
            backgroundColor: colors
            }]
        },
        options: {
            maintainAspectRatio: false,
            plugins: {
            legend: {
                display: false,
            }
            },
            scales: {
            y: {
                beginAtZero: true,
                max: 100,
                ticks:{
                callback: (value) => {
                    return `${value}%`
                }
                }
            }
            }
        }
        });
}
