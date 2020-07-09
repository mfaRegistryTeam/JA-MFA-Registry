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
            finish: '<i type="submit" class="zmdi zmdi-check" ></i>',
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

// Makes certain feilds required based on choice from radio button
// ---------------------------------------
$(document).ready(function() {
    $('input:radio[name="classification"]').change(function() {
        if ($(this).val() == 'CitizenTO') {
            // alert('type A');
            $("#radio").prop("required", true);
            $("#street_bb").prop("required", true);
            $("#city_town_bb").prop("required", true);
            $("#parish_bb").prop("required", true);
            $("#street_abroad").prop("required", true);
            $("#city_town_abroad").prop("required", true);
            $("#state_abroad").prop("required", true);
            $("#country_abroad").prop("required", true);
            $("#firstname_ab").prop("required", true);
            $("#lastname_ab").prop("required", true);
            $("#emerg_rel_ab").prop("required", true);
            $("#emerg_phone_ab").prop("required", true);
            $("#emerg_email_ab").prop("required", true);
            $("#dept_date").prop("required", true);
            $("#ret_date").prop("required", true);
            $("#residential_abroad").prop("required", true);
            $("#mobile_abroad").prop("required", true);
            $("#WA_abroad").prop("required", true);
            $("#abroad_email").prop("required", true);

            $("#street_ro").prop("required", false);
            $("#city_town_ro").prop("required", false);
            $("#state_ro").prop("required", false);
            $("#country_ro").prop("required", false);
            $("#residential_ro").prop("required", false);
            $("#mobile_ro").prop("required", false);
            $("#WA_ro").prop("required", false);
            $("#AOI").prop("required", false);

            $("#AOI_fr").prop("required", false);
            $("#KBB").prop("required", false);

        } else if ($(this).val() == 'ResidentO') {
            // alert('type B');
            $("#street_ro").prop("required", true);
            $("#city_town_ro").prop("required", true);
            $("#state_ro").prop("required", true);
            $("#country_ro").prop("required", true);
            $("#residential_ro").prop("required", true);
            $("#mobile_ro").prop("required", true);
            $("#WA_ro").prop("required", true);
            $("#AOI").prop("required", false);

            $("#AOI_fr").prop("required", false);
            $("#KBB").prop("required", false);

            $("#radio").prop("required", false);
            $("#street_bb").prop("required", false);
            $("#city_town_bb").prop("required", false);
            $("#parish_bb").prop("required", false);
            $("#street_abroad").prop("required", false);
            $("#city_town_abroad").prop("required", false);
            $("#state_abroad").prop("required", false);
            $("#country_abroad").prop("required", false);
            $("#firstname_ab").prop("required", false);
            $("#lastname_ab").prop("required", false);
            $("#emerg_rel_ab").prop("required", false);
            $("#emerg_phone_ab").prop("required", false);
            $("#emerg_email_ab").prop("required", false);
            $("#dept_date").prop("required", false);
            $("#ret_date").prop("required", false);
            $("#residential_abroad").prop("required", false);
            $("#mobile_abroad").prop("required", false);
            $("#WA_abroad").prop("required", false);
            $("#abroad_email").prop("required", false);

        } else if ($(this).val() == 'Friend') {
            // alert('type B');
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);
            $("#AOI_fr").prop("required", false);

            $("#KBB").prop("required", false);
            $("#KBB").prop("required", false);
            $("#KBB").prop("required", false);
            $("#KBB").prop("required", false);
            $("#KBB").prop("required", false);
            $("#KBB").prop("required", false);

            $("#radio").prop("required", false);
            $("#street_bb").prop("required", false);
            $("#city_town_bb").prop("required", false);
            $("#parish_bb").prop("required", false);
            $("#street_abroad").prop("required", false);
            $("#city_town_abroad").prop("required", false);
            $("#state_abroad").prop("required", false);
            $("#country_abroad").prop("required", false);
            $("#firstname_ab").prop("required", false);
            $("#lastname_ab").prop("required", false);
            $("#emerg_rel_ab").prop("required", false);
            $("#emerg_phone_ab").prop("required", false);
            $("#emerg_email_ab").prop("required", false);
            $("#dept_date").prop("required", false);
            $("#ret_date").prop("required", false);
            $("#residential_abroad").prop("required", false);
            $("#mobile_abroad").prop("required", false);
            $("#WA_abroad").prop("required", false);
            $("#abroad_email").prop("required", false);

            $("#street_ro").prop("required", false);
            $("#city_town_ro").prop("required", false);
            $("#state_ro").prop("required", false);
            $("#country_ro").prop("required", false);
            $("#residential_ro").prop("required", false);
            $("#mobile_ro").prop("required", false);
            $("#WA_ro").prop("required", false);
            $("#AOI").prop("required", false);
        }
    });
});

$(document).ready(function() {
    $('input[type="radio"]').click(function() {
        if ($(this).attr('id') == 'watch-me') {
            $('#show-me').show();
        } else {
            $('#show-me').hide();
        }
    });
});


//  script for revealing forms for student, employed or others
function show2() {
    document.getElementById('div2').style.display = 'block';
    document.getElementById('div3').style.display = 'none'
    document.getElementById('div4').style.display = 'none'
}

function show3() {
    document.getElementById('div3').style.display = 'block';
    document.getElementById('div2').style.display = 'none'
    document.getElementById('div4').style.display = 'none'
}

function show4() {
    document.getElementById('div4').style.display = 'block';
    document.getElementById('div3').style.display = 'none'
    document.getElementById('div2').style.display = 'none'
}