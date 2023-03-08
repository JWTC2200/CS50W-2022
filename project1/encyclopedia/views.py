from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django import forms
import markdown
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
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
    
def search(request):
    q = request.POST.get('q')
    if q in util.list_entries():
        return redirect('entry', q)
    else:
        partial_matches = []
        for page in util.list_entries():
            if q.lower() in page.lower():
                partial_matches.append(page)
        return render(request, "encyclopedia/results.html", {
            "matches": partial_matches,
        })
    
    
        
