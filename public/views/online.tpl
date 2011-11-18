%rebase base active = "online"
<div style="width: 900px; margin: 0 auto;">
  <label for="text"></label><input type="text" id="char" id="text">
  <label for="dfrom"></label><input type="text" class="datap dfrom" id="dfrom">
  <label for="dto"></label><input type="text" class="datap dto" id="dto">
  <button id="send">GET</button>
</div>
<table style="display: none;">
  <caption>Online users</caption>
  <thead>
    <tr class="all">
    <td></td>
    %for day in all_days:
      <th scope="col">{{ day }}</th>
    %end
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">dSpIN</th>
      %for ds in default:
        <td>{{ ds }}</td>
      %end
    </tr>
  </tbody>
</table>