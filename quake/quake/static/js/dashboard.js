$(document).ready(
    function () {
        last_day_chart(JSON.parse(_chart_day_data.replace(/&#x27;/g, '"')));
        last_month_chart(JSON.parse(_chart_mon_data.replace(/&#x27;/g, '"')));
        max_mag(JSON.parse(_chart_max_data.replace(/&#x27;/g, '"')));

        document.getElementById("dashUpdateBtn").onclick = function () {
            dashupdate(true);
        };

        setInterval(
            function () {
                dashupdate(false);
            }, 60000);

    });

function dashupdate(showModal) {
    if (showModal) {
        $('#waitModal').modal('show');
    }

    $.ajax({
            url: 'update',
            success: function (response) {
                //console.log(response);

                last_day_chart(response.chart_day_data);
                last_month_chart(response.chart_mon_data);
                max_mag(response.chart_max_data);
            }
        })
        .always(function () {
            $('#waitModal').modal('hide');
        });
}