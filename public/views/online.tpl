%rebase base active = "online"
<div class="online-rows">
    <p><label for="text">Ник</label><input type="text" id="char" id="text"></p>
    <p><label for="dfrom">От (дата)</label><input type="text" class="datap dfrom" id="dfrom"></p>
    <p><label for="dto">До (дата)</label><input type="text" class="datap dto" id="dto"></p>
    <p><button id="send">Получить</button></p>
</div>
<table style="display: none;">
  <caption>User online</caption>
  <thead>
    <tr class="all">
    <td></td>
    </tr>
  </thead>
  <tbody>
    <tr>
    </tr>
  </tbody>
</table>
<script type="text/javascript">
    $(function(){
        get(nick="dSpIN");
    });
</script>