import cgi

if __name__== '__main__':
    
    form = cgi.FieldStorage()

    name = form.getvalue('nm')
    password = form.getvalue('pw')
    
    print(name)
