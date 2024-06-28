from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    print("entry called")
    if title.capitalize() in [entry.capitalize() for entry in util.list_entries()]:
        page = util.get_entry(title)

        return render(request,   "encyclopedia/entry.html", 
                        {"title": title.capitalize(), 
                        "text": page
                        }
                    ) 
    
    else:
        return render(request, "encyclopedia/entry_error.html", )