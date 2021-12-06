function validar(form){
    var telefono=form.telefono.value;
    var cadena=evaluarTelefono(telefono);
    if(cadena==''){
        return true;
    }
    else{
        alert(cadena)
        return false;
    }
}
function evaluarTelefono(cadena){
    var salida="";
    var patron=/[0-9]{3}-[0-9]{3}-[0-9]{4}/;
    var res=patron.test(cadena);
    if(res==false){
        salida="Debes informar un número telefonico con el siguiente formato:###-###-#### \n";
    }
    return salida;
}