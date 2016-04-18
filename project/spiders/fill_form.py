from lxml import html


def _retrieve_form_element(form, origin_url):
    fields = {}
    for x in form.inputs:
        if x.value is None:
            x.value = "None"
        if x.name and x.type != "submit":
            fields[x.name] = [x.value]

    url = form.action
    if (url is None) or (url is ""):
        url = origin_url
    return {"fields": fields, "url": url}


def fetch_form(url, body):
    doc = html.document_fromstring(body, base_url=url)
    form_items = []
    for form in doc.xpath('//form'):
        form_items.append(_retrieve_form_element(form, url))
    return form_items
