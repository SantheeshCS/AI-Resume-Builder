from django.template.loader import render_to_string
from io import BytesIO

try:
    from weasyprint import HTML
except Exception:
    HTML = None

def render_resume_pdf(template_name, context):
    if HTML is None:
        raise RuntimeError(
            "PDF generation is disabled in local Windows environment. "
            "Use Linux deployment for WeasyPrint support."
        )

    html_string = render_to_string(template_name, context)
    result = BytesIO()
    HTML(string=html_string).write_pdf(result)
    return result.getvalue()
