function validar(form){
    var telefono=form.telefono.value;
    var password=form.password.value;
    var cadena=evaluarTelefono(telefono);
    cadena+=validarLongitudPassword(password);
    cadena+=passwordRobusto(password);
    var div=document.getElementById("notificaciones");
    if(cadena==''){
        div.innerHTML="";
        return true;
    }
    else{
        div.innerHTML=cadena;
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
function validarLongitudPassword(cadena){
    var salida="";
    if(cadena.length<8){
        salida="Debes introducir un password de al menos 8 caracteres.\n";
    }
    return salida;
}
function tieneDigito(cadena){
    var ban=false;
    for(i=0;i<cadena.length;i++){
        var cod=cadena.charCodeAt(i);
        if(cod>=48 && cod<=57){
            ban=true;
            break;
        }
    }
    return ban;
}
function passwordRobusto(cadena){
    var salida="";
    if(!tieneDigito(cadena)){
        salida="El password debe incluir al menos un digito \n";

    }
    if(!tieneMayuscula(cadena)){
        salida+='El password debe incluir al menos una mayuscula \n';
    }
    if(!tieneCaracterEspecial(cadena)){
        salida+='El password debe incluir al menos un caracter especial \n';
    }
    return salida;
}
function tieneMayuscula(cadena){
    var ban=false;
    for(i=0;i<cadena.length;i++){
        var cod=cadena.charCodeAt(i);
        if((cod>=65 && cod<=90)|| cod==165){
            ban=true;
            break;
        }
    }
    return ban;
}
function tieneCaracterEspecial(cadena){
    var ban=false;
    for(i=0;i<cadena.length;i++){
        var cod=cadena.charCodeAt(i);
        if((cod>=32 && cod<=47)||(cod>=58 && cod<=64) || (cod>=91 && cod<=96) || (cod>=123 && cod<=126) || cod==173){
            ban=true;
            break;
        }
    }
    return ban;
}
function ver(){
    var check=document.getElementById("verPassword");
    if(check.checked){
        document.getElementById("password").setAttribute("type","text");
    }
    else{
        document.getElementById("password").setAttribute("type","password");
    }
}
function consultarEmail(){
    var ajax=new XMLHttpRequest();
    var email=document.getElementById("email").value;
    var url='/usuarios/email/'+email;
    var div=document.getElementById("notificaciones");
    ajax.open('Get',url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
           var respuesta=JSON.parse(this.responseText);
           if(respuesta.estatus=='Ok'){
               document.getElementById("registrar").removeAttribute("disabled");
               div.innerHTML="";
           }
           else{
                document.getElementById("registrar").setAttribute("disabled","true"); 
                div.innerHTML=respuesta.mensaje;
           }
        }
    };
    ajax.send();
}