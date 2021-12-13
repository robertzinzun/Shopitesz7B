function seleccionar(id){
    calcularTotales();
}
function calcularTotales(){
    var arrChecks=document.getElementsByName("idCarrito");
    var subtotal=0;
    var envio=0;
    var total=0;
    for(i=0;i<arrChecks.length;i++){
        var id=arrChecks[i].value;
        if(arrChecks[i].checked){
            subtotal+=parseFloat(document.getElementById("subtotal"+id).textContent);
            envio+=parseFloat(document.getElementById("envio"+id).textContent);
        }
    }  
    total=envio+subtotal;  
    document.getElementById("total").textContent=total;
    document.getElementById("subtotal").textContent=subtotal;
    document.getElementById("costosEnvio").textContent=envio;

}
function seleccionarTodos(){
    var check=document.getElementById("todos");   
    var arrChecks=document.getElementsByName("idCarrito");
    if(check.checked){
        for(i=0;i<arrChecks.length;i++){
            arrChecks[i].checked=true;
        }    
    }
    else{
        for(i=0;i<arrChecks.length;i++){
            arrChecks[i].checked=false;
        }    
    }
    calcularTotales();
}
function pagar(){
    var total=parseFloat(document.getElementById("total").textContent);
    var arrChecks=document.getElementsByName("idCarrito");
    var ban=false;
    for(i=0;i<arrChecks.length;i++){
        if(arrChecks[i].checked){
            ban=true;
            break;
        }
    }
    if(ban==false){
        document.getElementById("notificaciones").style.display='block';
        document.getElementById("notificaciones").innerHTML='Debes seleccionar el producto a pagar.';
        document.getElementById("tarjetas").style.display='none';
    }
    else{
        document.getElementById("notificaciones").style.display='none';
        document.getElementById("notificaciones").innerHTML='';
        document.getElementById("tarjetas").style.display='block';
        document.getElementById("totalPedido").textContent=total;
        document.getElementById("tarjeta").options[0].selected=true;
        document.getElementById("btnPagar").setAttribute("disabled","true");
        document.getElementById("saldo").textContent="";
        document.getElementById("banco").textContent="";

    }

}
function registrarPedido(){
    var idTarjeta=parseInt(document.getElementById("tarjeta").options[document.getElementById("tarjeta").options.selectedIndex].value);
    var total=parseFloat(document.getElementById("total").textContent);
    var subtotal=parseFloat(document.getElementById("subtotal").textContent);
    var envio=parseFloat(document.getElementById("costosEnvio").textContent);
    var pedido={idTarjeta:idTarjeta,envio:envio,subtotal:subtotal,total:total,carrito:[]};
    var arrChecks=document.getElementsByName("idCarrito");
    for(i=0;i<arrChecks.length;i++){
        var id=arrChecks[i].value;
        if(arrChecks[i].checked){
            var idProd=parseInt(document.getElementById("idProducto"+id).value);
            var subProd=parseFloat(document.getElementById("subtotal"+id).textContent);
            var precio=parseFloat(document.getElementById("precio"+id).textContent);
            var cantidad=parseInt(document.getElementById("cantidad"+id).textContent);
            var producto={idProducto:idProd,precio:precio,cantidad:cantidad,subtotal:subProd};
            pedido.carrito.push(JSON.stringify(producto));
        }
    }  
    var ajax=new XMLHttpRequest();
    var url="/pedidos/registrar";
    ajax.open("post",url,true);
    ajax.onreadystatechange=function(){
        if(this.status==200 && this.readyState==4){
            var respuesta=JSON.parse(this.responseText);
            alert(respuesta.mensaje);
        }
    }
    ajax.setRequestHeader("Content-type", "application/json");
    ajax.send(JSON.stringify(pedido));
}
function mostrarTarjeta(){
    var ajax=new XMLHttpRequest();
    var id=document.getElementById("tarjeta").options[document.getElementById("tarjeta").options.selectedIndex].value;
    document.getElementById("saldo").value="";
    document.getElementById("banco").value="";
    if(id!=0){
        url='/tarjetas/'+id;
        ajax.open('get',url,true);
        ajax.onreadystatechange=function(){
            if(this.status==200 && this.readyState==4){
                var tarjeta=JSON.parse(this.responseText);
                llenarCamposTarjeta(tarjeta);
            }
        };
        ajax.send();
    }
    else{
        document.getElementById("saldo").textContent=tarjeta.saldo;
        document.getElementById("banco").textContent=tarjeta.banco;
        document.getElementById("btnPagar").setAttribute("disabled","true");
    }
}
function llenarCamposTarjeta(tarjeta){
    document.getElementById("saldo").textContent=tarjeta.saldo;
    document.getElementById("banco").textContent=tarjeta.banco;
    var total= document.getElementById("totalPedido").textContent;
    if(tarjeta.saldo>=total){
        document.getElementById("btnPagar").removeAttribute("disabled");
    }
    else{
        document.getElementById("btnPagar").setAttribute("disabled",true);
    }
}