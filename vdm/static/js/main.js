$(document).ready(function(e) { 

//$('#accordion').on('hidden.bs.collapse', function () {
////do something...
//})
//
//$('#accordion .accordion-toggle').click(function (e){
//  var chevState = $(e.target).siblings("i.indicator").toggleClass('glyphicon-triangle-right glyphicon-triangle-bottom');
//  $("i.indicator").not(chevState).removeClass("glyphicon-triangle-bottom").addClass("glyphicon-triangle-right");
//});
//
////table fixed column
//
//});




   // Make Expandable Rows.
//    $('tr.parent > td:first-child' || 'tr.parent > td:fourth-child')
//        .css("cursor", "pointer")
//        .attr("title", "Click to expand/collapse")
//        .click(function() {
//            var parent = $(this).parent();
//            parent.siblings('.child-' + parent.attr("id")).toggle();
//            parent.find(".glyphicon-triangle-right").toggleClass("glyphicon-triangle-bottom");
//        });
//   $('tr[class^=child-]').hide().children('td');
//
   
   
   //checkbox
   $("input[type=checkbox]").on('ifChanged', function () {
				var onOffText = $(this).is(":checked") ? "On" : "Off";
				$(this).parent().parent().next().text(onOffText);
            });