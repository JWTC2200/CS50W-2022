from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django import forms
import markdown
from . import util


class new_page_form(forms.Form):
    title = forms.CharField(required = True)
    text = forms.CharField(required = True, widget = forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    # Show first links
    
    file = util.get_entry(title)
    if not file:
        return render(request, "encyclopedia/404.html")
    page_text = markdown.markdown(file)
    
    return render(request, "encyclopedia/entry.html", {
        "page_title": title,
        "page_text": page_text,
    })
    
def search(request):
    q = request.POST.get("q")
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

def newpage(request):
    if request.method == "POST":
        form = new_page_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            text = form.cleaned_data.get("text")
            text = f'# {title}\n\n{text}'
            
            if title in util.list_entries():
                return render(request, "encyclopedia/409.html")
            else:
                util.save_entry(title, text)
                return redirect('entry', title)
                    
    return render(request, "encyclopedia/newpage.html", {
        "new_page_form": new_page_form
    })
    
        
