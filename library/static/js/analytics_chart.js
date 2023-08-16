//Chart for analytics.html for statistics
//Get data from routes get_data
fetch("/get_data")
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById("popularity").getContext("2d");
        new Chart(ctx, {
            type: "horizontalBar",
            data: {
                labels: data.timeslots,
                datasets: [{
                    label: "Popular timeslots",
                    data: data.app_count,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    xAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        })
    });
