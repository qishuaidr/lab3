from django.template import Context
from django.shortcuts import render
from addr_book.models import Book, Author
from django.template import RequestContext

def main(request):
#    a=Author(Name="1",Age="1",Country="1",AuthorID="1")
#    a.save()
#    c=Book(ISBN="1",Title="1",AuthorID=a,Publisher="1",PublishDate="1",Price="1")
#    c.save()
#    a=Author(Name="2",Age="2",Country="2",AuthorID="2")
#    a.save()
#    c=Book(ISBN="2",Title="2",AuthorID=a,Publisher="2",PublishDate="2",Price="2")
#    c.save()
#    a=Author(Name="3",Age="3",Country="3",AuthorID="3")
#    a.save()
#    c=Book(ISBN="3",Title="3",AuthorID=a,Publisher="3",PublishDate="3",Price="3")
#    c.save()
#    b=Book.objects.all()
#    a=Author.objects.all()
#    b.delete()
#    a.delete()
    post = request.POST
    name=""
    if post:
        name = post["name"]
        book_list = Book.objects.filter(AuthorID__Name=name)
        #c={"book_list":book_list,}
    else:
        book_list = Book.objects.all()
    c={"book_list":book_list,"name":name,}
    return render(request, 'main.html', c,context_instance=RequestContext(request))

def delete(request):
    ID=request.GET["id"]
    name=request.GET["name"]
    book_list=[]
    book=Book.objects.filter(ISBN=ID)
    book.delete()
    if (name==""):
        book_list = Book.objects.all()
    else:
        book_list = Book.objects.filter(AuthorID__Name=name)
    c={"book_list":book_list,}
    return render(request, 'main.html',c,context_instance=RequestContext(request))
    
def show(request):
    ID=request.GET["id"]
    book_list=Book.objects.filter(ISBN=ID)
    c={"book_list":book_list,}
    return render(request, 'show.html', c,context_instance=RequestContext(request))

def renew(request):
    ID=request.GET["id"]
    book=Book.objects.get(ISBN=ID)
    c={"book":book,}
    post = request.POST
    if post:
        author=Author.objects.filter(AuthorID=post["authorid"],)
        if author:
            new_book=Book(
            ISBN=post["isbn"],
            Title=post["title"],
            AuthorID=Author.objects.get(Name=post["authorid"]),
            Publisher=post["publisher"],
            PublishDate=post["publishdate"],
            Price=post["price"],)
            new_book.save()
            book.delete()
            c={"error":"success!","href":"/"}
        else:
            c={"error":"you hace to insert a new author!","href":"/add_author"}
    return render(request, 'renew.html',c,context_instance=RequestContext(request))
def add(request):
    post=request.POST
    c={}
    if post:
        author=Author.objects.filter(AuthorID=post["authorid"],)
        book=Book.objects.filter(ISBN=post["isbn"],)
        if author and not book:
            c={"error":"",}
            author=Author.objects.get(AuthorID=post["authorid"],)
            new_book=Book(
                ISBN=post["isbn"],
                Title=post["title"],
                AuthorID=author,
                Publisher=post["publisher"],
                PublishDate=post["publishdate"],
                Price=post["price"],
              )
            new_book.save()
        elif not author:
            c={"error":"press there to insert a new author","href":"/add_author"}  
        else:
            c={"error":"this isbn is existed!","href":"#"} 
    return render(request,'add.html',c,context_instance=RequestContext(request))

def add_author(request):
    post=request.POST
    c={}
    if post:
        author=Author.objects.filter(AuthorID=post["authorid"],)
        if author:
            c={"error":"this ID is exsited!",}
        else:
            c={"error":"success!",}
            new_author=Author(
                AuthorID=post["authorid"],
                Name=post["name"],
                Age=post["age"],
                Country=post["country"],
              )
            new_author.save()
    return render(request,'add_author.html',c,context_instance=RequestContext(request))  