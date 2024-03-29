<!DOCTYPE HTML>
<html>
<head>
    <title>FreeShard Watcher</title>
    <meta http-equiv="content-type" content="text/html; charset=utf-8" />
    <link rel="stylesheet" href="/static/css/main.css" type="text/css" media="screen" charset="utf-8"/>
    <link rel="stylesheet" href="/static/css/visualize.css" type="text/css" media="screen" charset="utf-8"/>
    <link rel="stylesheet" href="/static/css/visualize-dark.css" type="text/css" media="screen" charset="utf-8"/>
    <link rel="stylesheet" href="/static/css/jquery-ui-1.8.16.custom.css" type="text/css" media="screen" charset="utf-8"/>
    <script type="text/javascript" src="/static/js/jquery-1.6.4.min.js"></script>
    <script type="text/javascript" src="/static/js/visualize.jQuery.js"></script>
    <script type="text/javascript" src="/static/js/jquery-ui-1.8.16.custom.min.js"></script>
    <script type="text/javascript" src="/static/js/example.js"></script>
    <script type="text/javascript" src="/static/js/excanvas.js"></script>
</head>
<body>
<div id="header">
  <h1><a href="/">FreeShard Watcher</a></h1>
  <ul id="menu">
    %if active == 'about':
      <li class="active"><a href="/">О сервисе</a></li>
    %else:
      <li><a href="/">О сервисе</a></li>
    %end
    %if active == 'download':
      <li class="active"><a href="/download/">Скачать</a></li>
    %else:
      <li><a href="/download/">Скачать</a></li>
    %end
    %if active == 'online':
      <li class="active"><a href="/online/">Онлайн версия</a></li>
    %else:
      <li><a href="/online/">Онлайн версия</a></li>
    %end
    %if active == 'help':
      <li class="active"><a href="/help/">Помощь</a></li>
    %else:
      <li><a href="/help/">Помощь</a></li>
    %end
    %if active == 'contact':
      <li class="active"><a href="/contact/">Контакты</a></li>
    %else:
      <li><a href="/contact/">Контакты</a></li>
    %end
  </ul>
</div>
%if active == 'about' or active == 'online':
  %include
%else:
  <div class="content">
    %include
  </div>
%end
<div id="footer">
  <p class="right">Design: <a href="http://www.solucija.com/">Luka Cvrk</a></p>
  <p>&copy; Copyright 2011 <a href="http://freeshardwatcher.tk">FreeShard Watcher</a></p>
</div>
</body>
</html>