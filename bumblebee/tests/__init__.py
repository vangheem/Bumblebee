

basichtml = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"> 
<html> 
<head> 
    <meta http-equiv="content-type" content="text/html; charset=iso-8859-1"/> 
    <meta name="description" content="description"/> 
    <meta name="keywords" content="keywords"/> 
    <meta name="author" content="author"/> 
    <title>Test Page</title> 
 
    <link href="/static/style.css" media="all" rel="stylesheet"/> 
    <script type="text/javascript" src="/static/jquery.js"></script>  
    <script type="text/javascript"> 
        $(function(){
            $('#something').remove();
        });
    </script> 
 
    <style type="text/css"> 
    div#wrapper {
        width: 665px;
    }
    </style> 
</head> 
<body> 
    <div id="wrapper"> 
        <div id="logo"> 
            <a href="/"> 
                <img src="/logo.jpg" alt="FBI Delivery System"/> 
            </a> 
        </div> 
        <div id="content"> 
            <h1>Page Title</h1> 
            <p> blah, blah, blah</p>
        </div>
        <div id="footer">
            footer text
        </div>
    </div>
</body> 
</html>"""