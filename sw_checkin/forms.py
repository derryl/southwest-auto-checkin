from django import forms


class EmailForm(forms.Form):
    email = forms.EmailField()


class NameForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)


class ReservationForm(forms.Form):
    confirmation_num = forms.CharField(max_length=13)
    flight_date = forms.DateField()
    flight_time = forms.TimeField()