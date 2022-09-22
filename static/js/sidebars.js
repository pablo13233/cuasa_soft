$(document).ready(function () {

  $(".menu-bars").click(function () {
      $("#slide-menu").addClass("active");
  });

  $(".slide-menu-close").click(function () {
      $("#slide-menu").removeClass("active");
  });

  $(".skip-form-close").click(function () {
      $(".skip-header-dd").removeClass("active");
  });

  var togle = false;
  $(".dropdownmenu").click(function () {
      if (togle == false) {
          $(this).addClass("active");
          togle = true;
      } else {
          $(this).removeClass("active");
          togle = false;
      }
  });
});