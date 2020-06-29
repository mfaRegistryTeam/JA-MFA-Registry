$(function() {
    $("#form-total").steps({
        headerTag: "h2",
        bodyTag: "section",
        transitionEffect: "fade",
        enableAllSteps: true,
        stepsOrientation: "vertical",
        autoFocus: true,
        transitionEffectSpeed: 500,
        titleTemplate: '<div class="title">#title#</div>',
        labels: {
            previous: '<i class="zmdi zmdi-arrow-left"></i>',
            next: '<i class="zmdi zmdi-arrow-right"></i>',
            finish: '<i class="zmdi zmdi-check" ></i>    ',
        },
    })
});



/*Attempt at setting min date for calendar */

$(document).ready(function() {

  // var today = new Date();
  // var dd = today.getDate();
  // var mm = today.getMonth()+1; //January is 0!
  // var yyyy = today.getFullYear();
  //  if(dd<10){
  //         dd='0'+dd
  //     } 
  //     if(mm<10){
  //         mm='0'+mm
  //     } 
  
  // today = new Date(yyyy,dd,mm);
  // document.getElementById("ret_date").setAttribute("min", today);
  // document.getElementById("dept_date").setAttribute("min", today);

    /* by default hide all radio_content div elements except first element */
    $(".content .radio_content").hide();
    $(".content .radio_content:first-child").show();

    /* when any radio element is clicked, Get the attribute value of that clicked radio element and show the 
    radio_content div element which matches the attribute value and hide the remaining tab content div elements */
    $(".radio_wrap").click(function() {
        var current_raido = $(this).attr("data-radio");
        $(".content .radio_content").hide();
        $("." + current_raido).show();
    })
});


var FormStuff = {
    
  
    init: function() {
      // kick it off once, in case the radio is already checked when the page loads
      this.applyConditionalRequired();
      this.bindUIActions();
    },
    
    bindUIActions: function() {
      // when a radio or checkbox changes value, click or otherwise
      $("input[type='radio'], input[type='checkbox']").on("change", this.applyConditionalRequired);
    },
    
    applyConditionalRequired: function() {
      // find each input that may be hidden or not
      $(".require-if-active").each(function() {
        var el = $(this);
        // find the pairing radio or checkbox
        if ($(el.data("require-pair")).is(":checked")) {
          // if its checked, the field should be required
          el.prop("required", true);
        } else {
          // otherwise it should not
          el.prop("required", false);
        }
      });
    }
  
  };
  
  FormStuff.init();


  $(document).ready(function() {
    $('input[type="radio"]').click(function() {
        if($(this).attr('id') == 'watch-me') {
             $('#show-me').show();           
        }
        else {
             $('#show-me').hide();   
        }
    });
 });


//  script for revealing forms for student, employed or others
function show2(){
  document.getElementById('div2').style.display = 'block';
  document.getElementById('div3').style.display = 'none'
  document.getElementById('div4').style.display = 'none'
}
function show3(){
  document.getElementById('div3').style.display = 'block';
  document.getElementById('div2').style.display = 'none'
  document.getElementById('div4').style.display = 'none'
}
function show4(){
  document.getElementById('div4').style.display = 'block';
  document.getElementById('div3').style.display = 'none'
  document.getElementById('div2').style.display = 'none'
}
