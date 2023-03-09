from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django import forms
from random import choice
import markdown2
from . import util


class new_page_form(forms.Form):
    title = forms.CharField(required = True, widget = forms.TextInput(attrs = {
        "placeholder": "Page title",
        "style": "width: 300px",
        "class": "form-control",
        }))
    text = forms.CharField(required = True, widget = forms.Textarea(attrs = {
        "placeholder": "Page text",
        "style": "width: 600px",
        "class": "form-control",
        "rows": "20",
        }))
    
class edit_page_form(forms.Form):
    title = forms.CharField(required = True, widget = forms.TextInput(attr = {
        "placeholder": "Page title",
        "style": "width: 300px",
        "class": "form-control",
        }))
    text = forms.CharField(required = True, widget = forms.Textarea(attrs = {
        "placeholder": "Page text",
        "style": "width: 600px",
        "class": "form-control",
        "rows": "20",
        }))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, title):
    # Show first links
    
    file = util.get_entry(title)
    if not file:
        return render(request, "encyclopedia/404.html")
    page_text = markdown2.markdown(file)
    
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
    
def edit(request, title):  
    if request.method == "POST":
        form = edit_page_form(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            text = form.cleaned_data.get("text")
            text = f'# {title}\n{text}'
            util.save_entry(title, text)
            return redirect('entry', title)
   
    else:
        with open(f'./entries/{title}.md') as current_page:
                current_data = current_page.readlines()   
                
        entry_data = {
            "title": title,
            "text": " ".join(current_data[1:]),
            }
        
        return render(request, "encyclopedia/editpage.html", {
            "edit_page_form": edit_page_form(entry_data),
        })

    
def random(request):
    random_page = choice(util.list_entries())
    return redirect('entry', random_page)
    
