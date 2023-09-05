//Chart for analytics.html for statistics
//Get data from routes get_data
fetch("/get_data")
    .then(response => response.json())
    .then(data => {
        var ctx = document.getElementById("popularity").getContext("2d");
        new Chart(ctx, {
            type: "bar",
            data: {
                labels: Object.keys(data.grouped_data).map(time => {
                    const hours = parseInt(time);
                    const minutes = (time - hours) * 60;
                    const formattedTime = `${hours.toString().padStart(2, '0')}:${minutes === 0 ? '00' : minutes.toString().padStart(2, '0')}`;
                    return formattedTime;
                }),
                datasets: [{
                    label: "Popular timeslots",
                    data: Object.values(data.grouped_data),
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }}]
                }
            }
        })
    });
