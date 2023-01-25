from django.forms.widgets import ClearableFileInput


class AdminPDFWidget(ClearableFileInput):
    template_name = "admin/pdf_file_input.html"
