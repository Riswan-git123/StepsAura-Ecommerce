from django import forms

class ContactForm(forms.Form):
    name=forms.CharField(required=True,label="Name",max_length=30,error_messages={'required':'name required',
                                                                                  'invalid':'enter a valid name',
                                                                                  'max_length':'max length reached limit is 30'})
    email=forms.EmailField(required=True,label="Email",max_length=30,error_messages={'required':'email required',
                                                                                  'invalid':'enter a valid email',
                                                                                  'max_length':'max length reached limit is 30'})
    subject=forms.CharField(required=True,label="Subject",max_length=200)
    message=forms.CharField(required=True,label="Messsage",max_length=300)
    