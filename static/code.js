function myFunction() {
    var x = document.getElementById("divspinner");
    var y = document.getElementById("divtable");
    var frec = document.getElementById("inputLarge");

    var dataa = 0;

    if (document.getElementById("customRadio1").checked) {
        dataa = { frecuencia: frec.value, tipo: 1 };
    } else {

        dataa = { frecuencia: frec.value, tipo: 0 };
    }
    if (x.style.display === "none") {
        x.style.display = "block";
    } else {

    }
    $.ajax({
            method: "POST",
            url: "http://localhost:8080/generar",
            data: dataa
        })
        .done(function(msg) {
            x.style.display = "none";
            y.innerHTML += msg;
            console.log(msg);
            y.style.display = "block";

        });
}


$("#idForm").submit(function(e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.
    console.log('jijijiji');
    var form = document.getElementById("idForm");
    var y = document.getElementById("divcards");
    var x = document.getElementById("divspinner");
    var data = new FormData(form);
    if (x.style.display === "none") {
        x.style.display = "block";
    }
    $.ajax({
        type: "POST",
        enctype: 'multipart/form-data',
        url: '/cargar_imagenes',
        data: data, // serializes the form's elements.
        processData: false,
        contentType: false,
        cache: false,
        success: function(data) {
            console.log(data); // show response from the php script.
            y.innerHTML = data;
        }
    });


});

function uploadd() {
    var x = document.getElementById("inputGroupFile02");
    var formdata = new FormData();
    var file = x.files[0];
    formdata.append("file", file);
    $.ajax({
            method: "POST",
            url: "http://localhost:8080/filtrar",
            data: file,
            processData: false,
            contentType: false
        })
        .done(function(msg) {
            console.log(msg);
        });

}