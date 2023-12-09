const input_genero = document.getElementById("input-genero");
const opt_container = document.getElementById("genero-options");
const svg = document.getElementById("genero-svg");

input_genero.addEventListener("click", function () {
    opt_container.classList.toggle("show-opt");
    svg.classList.toggle("trasform-svg");
});

function SelectOpt(Opt) {
    var opt = Opt.innerHTML;

    input_genero.value = opt;

    opt_container.classList.toggle("show-opt");
    svg.classList.toggle("trasform-svg");
}
