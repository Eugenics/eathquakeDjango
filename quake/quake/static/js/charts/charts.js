$(document).ready(
    function () {
        last_day_chart();
        last_month_chart();
        max_mag();

    });


function last_day_chart() {
    var json_day_data = JSON.parse(_chart_day_data.replace(/&#x27;/g, '"'));
    var chart_day_data = [];
    for (var k in json_day_data) {
        chart_day_data.push(json_day_data[k]);
    }

    var color = Chart.helpers.color;
    var ctx = document.getElementById("dayChart");
    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ["mag < 3", "mag between 3 and 6", "mag > 6"],
            datasets: [{
                backgroundColor: [
                    color(window.chartColors.green).alpha(0.5).rgbString(),
                    color(window.chartColors.yellow).alpha(0.5).rgbString(),
                    color(window.chartColors.red).alpha(0.5).rgbString(),
                ],
                hoverBackgroundColor: [
                    window.chartColors.green,
                    window.chartColors.yellow,
                    window.chartColors.red,
                ],
                borderWidth: 1,
                label: 'Total in past 24 hours:',
                data: chart_day_data,
            }, ],
        },
        options: {
            maintainAspectRatio: false,
            legend: {
                display: true,
                position: 'bottom'
            },
            cutoutPercentage: 50,
        },
    });
}



function last_month_chart() {
    var json_data = JSON.parse(_chart_mon_data.replace(/&#x27;/g, '"'));
    var chart_mon_data = [];
    for (var k in json_data) {
        chart_mon_data.push(json_data[k]);
    }
    //console.log(chart_data);

    var color = Chart.helpers.color;
    var ctx = document.getElementById("monthChart");
    var myPieChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ["mag < 3", "mag between 3 and 6", "mag > 6"],
            datasets: [{
                backgroundColor: [
                    color(window.chartColors.green).alpha(0.5).rgbString(),
                    color(window.chartColors.yellow).alpha(0.5).rgbString(),
                    color(window.chartColors.red).alpha(0.5).rgbString(),
                ],
                hoverBackgroundColor: [
                    window.chartColors.green,
                    window.chartColors.yellow,
                    window.chartColors.red,
                ],
                borderWidth: 1,
                label: 'Total in past month:',
                data: chart_mon_data,
            }],
        },
        options: {
            maintainAspectRatio: false,
            legend: {
                display: true,
                position: 'bottom'
            },
            cutoutPercentage: 50,
        },
    });
}


function max_mag() {
    json_data = JSON.parse(_chart_max_data.replace(/&#x27;/g, '"'));
    var chart_max_data = [];
    for (var k in json_data) {
        chart_max_data.push(json_data[k]);
    }

    var color = Chart.helpers.color;
    var ctx = document.getElementById("maxChart");
    var myPieChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ["max in last day", "max in month", "max in year"],
            datasets: [{
                backgroundColor: color(window.chartColors.green).alpha(0.5).rgbString(),
                hoverBackgroundColor: window.chartColors.green,
                borderWidth: 1,
                label: 'Max magnitude values:',
                data: chart_max_data,
            }],
        },
        options: {
            maintainAspectRatio: false,
            legend: {
                display: false,
                position: 'top'
            },
            cutoutPercentage: 0,
        },
    });
}