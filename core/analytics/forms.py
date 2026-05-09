from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="CSV file", error_messages="empty": "Either the file is empty or invalid!")
    
    