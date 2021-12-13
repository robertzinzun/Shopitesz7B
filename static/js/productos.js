function incrementar(id){
    var cant="cant"+id;
    var exist="exis"+id;
    var cantidad=document.getElementById(cant).value;
    var existencia=parseInt(document.getElementById(exist).textContent);
    if(cantidad<existencia)
        cantidad++;
    else
        alert('Producto agotado');
    document.getElementById(cant).value=cantidad;
}
function decrementar(id){
    var cant="cant"+id;
    var cantidad=document.getElementById(cant).value;
    if(cantidad>1)
        cantidad--;
    document.getElementById(cant).value=cantidad;
}
function comprar(id){
    //alert(id);
    var cantAux="cant"+id;
    var precAux="prec"+id;
    var cantidad=parseInt(document.getElementById(cantAux).value);
    var precio=parseFloat(document.getElementById(precAux).textContent);
    //alert(precio);
    document.getElementById("cantidad").textContent=cantidad;
    document.getElementById("precio").textContent=precio;
    document.getElementById("producto").textContent=document.getElementById("prod"+id).textContent;
    document.getElementById("subtotal").textContent=precio*cantidad;
    document.getElementById("idProducto").value=id;
    document.getElementById("imagen").setAttribute("src","/productos/imagen/"+id);
}
function carrito(){
    var id=parseInt(document.getElementById("idProducto").value);
    var cantidad=parseInt(document.getElementById("cantidad").textContent);
    var ajax=new XMLHttpRequest();
    url="/carrito/agregar"
    var ojson={idProducto:id,cantidad:cantidad};
    ajax.open("post",url,true);
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            alert(respuesta.mensaje);
            document.getElementById("productos").textContent=respuesta.productos;
        }
    };
    ajax.setRequestHeader("Content-type", "application/json");
    ajax.send(JSON.stringify(ojson));
}