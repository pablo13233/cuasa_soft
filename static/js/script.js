


$(document).ready(function(){

    


    $("#menu_sidebar").on( "click", function() {
      
      
              
      var elemento = document.getElementById('navbar');

      elemento.classList.toggle("close");

      //var element  = document.getElementById('body');

      //element.style.backgroundColor='#18191a';
      //alert("Hello! I am an alert box!!");
    });

    

    
      /**------------------------------------------------------------------------- */
      var win = navigator.platform.indexOf('Win') > -1;
      if (win && document.querySelector('#sidenav-scrollbar')) {
        var options = {
          damping: '0.5'
        }
        Scrollbar.init(document.querySelector('#sidenav-scrollbar'), options);
      };
  
  });




