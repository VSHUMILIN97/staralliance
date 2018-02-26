 var ws = new WebSocket("ws://" + window.location.hostname + ":8090/");
    function fix(value) {
    if (value.toString().indexOf('e')) {
    return value.toFixed(8);
        }
    else {
    return Number(Math.round(value+'e8')+'e-8');
     }
    }

 var checkBoxState = [];
function getCheckedBoxes(chkboxName) {
  var checkboxes = document.getElementsByName(chkboxName);
  var checkboxesChecked = [];
  // loop over them all
  for (var i=0; i<checkboxes.length; i++) {
     // And stick the checked ones onto an array...
     if (checkboxes[i].checked) {
        checkboxesChecked.push(checkboxes[i]);
     }
  }
  // Return the array if it is non-empty, or null
  return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}

    ws.onopen = function(event){

    };
    ws.onclose = function (event) {
         if (event.wasClean){
             alert('Соединение закрыто');
         } else{
             alert('Соединение оборвано по причине: ' + event.reason + ' - код ошибки: '+ event.code );
         }
     };
    ws.onerror = function (error) {
         alert('Ошибка - ' + error.data);
     };
    ws.onmessage = function (event) {
        var msg = JSON.parse(event.data);
        var json_msg = JSON.parse(msg['ticks']);
        var table = document.getElementById("tableID");
        while(table.firstChild) table.removeChild( table.firstChild ); // Удаляет все корневые элементы на старте и заполняет таблицу заново
        var tableHead = document.createElement('thead');
        table.appendChild(tableHead);
        var tr = document.createElement('tr');
        tr.style.minHeight = "5px";
        tableHead.appendChild(tr);

        //var rows = msg['rows'],
        // columns = msg['columns'];

        var th = document.createElement('th');
        th.style.width = "150px";
        tr.appendChild(th);

        for (var name in msg['cnames']) {
            var th = document.createElement('th');
            th.appendChild(document.createTextNode((msg['cnames'])[name]));
            th.style.width = "110px";
            var checkbox = document.createElement("INPUT");
            checkbox.type = "checkbox";
            th.appendChild(checkbox);
             th.onclick = function () {

              var checkedBoxes = getCheckedBoxes("mycheckboxes");
              var t = document.getElementById('tableID');
              var tbody = table.getElementsByTagName('tbody')[0];
              var trow = t.getElementsByTagName('tr');
              var therow = tbody.getElementsByTagName('th');
              var thead = document.getElementsByTagName('thead');
              var theadrow = thead[0].getElementsByTagName('tr');
              var theadr = theadrow[0].getElementsByTagName("th");
              var gettercount;
              for (var ink = 0; ink < theadr.length; ink++) {
                  if (this.innerHTML === theadr[ink].innerHTML && theadr[ink] !== theadr[0]) {
                      //theadr[ink].hidden = true;
                      gettercount = ink
                  }
              }
              for (var i = 0; i < trow.length; i++) {
                  var cell = trow[i].getElementsByTagName("td");
                  for (var int = 0; int < cell.length; int++) {
                      if (this.cellIndex !== int + 1) {
                          cell[int].style.visibility = 'hidden';
                      } else {
                          if (cell[int].innerHTML === '—') {
                              trow[i].classList.add('hid');
                          }
                      }
                  } // Идея. Воспользоваться - в полях и скрывать по ним. Нет значения, значит нет монеты.
                         }// Идея говно


            //t.classList.add('hideUninteresting');
             };
            tr.appendChild(th);
        }



        var tableBody = document.createElement('tbody');
        table.appendChild(tableBody);


        for (var r in msg['rnames']) {
            var tr = document.createElement('tr');
            var text = (msg['rnames'])[r];
            var th = document.createElement('th');
            th.appendChild(document.createTextNode(text));
            tr.appendChild(th);
            for (var c in msg['cnames']) {
                var success = false;
                for (var iter = 0; iter < json_msg.length; iter++){
                var io = json_msg[iter]['Value'];
                for (var commendme in io) {
                    //alert(io[commendme]['PairName']);

                    if ((io[commendme]['PairName'] === (msg['rnames'])[r]) && (io[commendme]['Exchange'] === (msg['cnames'])[c])) {
                        var td = document.createElement('td');
                        var v = io[commendme]['Tick'];
                        if (v !== 0) {
                            td.appendChild(document.createTextNode(fix(v)));
                        } else {
                            td.appendChild(document.createTextNode('—'));
                        }
                        /*if (json_msg[i]['Chg'] == 'U') {
                            td.appendChild(document.createElement("up"));
                        } else if (json_msg[i]['Chg'] == 'D') {
                            td.appendChild(document.createElement("down"));
                        }*/
                        td.setAttribute("id", (msg['rnames'])[r] + "_" + (msg['cnames'])[c]);
                        tr.appendChild(td);
                        //tr.replaceChild(td);
                        success = true;
                    }
                }
                }
                if (success === false) {
                    var td = document.createElement('td');
                    var v = '—';
                    td.appendChild(document.createTextNode(v));
                    tr.appendChild(td);
                }
            }
            tr.setAttribute("title", text);
            tableBody.appendChild(tr);
        }
        var tbody = table.getElementsByTagName('tbody')[0];
        var trow = tbody.getElementsByTagName('tr');

        for (var i = 0, len = trow.length; i < len; i++) {
            var cells = trow[i].getElementsByTagName('td');
            var max = -999999999,
                min = 99999999999,
                maxi, mini;
            for (var j = 0, lent = cells.length; j < lent; j++) {
                if (parseFloat(cells[j].innerHTML, 10) > max) {
                    max = parseFloat(cells[j].innerHTML, 10);
                }
                if (parseFloat(cells[j].innerHTML, 10) < min) {
                    min = parseFloat(cells[j].innerHTML, 10);
                }
                if (cells[j].innerText === '—') {
                    cells[j].classList.toggle("nope");
                }
            }
            if (((max - min) / max) * 100 > 3) {
                for (var j = 0, lent = cells.length; j < lent; j++) {
                    if (parseFloat(cells[j].innerHTML, 10) === max) {
                        cells[j].classList.toggle("max");
                    }
                    else if (parseFloat(cells[j].innerHTML, 10) === min) {
                        cells[j].classList.toggle("min");
                    }
                }
            }
            else {
                trow[i].classList.add("hid");
            }
        }

        var elements = document.getElementsByTagName('tr');
        for (var i = 1; i < elements.length; i++) {
            (elements)[i].addEventListener("click", function () {
                this.classList.toggle("selected");
                var ups = this.getElementsByTagName('up');
                var downs = this.getElementsByTagName('down');
                var cells = this.getElementsByTagName("td");
                var h = this.getElementsByTagName("th");
                for (var i = 0, len = cells.length; i < len; i++) {
                    cells[i].classList.toggle("selected");
                }
                for (var i = 0, len = ups.length; i < len; i++) {
                    ups[i].classList.toggle("selected");
                }
                for (var i = 0, len = downs.length; i < len; i++) {
                    downs[i].classList.toggle("selected");
                }
                for (var i = 0, len = h.length; i < len; i++) {
                    h[i].classList.toggle("selected");
                }
            });
        }

        document.getElementById("scrdiv").addEventListener('scroll', function () {
            this.querySelector("thead").style.transform = "translate(0," + this.scrollTop + "px)";
        }, false);

        var btn = document.getElementById("hidebt");
        if (!btn.hasAttribute("onclick")) {
            document.getElementById("hidebt").addEventListener('click', function () {
                table.classList.toggle("hideUninteresting");
                if (this.innerText === "Show Useless") {
                    this.innerText = "Hide Useless";
                }
                else {
                    this.innerText = "Show Useless";
                }
            }, false);
            btn.setAttribute("onclick","true");
        }
   };
