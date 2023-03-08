from django.shortcuts import render
from django.http import HttpResponseRedirect
import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    # Show first links
    
    file = util.get_entry(title)
    if not file:
        return render(request, "encyclopedia/404.html", {
            "page_title": 404
        })
    page_text = markdown.markdown(file)
    
    return render(request, "encyclopedia/entry.html", {
        "page_title": title,
        "page_text": page_text,
    })
    
        