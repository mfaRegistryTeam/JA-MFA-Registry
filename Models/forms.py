from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import RadioField, DateField,widgets
from wtforms import Form, IntegerField, StringField, BooleanField,SelectField, TextAreaField, validators, DecimalField,DateTimeField

class RegisterForm(Form):
    Firstname = StringField('',[validators.optional()] )
    Middlename = StringField('',[validators.optional()] )
    Lastname = StringField('',[validators.optional()] )
    Gender = RadioField('',choices=[
        ('Male','Male'), ('Female','Female')])
    dt = DateTimeField('', format='%Y-%m-%d')
    classification = RadioField('',choices=[
        ('CitizenTO','Barbadian Citizen Traveling Overseas'), ('ResidentO','Barbadian Resident Overseas'),('Friend','Friend of Barbados')], default=None)

    Type = RadioField('',choices=[
        ('Student','Student'), ('Employed','Employed'), ('Other','Other')], default=None)

    field_study_level = RadioField('',choices=[
        ('Graduate','Graduate'), ('Undergraduate','Undergraduate')], default=None)

    Jobtitle = StringField('',[validators.optional()])
    Workplacename = StringField('',[validators.optional()])
    EmpOther =  StringField('',[validators.optional()])
    OcpOther =  StringField('',[validators.optional()])
    PassportNumber = StringField('',[validators.optional()] )
    PassportCountry = StringField('',[validators.optional()] )
    WeChat = StringField('',[validators.optional()] )
    PhoneNumber = StringField('',[validators.optional()] )
    Street = StringField('',[validators.optional()] )
    street_bb = StringField('',[validators.optional()] )
    city_town_bb = StringField('',[validators.optional()] )
    CityorTown = StringField('',[validators.optional()] )
    Parish = StringField('',[validators.optional()] )
    EmergDetails = StringField('',[validators.optional()] )
    EmergencyConFirstname = StringField('',[validators.optional()] )
    EmergencyConLastname = StringField('',[validators.optional()] )
    EmergencyConRel = StringField('',[validators.optional()] )
    EmergencyConPhone = StringField('',[validators.optional()] )
    EmergencyConEmail = StringField('',[validators.optional()] )
    POT_des = TextAreaField('',[validators.optional()] )
    Classification = RadioField('',choices=[
        ('CitizenTO','Barbadian Citizen Traveling Overseas'), ('ResidentO','Barbadian Resident Overseas'), ('Friend','Friend of Barbados')], default=None)

    POTdescription = StringField('')
    AddressAbroad = StringField('',[validators.optional()] )
    State =  StringField('',[validators.optional()] )
    AbroadPhone = StringField('',[validators.optional()] )
    AbroadEmail = StringField('',[validators.optional()] )
    DepDate = StringField('',[validators.optional()] )
    ReturnDate = StringField('',[validators.optional()] )
    ResidentialPhoneNumberAbroad = StringField('',[validators.optional()] )
    MobilePhoneNumberAbroad = StringField('',[validators.optional()] )
    ResPhoneNumberAbroad = StringField('',[validators.optional()] )
    PhoneNumberAbroad = StringField('',[validators.optional()] )
    ResidentialAbroad = StringField('',[validators.optional()] )
    ResMobileAbroad = StringField('',[validators.optional()] )
    MobileAbroad = StringField('',[validators.optional()] )
    WhatsappAbroad = StringField('',[validators.optional()] )
    ResWhatsappAbroad = StringField('',[validators.optional()] )
    WechatAB = StringField('',[validators.optional()] )
    ResidentialWhatsappAbroad = StringField('',[validators.optional()] )
    ResWechatAB = StringField('',[validators.optional()] )


    ResidenceAbroadDetails = StringField('',[validators.optional()] )
    Location = StringField('',[validators.optional()] )
    AreaofInterestfr =RadioField('', choices=[('Education','Education'), ('Sports','Sports'), ('Investment','Investment'), ('Medical', 'Medical'), ('Volunteerism','Volunteerism'), ('Real-Estate','Real-Estate'), ('Culture','Culture'),('Geneology','Geneology'), ('Other','Other')], default=None)
    KnowBarbados = RadioField('', choices=[('Tourism','Tourism'), ('Business','Business'), ('Family','Family'), ('Medical', 'Medical'), ('Word of Mouth','Word of Mouth'), ('Other','Other')], default=None)
    street_abroad = StringField('',[validators.optional()] )
    city_abroad = StringField('',[validators.optional()] )
    state_abroad = StringField('',[validators.optional()] )
    resstreet_abroad = StringField('',[validators.optional()] )
    rescity_abroad = StringField('',[validators.optional()] )
    resstate_abroad = StringField('',[validators.optional()] )
    EmergencyConFirstnameab = StringField('',[validators.optional()] )
    EmergencyConLastnameab = StringField('',[validators.optional()] )
    EmergencyConRelab = StringField('',[validators.optional()] )
    EmergencyConPhoneab = StringField('',[validators.optional()] )
    EmergencyConEmailab = StringField('',[validators.optional()] )
    dep_date = DateField('', format='%Y-%m-%d')
    ret_date = DateField('', format='%Y-%m-%d')
    edu_inst = StringField('',[validators.optional()] )
