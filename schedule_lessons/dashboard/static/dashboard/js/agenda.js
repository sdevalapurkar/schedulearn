$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    $(".option-icon").click(function(){
        $("#twoButtons").toggleClass("buttons-showHide");
        $(".option-icon").toggleClass("slide-position");
      });
});
