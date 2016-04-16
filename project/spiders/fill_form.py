from lxml import html


def _retrieve_form_element(form):
    fields = {}

    for x in form.inputs:
        fields[x.name] = x.value

    return {"fields": fields, "url": form.action}


def fetch_form(url, body):
    doc = html.document_fromstring(body, base_url=url)
    form_items = []
    for form in doc.xpath('//form'):
        form_items.append(_retrieve_form_element(form))
    return form_items
