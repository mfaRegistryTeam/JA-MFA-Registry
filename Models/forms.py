from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import RadioField, DateField,widgets
from wtforms import Form, IntegerField, StringField, BooleanField,SelectField, TextAreaField, validators, DecimalField,DateTimeField

class RegisterForm(Form):
    first_name = StringField('',[validators.required()] )
    middle_name = StringField('',[validators.required()] )
    last_name = StringField('',[validators.required()] )
    Gender = RadioField('',choices=[
        ('Male','Male'), ('Female','Female')])
    DOB = DateTimeField('', format='%Y-%m-%d')
    
    street_jm = StringField('',[validators.required()] )
    city_town_jm = StringField('',[validators.required()])
    parish_jm = StringField('',[validators.required()] )

    marital_status = RadioField('',choices=[
        ('Single','Single'), ('Married','Married'), ('Widowed','Widowed'),('Divorced','Divorced')], default=None)

    
    occupation = RadioField('',choices=[
        ('Student','Student'), ('Employed','Employed'),('Unemployed','Unemployed'), ('Other','Other')], default=None)

    
    ja_passport_num = StringField('',[validators.required()] )
    other_passport_num = StringField('',[validators.optional()] )
    WeChat = StringField('',[validators.optional()] )
    landline = StringField('',[validators.optional()] )
    whatsapp_num = StringField('',[validators.optional()] ) 
    other_contacts = TextAreaField('',[validators.optional()] )
    study_details = TextAreaField('',[validators.optional()] )
    edu_addr = TextAreaField('',[validators.optional()] )
    edu_inst = StringField('',[validators.optional()] )
    job_title = StringField('',[validators.optional()])
    workplace_details = TextAreaField('',[validators.optional()] )
    other = TextAreaField('',[validators.optional()] )
    
    emerg_firstname = StringField('',[validators.optional()] )
    emerg_lastname = StringField('',[validators.optional()] )
    emerg_rel = StringField('',[validators.optional()] )
    emerg_phone = StringField('',[validators.optional()] )
    emerg_email = StringField('',[validators.optional()] )

    emerg_firstname2 = StringField('',[validators.optional()] )
    emerg_lastname2 = StringField('',[validators.optional()] )
    emerg_rel2 = StringField('',[validators.optional()] )
    emerg_phone2 = StringField('',[validators.optional()] )
    emerg_email2 = StringField('',[validators.optional()] )
    POT_des = TextAreaField('',[validators.optional()] )


    airport_details_1 = StringField('',[validators.optional()] )
    short_ext_street_1 = StringField('',[validators.optional()] )
    short_ext_city_1 = StringField('',[validators.optional()] )
    short_ext_state_1 = StringField('',[validators.optional()] )
    # short_ext_fname_1 = StringField('',[validators.optional()] )
    # short_ext_lname_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_1 = StringField('',[validators.optional()] )
    quick_details_1 = TextAreaField('',[validators.optional()] )


    quick_details_2_1 = TextAreaField('',[validators.optional()] )
    airport_details_2_1 = StringField('',[validators.optional()] )
    short_ext_street_2_1 = StringField('',[validators.optional()] )
    short_ext_city_2_1 = StringField('',[validators.optional()] )
    short_ext_state_2_1 = StringField('',[validators.optional()] )
    # short_ext_fname_2_1 = StringField('',[validators.optional()] )
    # short_ext_lname_2_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_2_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_2_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_2_1 = StringField('',[validators.optional()] )
    
    airport_details_2_2 = StringField('',[validators.optional()] )
    short_ext_street_2_2 = StringField('',[validators.optional()] )
    short_ext_city_2_2 = StringField('',[validators.optional()] )
    short_ext_state_2_2 = StringField('',[validators.optional()] )
    # short_ext_fname_2_2 = StringField('',[validators.optional()] )
    # short_ext_lname_2_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_2_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_2_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_2_2 = StringField('',[validators.optional()] )
    quick_details_2_2 = TextAreaField('',[validators.optional()] )

    airport_details_3_1 = StringField('',[validators.optional()] )
    short_ext_street_3_1 = StringField('',[validators.optional()] )
    short_ext_city_3_1 = StringField('',[validators.optional()] )
    short_ext_state_3_1 = StringField('',[validators.optional()] )
    # short_ext_fname_3_1 = StringField('',[validators.optional()] )
    # short_ext_lname_3_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_3_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_3_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_3_1 = StringField('',[validators.optional()] )
    quick_details_3_1 = TextAreaField('',[validators.optional()] )


    airport_details_3_2 = StringField('',[validators.optional()] )
    short_ext_street_3_2 = StringField('',[validators.optional()] )
    short_ext_city_3_2 = StringField('',[validators.optional()] )
    short_ext_state_3_2 = StringField('',[validators.optional()] )
    # short_ext_fname_3_2 = StringField('',[validators.optional()] )
    # short_ext_lname_3_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_3_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_3_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_3_2 = StringField('',[validators.optional()] )
    quick_details_3_2 = TextAreaField('',[validators.optional()] )


    airport_details_3_3 = StringField('',[validators.optional()] )
    short_ext_street_3_3 = StringField('',[validators.optional()] )
    short_ext_city_3_3 = StringField('',[validators.optional()] )
    short_ext_state_3_3 = StringField('',[validators.optional()] )
    # short_ext_fname_3_3 = StringField('',[validators.optional()] )
    # short_ext_lname_3_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_3_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_3_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_3_3 = StringField('',[validators.optional()] )
    quick_details_3_3 = TextAreaField('',[validators.optional()] )


    airport_details_4_1 = StringField('',[validators.optional()] )
    short_ext_street_4_1 = StringField('',[validators.optional()] )
    short_ext_city_4_1 = StringField('',[validators.optional()] )
    short_ext_state_4_1 = StringField('',[validators.optional()] )
    # short_ext_fname_4_1 = StringField('',[validators.optional()] )
    # short_ext_lname_4_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_4_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_4_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_4_1 = StringField('',[validators.optional()] )
    quick_details_4_1 = TextAreaField('',[validators.optional()] )

    airport_details_4_2 = StringField('',[validators.optional()] )
    short_ext_street_4_2 = StringField('',[validators.optional()] )
    short_ext_city_4_2 = StringField('',[validators.optional()] )
    short_ext_state_4_2 = StringField('',[validators.optional()] )
    # short_ext_fname_4_2 = StringField('',[validators.optional()] )
    # short_ext_lname_4_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_4_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_4_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_4_2 = StringField('',[validators.optional()] )
    quick_details_4_2 = TextAreaField('',[validators.optional()] )


    airport_details_4_3 = StringField('',[validators.optional()] )
    short_ext_street_4_3 = StringField('',[validators.optional()] )
    short_ext_city_4_3 = StringField('',[validators.optional()] )
    short_ext_state_4_3 = StringField('',[validators.optional()] )
    # short_ext_fname_4_3 = StringField('',[validators.optional()] )
    # short_ext_lname_4_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_4_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_4_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_4_3 = StringField('',[validators.optional()] )
    quick_details_4_3 = TextAreaField('',[validators.optional()] )



    airport_details_4_4 = StringField('',[validators.optional()] )
    short_ext_street_4_4 = StringField('',[validators.optional()] )
    short_ext_city_4_4 = StringField('',[validators.optional()] )
    short_ext_state_4_4 = StringField('',[validators.optional()] )
    # short_ext_fname_4_4 = StringField('',[validators.optional()] )
    # short_ext_lname_4_4 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_4_4 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_4_4 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_4_4 = StringField('',[validators.optional()] )
    quick_details_4_4 = TextAreaField('',[validators.optional()] )


    airport_details_5_1 = StringField('',[validators.optional()] )
    short_ext_street_5_1 = StringField('',[validators.optional()] )
    short_ext_city_5_1 = StringField('',[validators.optional()] )
    short_ext_state_5_1 = StringField('',[validators.optional()] )
    # short_ext_fname_5_1 = StringField('',[validators.optional()] )
    # short_ext_lname_5_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_5_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_5_1 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_5_1 = StringField('',[validators.optional()] )
    quick_details_5_1 = TextAreaField('',[validators.optional()] )

    airport_details_5_2 = StringField('',[validators.optional()] )
    short_ext_street_5_2 = StringField('',[validators.optional()] )
    short_ext_city_5_2 = StringField('',[validators.optional()] )
    short_ext_state_5_2 = StringField('',[validators.optional()] )
    # short_ext_fname_5_2 = StringField('',[validators.optional()] )
    # short_ext_lname_5_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_5_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_5_2 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_5_2 = StringField('',[validators.optional()] )
    quick_details_5_2 = TextAreaField('',[validators.optional()] )

    

    airport_details_5_3 = StringField('',[validators.optional()] )
    short_ext_street_5_3 = StringField('',[validators.optional()] )
    short_ext_city_5_3 = StringField('',[validators.optional()] )
    short_ext_state_5_3 = StringField('',[validators.optional()] )
    # short_ext_fname_5_3 = StringField('',[validators.optional()] )
    # short_ext_lname_5_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_5_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_5_3 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_5_3 = StringField('',[validators.optional()] )
    quick_details_5_3 = TextAreaField('',[validators.optional()] )

    airport_details_5_4 = StringField('',[validators.optional()] )
    short_ext_street_5_4 = StringField('',[validators.optional()] )
    short_ext_city_5_4 = StringField('',[validators.optional()] )
    short_ext_state_5_4 = StringField('',[validators.optional()] )
    # short_ext_fname_5_4 = StringField('',[validators.optional()] )
    # short_ext_lname_5_4 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_5_4 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_5_4 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_5_4 = StringField('',[validators.optional()] )
    quick_details_5_4 = TextAreaField('',[validators.optional()] )

    airport_details_5_5 = StringField('',[validators.optional()] )
    short_ext_street_5_5 = StringField('',[validators.optional()] )
    short_ext_city_5_5 = StringField('',[validators.optional()] )
    short_ext_state_5_5 = StringField('',[validators.optional()] )
    # short_ext_fname_5_5 = StringField('',[validators.optional()] )
    # short_ext_lname_5_5 = StringField('',[validators.optional()] )
    # short_ext_emerg_rel_5_5 = StringField('',[validators.optional()] )
    # short_ext_emerg_phone_5_5 = StringField('',[validators.optional()] )
    # short_ext_emerg_email_5_5 = StringField('',[validators.optional()] )
    quick_details_5_5 = TextAreaField('',[validators.optional()] )

    

    