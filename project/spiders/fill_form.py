from lxml import html


def _retrieve_form_element(form):
    fields = {}
    print "-------------------"
    for x in form.inputs:
        if x.value is None:
            x.value = "None"

        fields[x.name] = [x.value]

    return {"fields": fields, "url": form.action}


def fetch_form(url, body):
    doc = html.document_fromstring(body, base_url=url)
    form_items = []
    for form in doc.xpath('//form'):
        form_items.append(_retrieve_form_element(form))
    return form_items
