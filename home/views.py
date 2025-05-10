from django.shortcuts import render,redirect
from .models import todo

# Create your views here.
def home(request):
    allTODO = todo.objects.all()
    context = {
        "items" : allTODO
    }

    if request.method == "POST":
        data = request.POST

        title = data.get('title')
        description = data.get('description')

        print(title)
        print(description)
        item = todo.objects.create(
            title = title,
            description = description,
            status = "In progress"
        )

        print(item)

        return redirect("/")

    return render(request,"home.html",context)

def delete_item(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.delete()

    return redirect("/")

def update_status_to_finish(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.status = "Finished"
    item.save()

    return redirect("/")

def update_status_to_progress(request,id):
    print(id)
    item = todo.objects.get(id = id)
    item.status = "In Progress"
    item.save()

    return redirect("/")
