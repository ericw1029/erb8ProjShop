from django import forms

class CsvImportForm(forms.Form):
    csv_file = forms.FileField(label="Select a CSV file to import")