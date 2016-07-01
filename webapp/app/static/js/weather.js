$(function show_weather() {
    $.getJSON("/show_forecast", function(data) {
        forecast(data.address);
        console.log(data.address);
    });
});


function forecast(address) {
    $.simpleWeather({
        woeid: '', //2357536
        location: address,
        unit: 'f',
        success: function(weather) {
            html = '<h2><i class="icon-' + weather.forecast[1].code + ' weatheri"></i>' + weather.forecast[1].high + '&deg;' + weather.units.temp + '</h2>';
            html += '<ul><li>' + weather.city + ', ' + weather.region + '</li>';
            html += '<li class="currently">' + weather.forecast[1].text + '</li>';
            html += '<li>' + weather.forecast[1].alt.low + '~' + weather.forecast[1].alt.high + '&deg;C</li></ul>';
            $("#weather").html(html);
        },
        error: function(error) {
            $("#weather").html('<p>' + error + '</p>');
        }
    });
};
