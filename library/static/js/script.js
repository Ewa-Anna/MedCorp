const script = function () {
    function selectedDate() {
        //min date to choose in calendar should be today
        const today = new Date().toISOString().split('T')[0]; //strip Date() from time; format: YYYY-MM-DD
        const maxDate = new Date();
        maxDate.setFullYear(maxDate.getFullYear() + 1); //max date to choose in calendar should be today + 1 year
        const max_date = maxDate.toISOString().split('T')[0];

        document.getElementById("selected_date").setAttribute("min", today);
        document.getElementById("selected_date").setAttribute("max", max_date);
    };

    function birthDate() {
        const maxDate = new Date();
        const birthdate = new Date();
        const today = new Date().toISOString().split('T')[0];
        birthdate.setFullYear(maxDate.getFullYear() - 100); //allow user to setup birthdate max 100 years prior to today
        const min_birthdate = birthdate.toISOString().split('T')[0];

        document.getElementById("birthdate").setAttribute("min", min_birthdate);
        document.getElementById("birthdate").setAttribute("max", today);
    };

    function chartForTimeSlots() {
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
    };

    window.addEventListener('DOMContentLoaded', () => {
        selectedDate();
        birthDate();
        chartForTimeSlots();
    });

}();

