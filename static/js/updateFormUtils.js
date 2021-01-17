//Author: Joshua Alkins


//--------SELECT TAG POPULATION------------------------------------------------------------------------------
function populate_select(options_array,select_id,default_option,includeNone){
    //populates a dropdown menu (with id == "select_id") with all options in options_array and sets the default selection
    var select = document.getElementById(select_id);
    select.innerHTML = ""

    if (includeNone){
        var none = 'None';

        var newOption = document.createElement("option");
        newOption.value = none;
        newOption.innerHTML = 'Please Select';

        if (none == default_option){
            newOption.selected="selected";
        }

        select.options.add(newOption);
    }

    for (var i in options_array){
        var option = options_array[i];

        var newOption = document.createElement("option");
        newOption.value = option;
        newOption.innerHTML = option;

        if (option == default_option){
            newOption.selected="selected";
        }

        select.options.add(newOption);
    }
}

function populate_countries(select_id,default_option,includeNone){
    //populates the list with countries array in formValues.js
    populate_select(countries,select_id,default_option,includeNone);
}

function populate_fields_of_study(select_id,default_option){
    //populates the list with fields_of_study array in formValues.js
    populate_select(fields_of_study,select_id,default_option,true);
}

function populate_job_classes(select_id,default_option){
    //populates the list with job_classes array in formValues.js
    populate_select(job_classes,select_id,default_option,true);
}

function populate_purpose_of_travel(select_id,default_option){
    //populates the list with purposes_of_travel array in formValues.js
    populate_select(purposes_of_travel,select_id,default_option,true);
}

function populate_jm_parishes(select_id,default_option){
    //populates the list with jm_parishes array in formValues.js
    populate_select(jm_parishes,select_id,default_option,true);
}


//--------CEHCKBOX POPULATION--------------------------------------------------------------------------------

function populate_checkbox(options_array,container_id,checkbox_id,default_options){
    var container = document.getElementById(container_id);
    

    for (var i in options_array){
        var option = options_array[i];

        var checkbox = document.createElement('input');
        checkbox.type='checkbox';
        checkbox.id=checkbox_id;
        checkbox.name=checkbox_id;
        checkbox.value=option;

        // if(option == default_options){
        //     checkbox.checked='checked';
        // }
     

        var label = document.createElement('label');
        label.htmlFor = option;
        label.appendChild(document.createTextNode(option));

        var br = document.createElement('br');
        var br2 = document.createElement('br');

        container.appendChild(checkbox);
        container.appendChild(label);
        container.appendChild(br);
        container.appendChild(br2);
    }

}

function populate_areas_of_interest(container_id,checkbox_id,default_options){
    populate_checkbox(areas_of_interest,container_id,checkbox_id,default_options);
}

function populate_kjm(container_id,checkbox_id,default_options){
    populate_checkbox(KJM,container_id,checkbox_id,default_options);
}

//--------CEHCKBOX POPULATION--------------------------------------------------------------------------------

function populate_radio(options_array,container_id,checkbox_id,default_option){
    var container = document.getElementById(container_id);
    

    for (var i in options_array){
        var option = options_array[i];

        var checkbox = document.createElement('input');
        checkbox.type='radio';
        checkbox.id=checkbox_id;
        checkbox.name=checkbox_id;
        checkbox.value=option;

        if(option == default_option){
            checkbox.checked='checked';
        }
     

        var label = document.createElement('label');
        label.htmlFor = option;
        label.appendChild(document.createTextNode(option));

        var br = document.createElement('br');
        var br2 = document.createElement('br');

        container.appendChild(checkbox);
        container.appendChild(label);
        container.appendChild(br);
        container.appendChild(br2);
    }

}

//--------DISPLAY CORRECT FORM SECTION-----------------------------------------------------------------------

//Requires removing setup from main.js & ids to be added to input radio button tags

