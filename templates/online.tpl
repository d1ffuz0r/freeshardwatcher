%rebase templates/base active = "online"
<div style="width: 900px; margin: 0 auto;">
    <input type="text" id="char">
    <button id="send">GET</button>
</div>
<table style="display: none;">
	<caption>Online users</caption>
	<thead>
		<tr class="all">
			<td></td>
			%for day in ALL:
			  <th scope="col">{{ day }}</th>
			%end
		</tr>
	</thead>
	<tbody>
		<tr>
			<th scope="row">dSpIN</th>
            %for ds in DSPIN:
              <td>{{ ds }}</td>
            %end
		</tr>
	</tbody>
</table>