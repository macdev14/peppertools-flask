document.addEventListener("DOMContentLoaded", function (event) {
  if (parseInt(document.getElementById("Id_Cliente")) <= 0) {
    getElementById("msg").innerHTML = "Selecione um cliente válido";
    document.getElementById("cad").disabled = true;
  }
});




//document.getElementById("query").addEventListener('change', filterOs());
