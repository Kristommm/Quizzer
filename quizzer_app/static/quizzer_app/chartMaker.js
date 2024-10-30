
const data = JSON.parse(document.getElementById('user_stats').textContent);
const subjects = Object.keys(data)
const colors = ['#ff80ed', '#065535', '#000000', '#133337', '#ffe4e1', '#008080', '#ff0000',
                '#e6e6fa', '#ffd700', '#00ffff', '#ffa500', '#0000ff', '#c6e2ff', '#b0e0e6',
                '#ff7373', '#40e0d0', '#d3ffce', '#f0f8ff', '#666666', '#faebd7', '#bada55'
                ]

for (i=1; i < subjects.length + 1; i++) {
    var chartName = 'chart' + i
    const topics = Object.keys(data[subjects[i-1]])
    const usedColors = colors.slice(0, topics.length)
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
            backgroundColor: usedColors
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
