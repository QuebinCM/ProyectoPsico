const start_test = document.getElementById("start-test");
const start_container = document.getElementById("start-test-container");
const test_container = document.getElementById("test-form-container");
const tiempo = document.getElementById("tiempo");

var minutos = 0;
var segundos = 0;

start_test.addEventListener("click", function () {
    start_container.classList.toggle("hide-start");
    test_container.classList.add("show-test");

    var intervalo = setInterval(function () {
        segundos++;

        if (segundos === 60) {
            minutos++;
            segundos = 0;
        }

        var formatoMinutos = minutos < 10 ? "0" + minutos : minutos;
        var formatoSegundos = segundos < 10 ? "0" + segundos : segundos;

        if (minutos === 60) {
            alert("¡Ha pasado una hora, se recargará la página!");
            window.location.reload();
        }

        tiempo.value = formatoMinutos + ":" + formatoSegundos;
    }, 1000);
});