function display_classification_form(classification){
    console.log("displaying classification: " + classification);
    switch(classification){
        case "CitizenTO":
            document.getElementById("CTO_radio").click();
            break;
        case "ResidentO":
            document.getElementById("BRO_radio").click();
            break;
        case "Friend":
            console.log("friend selected");
            document.getElementById("FOB_radio").click();
            break;
        default:
            document.getElementById("CTO_radio").click();
            break;
    }
}

function display_occupation_form(occupation){
    switch(occupation){
        case "Student":
            document.getElementById("Student").click();
            break;
        case "Employed":
            document.getElementById("Employed").click();
            break;
        case "Other":
            document.getElementById("Other").click();
            break;
        default:
            document.getElementById("Student").click();
            break;
    }
}

//--------Jamaica Radio Buttons------------------------------------------------------------------------------

function select_gender_radio(gender){
    switch(gender){
        case "Male":
            document.getElementById("male").click();
            break;
        case "Female":
            document.getElementById("female").click();
            break;
        default:
            document.getElementById("male").click();
            break; 
    }
}

function select_marital_status_radio(status){
    switch(status){
        case "Single":
            document.getElementById("Single").click();
            break;
        case "Married":
            document.getElementById("Married").click();
            break;
        case "Widowed":
            document.getElementById("Widowed").click();
            break;
        case "Divorced":
            document.getElementById("Divorced").click();
            break;
        default:
            document.getElementById("Single").click();
            break;
    }
}

function select_occupation_radio(occupation){
    switch(occupation){
        case "Student":
            document.getElementById("Student").click();
            break;
        case "Employed":
            document.getElementById("Employed").click();
            break;
        case "Unemployed":
            document.getElementById("Unemployed").click();
            break;
        case "Other":
            document.getElementById("Other").click();
            break;
        default:
            document.getElementById("Student").click();
            break;
    }
}

function select_study_level_radio(level){
    switch(level){
        case "Graduate":
            document.getElementById("Student").click();
            break;
        case "Undergraduate":
            document.getElementById("Employed").click();
            break;
        default:
            document.getElementById("Student").click();
            break;
    }
}

function select_amount_stop(amount){
    
    console.log("country_amt" + amount);
    document.getElementById("country_amt" + amount).click();

}


function select_duration_radio(value,amount,flight_order){
    var radio_id = "";

    var suffix = "_" + amount + "_" + flight_order;

    if(value=="Airport"){
        radio_id="airport" + suffix;
    }else if(value=="Short"){
        radio_id="short" + suffix;
    }else if(value=="Extended"){
        radio_id="extended" + suffix;
    }else{
        radio_id="airport" + suffix;
    }
    console.log(radio_id);
    document.getElementById(radio_id).click();
}

//--------FORM SETUP-----------------------------------------------------------------------------------------

//Requires removing code from steps

function form_setup() {
    //setsip the form by adding the form navigation buttons
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
    });
}

//--------HIDE AND DISPLAY FORM SECTIONS---------------------------------------------------------------------

//Replaces functions from main.js

function show_student_form(){
    document.getElementById('div2').style.display = 'block';
    document.getElementById('div3').style.display = 'none'
    document.getElementById('div4').style.display = 'none'
  }
  function show_employed_form(){
    document.getElementById('div3').style.display = 'block';
    document.getElementById('div2').style.display = 'none'
    document.getElementById('div4').style.display = 'none'
  }
  function show_other_occupation_form(){
    document.getElementById('div4').style.display = 'block';
    document.getElementById('div3').style.display = 'none'
    document.getElementById('div2').style.display = 'none'
  }


//Requires ids to be added to form container divs

  function show_CTO_form(){
    document.getElementById('CTO_form').style.display = 'block';
    document.getElementById('BRO_form').style.display = 'none'
    document.getElementById('FOB_form').style.display = 'none'
  }
  function show_BRO_form(){
    document.getElementById('CTO_form').style.display = 'none';
    document.getElementById('BRO_form').style.display = 'block'
    document.getElementById('FOB_form').style.display = 'none'
  }
  function show_FOB_form(){
    document.getElementById('CTO_form').style.display = 'none';
    document.getElementById('BRO_form').style.display = 'none'
    document.getElementById('FOB_form').style.display = 'block'
  }