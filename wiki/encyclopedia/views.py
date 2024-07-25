from django.shortcuts import render, redirect
from django import forms
from . import util
from markdown2 import Markdown as MD
from random import choice

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    page = get_page(title)
    if page is not None:
        return render(request,   
                        "encyclopedia/entry.html", 
                        {"title": title.capitalize(), 
                        "text": MD().convert(page),
                        "title": title
                            }
                        ) 
    
    else:
        return render(request, "encyclopedia/entry_error.html", {"message": "404 - Page not found..."}  )
    
def edit(request, title):
    page = get_page(title)
    if page is None:
        return render(request, "encyclopedia/entry_error.html", {"message": "404 - Page not found..."}  )
    
    elif request.method == "GET":
        input_form = NewEntry({"title": title, "content": page})
        
        return render(
            request, "encyclopedia/edit.html", 
            {"form": input_form,
             "entry": title}
        )
    
    elif request.method == "POST":
        input_form = NewEntry(request.POST)
        if input_form.is_valid():
            title = input_form.cleaned_data.get("title")
            content = input_form.cleaned_data.get("content")

            util.save_entry(title, content)
            return redirect("entry", title=title)

    

def search(request):
    query = request.GET.get("q","").capitalize()
    page = get_page(query)
    if page is not None:
        return redirect("entry", title=query)
    substrings_found = set()
    
    for entry in util.list_entries():
        # if query in entry.capitalize():
        lower_entry = entry.lower()
        if lower_entry.find(query.lower()) != -1:
            substrings_found.add(entry)
    
    if substrings_found == set():
        return render(request, "encyclopedia/entry_error.html", {"message": "No such Page could be found :["}  )
    else:
        return render(request, "encyclopedia/search.html", {
            "entries": substrings_found
        })
    
def create_new_page(request):
    if request.method == "GET":
        return render(
            request, "encyclopedia/create_new_page.html", {"form": NewEntry()}
        )
    
    input_form = NewEntry(request.POST)
    if input_form.is_valid():
        title = input_form.cleaned_data.get("title")
        content = input_form.cleaned_data.get("content")

        if title.capitalize() in [entry.capitalize() for entry in util.list_entries()]:
            return render(request, "encyclopedia/entry_error.html", {"message": "This Article already exists..."} )
        
        else:
            with open(f"entries/{title}.md", "w") as file:
                file.write(f"# {title} \n")
                file.write(content)
            return redirect("entry", title=title)

def random(request):
    
    page_name = choice(util.list_entries())
    return redirect("entry", title=page_name)


class NewEntry(forms.Form):
    title = forms.CharField(
        required = True,
        label = "",
        widget = forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        )
    )

    content = forms.CharField(
        required = True,
        label = "",
        widget = forms.Textarea(
            attrs = {
                "class": "form-control mb-4",
                "placeholder": "Content (markdown)",
                "id": "new_content",
            }
        )
    )

def get_page(title):
    try:
        if title.capitalize() in [entry.capitalize() for entry in util.list_entries()]:
            page = util.get_entry(title)
            return page
        else:
            return None
    except:
        return None
