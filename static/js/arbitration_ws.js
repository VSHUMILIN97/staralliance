var rinput = document.getElementById("pairDif");

function fix(value) {
		var prec = 9 - value.toString().split('.')[0].length;
        if (prec < 0) {
        		return value.toString().split('.')[0];
        }
        if (value.toString().indexOf('e') > 0) {
            return value.toFixed(8);
        }
        else {
            return Number(Math.round(value + 'e' + prec) +'e-' + prec).toFixed(prec);
        }
}

// Supportive function to provide search in the current table
function searchFunc() {
  // Declare variables
  var input, filter, table, tr, td, i, ftable;
  input = document.getElementById("unique");
  filter = input.value.toUpperCase();
  ftable = document.getElementById("tableID");
  table = ftable.getElementsByTagName("tbody")[0];
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    var h = tr[i].getElementsByTagName("th")[0];

    if (h) {
      if (h.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function exchHider(){
    var table = document.getElementById("tableID");
    var tbody = table.getElementsByTagName('tbody')[0];
    var trow = tbody.getElementsByTagName('tr');
    var table_state = document.getElementsByName('chck');

        for (var secinter = 0; secinter < trow.length; secinter++){
                    var cells = trow[secinter].getElementsByTagName('td');
                    if (trow[secinter].classList.contains('hidpairrow')){
                        trow[secinter].classList.remove('hidpairrow');
                    }
                    var countingstarts = 0;
                    var counter = 0;
                    for (var trdinter = 0; trdinter < cells.length; trdinter++){
                        if (cells[trdinter].classList.contains('pairhid')){
                            cells[trdinter].classList.remove('pairhid');
                        }
                        if (table_state[trdinter].checked === false){
                            cells[trdinter].classList.toggle('pairhid')
                        } else if (table_state[trdinter].checked === true){
                            counter++;
                            if (cells[trdinter].innerText === '—'){
                                countingstarts++;
                            }
                        }
                    }
                    if (countingstarts >= counter - 1){
                        trow[secinter].classList.toggle('hidpairrow')
                    }
                }
}

function maxormin(int){
    var tbody = table.getElementsByTagName('tbody')[0];
     var trow = tbody.getElementsByTagName('tr');
     var cells = trow[int].getElementsByTagName('td');
     var max = -999999999, min = 99999999999, indexmin, indexmax, hider;
     hider = rinput.value;
     if (hider < 1 || hider >= 99){
         hider = 3
     }
     trow[int].classList.remove('hid');
           for (var joy = 0; joy < cells.length; joy++) {
               if (cells[joy].classList.contains('nope')){
                   cells[joy].classList.remove('nope')
               }
               if (cells[joy].classList.contains('max')){
                   cells[joy].classList.remove('max')
               }
               if (cells[joy].classList.contains('min')){
                   cells[joy].classList.remove('min')
               }
               if (parseFloat(cells[joy].innerText) > max) {
                   max = parseFloat(cells[joy].innerText);
                   indexmax = cells[joy].cellIndex - 1;
               }
               if (parseFloat(cells[joy].innerText) < min) {
                   min = parseFloat(cells[joy].innerText);
                   indexmin = cells[joy].cellIndex - 1;
               }
               if (cells[joy].innerText === '—') {
                   cells[joy].classList.toggle("nope");
               }
           }
           if (((max - min) / max) * 100 > hider) {
               cells[indexmax].classList.toggle("max");
               cells[indexmin].classList.toggle("min");
           }
           else {
               trow[int].classList.add("hid");
           }
}

 var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
 var ws = new WebSocket(ws_scheme + '://' +  window.location.host + ':8070/arbitr');
//Second button supportive hide function
 var myexchs = document.getElementById("myexchs").value;
 var mypairs = document.getElementById("mypairs").value;
 var myticks = document.getElementById("myticks").value;
 var notarray = myexchs + '';
 var raw_data = JSON.stringify(myticks);
 var preparsed_data = JSON.parse(raw_data);
 var truly_ticks = JSON.parse(preparsed_data);
 var nosecondarray = mypairs + '';
 var truly_array = notarray.replace('[', '').replace(']', '').split(',');
 var truly_pairs = nosecondarray.replace('[', '').replace(']', '').split(',');


 var table = document.getElementById("tableID");
 var tableHead = document.createElement('thead');
 table.appendChild(tableHead);
 var tr = document.createElement('tr');
 tr.style.minHeight = "5px";
 tableHead.appendChild(tr);
 // The real header with Exchanges 150px height.
 var th = document.createElement('th');
 var x = document.createElement("INPUT");
 x.type = "text";
 x.id = "unique";
 x.name = "search";
 x.setAttribute("placeholder", "Searching field");
 x.style.width = "150px";
 x.onkeyup = function () {searchFunc()};
 th.style.width = "150px";
 th.appendChild(x);
 tr.appendChild(th);

 for (var inter = 0; inter < truly_array.length; inter++) {
            var th = document.createElement('th');
            th.appendChild(document.createTextNode(truly_array[inter]));
            th.style.width = "110px";
            th.name = 'HEADER';
            var checkbox = document.createElement("INPUT");
            checkbox.type = "checkbox";
            checkbox.checked = 'true';
            checkbox.name = 'chck';
            th.appendChild(checkbox);
      tr.appendChild(th);
 }


 var tableBody = document.createElement('tbody');
 table.appendChild(tableBody);
        var liter = 0;
        /* Massive loop-block. Pushes data from server JSON array to our table.
         * Creates blocks, cells and rows dynamically.
         * Throw - into the cell if there are no value for this Exchanger, but the pair exists.
         */
        for (var trend in truly_pairs) {

            var tr = document.createElement('tr');
            var text = truly_pairs[trend].toString();
            var th = document.createElement('th');
            th.appendChild(document.createTextNode(text));
            tr.appendChild(th);
            for (var exch in truly_array) {
                var td = document.createElement('td');
                var ex = truly_array[exch].toString();
                var full_text = ex.replace('"', '').replace('"', '') + '/' + text.replace('"', '').replace('"', '');
                full_text = full_text.replace(' ', '').replace(' ', '');
                var v;
                if (truly_ticks[liter][full_text] !== undefined){
                    v = truly_ticks[liter][full_text];
                    liter++;
                } else {
                    v = 0;
                }
                if (v !== 0) {
                    td.appendChild(document.createTextNode(fix(parseFloat(v))));
                } else {
                    td.appendChild(document.createTextNode('—'));
                }
                //Unnecessary block for now
                //Toggles the UP Green arrow and the DOWN Red arrow
                /*if (json_msg[i]['Chg'] == 'U') {
                 td.appendChild(document.createElement("up"));
                 } else if (json_msg[i]['Chg'] == 'D') {
                 td.appendChild(document.createElement("down"));
                 }*/
                td.setAttribute("id", (text + "_" + truly_array[exch]));
                tr.appendChild(td);

            }
            tr.setAttribute("title", text);
            tableBody.appendChild(tr);
        }
    document.getElementById("scrdiv").addEventListener('scroll', function () {
            this.querySelector("thead").style.transform = "translate(0," + this.scrollTop + "px)";
        }, false);

        //First button. Hides only non-Max&Min rows.
        var btn = document.getElementById("hidebt");
        document.getElementById("hidebt").addEventListener('click', function () {
            table.classList.toggle("hideUninteresting");
            /*if (this.innerText === "Show Useless") {
                this.innerText = "Hide Useless";
            }
            else {
                this.innerText = "Show Useless";
            }*/
            }, false);
        btn.setAttribute("onclick","true");

        //Second button
        var btn_pair = document.getElementById("pairhider");
        document.getElementById("pairhider").addEventListener('click', function () {
            if (table.classList.contains('hidePair')){
                table.classList.remove('hidePair')
            }
            exchHider();
            table.classList.add("hidePair");
            }, false);
        btn_pair.setAttribute("onclick","true");



 var mxmnrows = tableBody.getElementsByTagName('tr');
 for (var mxmn = 0; mxmn < mxmnrows.length; mxmn++){
     maxormin(mxmn)
 }

 rinput.onchange = function () {
     if (rinput.value >= 1 && rinput.value <= 99) {
         for (var mxmn = 0; mxmn < mxmnrows.length; mxmn++) {
             maxormin(mxmn)
         }
     }
     else {
         rinput.value = 3;
         for (var mxmn2 = 0; mxmn2 < mxmnrows.length; mxmn2++) {
             maxormin(mxmn2)
         }
     }
 };


 var input = document.getElementById("unique");
 var filter = input.value.toUpperCase();
 if (filter !== ''){
     searchFunc()
 }


 // Initial on connection. Maybe it's better to check which transport is used by browser to pass data.
 ws.onopen = function(event){
     // clear
 };

 ws.onmessage = function (event) {
     var message = JSON.parse(event.data);
     var info_half = message[0].split('/');
     var exch = info_half[0];
     var pair = info_half[1];
     var tick = message[1];
     var state_num;
     var thead = table.getElementsByTagName('th');
     for (var nul = 0; nul < thead.length; nul++){
         if (thead[nul].innerText === '"' + exch + '"'){
             state_num = nul - 1;
             break;
         }
     }
     var tbody = table.getElementsByTagName('tbody')[0];
     var tablerow = tbody.getElementsByTagName('tr');
     for (var iter = 0; iter < tablerow.length; iter++){
         var th = tablerow[iter].getElementsByTagName('th');
         if (th[0].innerText === '"' + pair + '"'){
             var td = tablerow[iter].getElementsByTagName('td');
             var currentVal = td[state_num].innerText;
             td[state_num].innerText = fix(parseFloat(tick));
             if (currentVal > fix(parseFloat(tick)) && currentVal != '—'){
                 td[state_num].appendChild(document.createElement('down'))
             }
             else if (currentVal < fix(parseFloat(tick)) && currentVal != '—') {
                 td[state_num].appendChild(document.createElement('up'))
             }
             maxormin(iter);
             break;
         }
     }
 };

 /* Works, when the server or client goes away.
  * Better to release all the memory and so on there.
  */
 ws.onclose = function (event) {
      if (event.wasClean){
          alert('Соединение закрыто');
      } else{
          alert('Your connection was closed. If you want to continue, reload this page.');
      }
  };

 // It's clear, I guess
 ws.onerror = function (error) {
     // pass
 };
