$(function(){

 	    $('.carousel').carousel({
            interval: 5432
        });

        $('#idBotonBorrar').click(function(){//contacto.html borrar formularios
            $('#id_nombre').val("");
            $('#id_correo').val("");
            $('#id_mensaje').val(""); 
            $('#id_asunto').val("");
        });

        $('#eve').mouseover(function(){
    		$('#descr').css("display", "block");
	   });
	   $('#eve').mouseout(function () {
      		$('#descr').hide();      
	   });
});

$(function(d, s, id) {
      var js, fjs = d.getElementsByTagName(s)[0];
      if (d.getElementById(id)) return;
      js = d.createElement(s); js.id = id;
      js.src = "//connect.facebook.net/es_ES/sdk.js#xfbml=1&version=v2.3";
      fjs.parentNode.insertBefore(js, fjs);
      }(document, 'script', 'facebook-jssdk'));

