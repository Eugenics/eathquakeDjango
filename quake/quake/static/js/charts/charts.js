$(document).ready(
    function () {
        last_day_chart();

    });


function last_day_chart() {
    var json_day_data = JSON.parse(chart_day_data.replace(/&#x27;/g, '"'));
    var chart_day_data = [];
    for (var k in json_day_data) {
        chart_day_data.push(json_day_data[k]);
    }

    var json_mon_data = JSON.parse(chart_mon_data.replace(/&#x27;/g, '"'));
    var chart_mon_data = [];
    for (k in json_mon_data) {
        chart_mon_data.push(json_mon_data[k]);
    }

    var color = Chart.helpers.color;
    var ctx = document.getElementById("dayChart");
    var myPieChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["less 3", "between 3 and 5", "greater 5"],
            datasets: [{
                    backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                    hoverBackgroundColor: window.chartColors.red,
                    borderWidth: 1,
                    label: 'Total in past 24 hours:',
                    data: chart_day_data,
                },
                {
                    backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                    hoverBackgroundColor: window.chartColors.red,
                    borderWidth: 1,
                    label: 'Total in past month:',
                    data: chart_mon_data,
                }
            ],
        },
        options: {
            maintainAspectRatio: false,
            legend: {
                display: false,
                position: 'bottom'
            },
            cutoutPercentage: 0,
        },
    });
}

/*

function last_month_chart() {
    var json_data = JSON.parse(chart_mon_data.replace(/&#x27;/g, '"'));
    var chart_data = [];
    for (var k in json_data) {
        chart_data.push(json_data[k]);
    }
    //console.log(chart_data);

    var color = Chart.helpers.color;
    var ctx = document.getElementById("monthChart");
    var myPieChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["less 3", "between 3 and 5", "greater 5"],
            datasets: [{
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                hoverBackgroundColor: window.chartColors.red,
                borderWidth: 1,
                label: 'Total in past 24 hours:',
                data: chart_data,
            }],
        },
        options: {
            maintainAspectRatio: false,
            legend: {
                display: false,
                position: 'bottom'
            },
            cutoutPercentage: 0,
        },
    });
}
*/