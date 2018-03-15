 var ws = new WebSocket("ws://" + window.location.hostname + ":8090/");

//Second button supportive hide function
function forceRefresh(){
    var table = document.getElementById("tableID");
    var tbody = table.getElementsByTagName('tbody')[0];
    var trow = tbody.getElementsByTagName('tr');
        for (var secinter = 0; secinter < trow.length; secinter++){
                    var cells = trow[secinter].getElementsByTagName('td');
                    countingstarts = 0;
                    for (var trdinter = 0; trdinter < cells.length; trdinter++){
                        if (checkBoxState[trdinter] === false){
                            cells[trdinter].classList.toggle('pairhid')
                        } else if (cells[trdinter].innerText === '—'){
                            countingstarts++;
                        }
                    }
                    if (countingstarts >= checkBoxState.filter(isTrue).length - 1){
                        trow[secinter].classList.toggle('hidpairrow')
                    }
                }
}
// Supportive function to provide search in the current table
function searchFunc() {
  // Declare variables
  var input, filter, table, tr, td, i, ftable;
  input = document.getElementById("exchInput");
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
    // Supportive function to fix float number from math representation to classic 0.0000320421
    function fix(value) {
        if (value.toString().indexOf('e')) {
            return value.toFixed(8);
        }
        else {
            return Number(Math.round(value+'e8')+'e-8');
        }
    }

    //Supportive function. Used in array with .filter
    function isTrue(value) {
        return value === true
    }

 // Crutch for made it works.
var checkBoxState = [false, false, false, false, false, false, false, false, false, false, false, false, false];
    // Checking whether checkbox has false or true state.
    function getCheckedBoxes(chkboxName) {
        var checkboxes = document.getElementsByName(chkboxName);
        var checkboxesChecked = [];
        // loop over them all
        for (var i=0; i<checkboxes.length; i++) {
        // And stick the checked ones onto an array...
        if (checkboxes[i].checked) {
            checkboxesChecked.push(true);
        }
        else {
            checkboxesChecked.push(false);
        }
  }
  // Return the array if it is non-empty, or null
  return checkboxesChecked.length > 0 ? checkboxesChecked : null;
}
    // Initial on connection. Maybe it's better to check which transport is used by browser to pass data.
    ws.onopen = function(event){
        // clear
    };

    /* Works, when the server or client goes away.
     * Better to release all the memory and so on there.
     */
    ws.onclose = function (event) {
         if (event.wasClean){
             alert('Соединение закрыто');
         } else{
             alert('Соединение оборвано по причине: ' + event.reason + ' - код ошибки: '+ event.code );
         }
     };

    // It's clear, I guess
    ws.onerror = function (error) {
         alert('Ошибка - ' + error.data);
     };

    // Works, when server pass data to a client with a preferred transport.
    ws.onmessage = function (event) {
        // Parsing JSON from websocket data.
        var msg = JSON.parse(event.data);
        var json_msg = JSON.parse(msg['ticks']);
        // Setting table block from HTML to variable Table
        var table = document.getElementById("tableID");
        // Deleting all the root and child Elements, such as: td, tr, th and so on.
        while(table.firstChild) table.removeChild( table.firstChild );
        // Setting table header block from HTML to variable tableHead
        // The first row is 5px line. VFX.
        var tableHead = document.createElement('thead');
        table.appendChild(tableHead);
        var tr = document.createElement('tr');
        tr.style.minHeight = "5px";
        tableHead.appendChild(tr);
        // The real header with Exchanges 150px height.
        var th = document.createElement('th');
        th.style.width = "150px";
        tr.appendChild(th);

        // Header cycle. Pushing Exchanges in table-header block. Also define onClick functions.
        inner = 0; // Iteration variable
        for (var name in msg['cnames']) {
            var th = document.createElement('th');
            th.appendChild(document.createTextNode((msg['cnames'])[name]));
            th.style.width = "110px";
            var checkbox = document.createElement("INPUT");
            checkbox.type = "checkbox";
            checkbox.name = 'chck';
            //Saving the checkboxes state
            if (checkBoxState[inner] === true){
                checkbox.checked = true;
            }
            /*
             *  On checkbox click function.
             *  Getting all the checkboxes and changing its state in global array, when it was clicked by user.
             */
            checkbox.onclick = function () {

                var chk = getCheckedBoxes('chck');
                var table = document.getElementById("tableID");
                var tbody = table.getElementsByTagName('tbody')[0];
                //var trow = tbody.getElementsByTagName('tr');
                for (var inty = 0; inty < chk.length; inty++){
                if (chk[inty] === true){
                    checkBoxState[inty] = true;
                } else {
                    checkBoxState[inty] = false;
                    //for (var hCells = 0; hCells < trow.length; hCells++){
                      // var td = trow[hCells].getElementsByTagName('td')[inty];
                     //  td.classList.toggle('');
                    //}
                }
                }
            };
            th.appendChild(checkbox);
            th.onclick = function () {
            // Cropped block. Supportive function to click exchange.
                if (checkbox.disabled === true){
                    alert('Sorry. You cannot choose, until you show all exchanges again.' +
                        ' We are working on this problem')
                }
             };

            inner++;
            tr.appendChild(th);
        }



        var tableBody = document.createElement('tbody');
        table.appendChild(tableBody);

        /* Massive loop-block. Pushes data from server JSON array to our table.
         * Creates blocks, cells and rows dynamically.
         * Throw - into the cell if there are no value for this Exchanger, but the pair exists.
         */
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
                    if ((io[commendme]['PairName'] === (msg['rnames'])[r]) && (io[commendme]['Exchange'] === (msg['cnames'])[c])) {
                        var td = document.createElement('td');
                        var v = io[commendme]['Tick'];
                        if (v !== 0) {
                            td.appendChild(document.createTextNode(fix(v)));
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

        //Search state crutch
        var input = document.getElementById("exchInput");
        var filter = input.value.toUpperCase();
        if (filter !== ''){
            searchFunc()
        }
        //Supportive cycle for the first button. Finds Max&Min, also toggle NOPE color.
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

        //Exch changer state crutch
        for (var checking = 0; checking < checkBoxState.length; checking++){
            if (checkBoxState[checking] === false) {
                continue
            } else{
                forceRefresh();
                break;
            }
        }
        //forceRefresh();

        // Loop, which is used to select style
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

        //Div block scroller
        document.getElementById("scrdiv").addEventListener('scroll', function () {
            this.querySelector("thead").style.transform = "translate(0," + this.scrollTop + "px)";
        }, false);

        //First button. Hides only non-Max&Min rows.
        var btn = document.getElementById("hidebt");
        if (!btn.hasAttribute("onclick")) {
            document.getElementById("hidebt").addEventListener('click', function () {
                table.classList.toggle("hideUninteresting");
                if (this.innerText === "Show less than 3% difference") {
                    this.innerText = "Hide less than 3% difference";
                }
                else {
                    this.innerText = "Show less than 3% difference";
                }
            }, false);
            btn.setAttribute("onclick","true");
        }

        //Second button. Provides Exchange and unimportant pairs hider
        var btn_pair = document.getElementById("pairhider");
        if (!btn_pair.hasAttribute("onclick")) {
            document.getElementById("pairhider").addEventListener('click', function () {
                forceRefresh();
                table.classList.toggle("hidePair");
                var checkbox = document.getElementsByName("chck");
                if (this.innerText === "Show Exchanges") {
                    this.innerText = "Hide Exchanges";
                    for (var ch_state_block = 0; ch_state_block < checkbox.length; ch_state_block++){
                        checkbox[ch_state_block].disabled = false;
                    }
                }
                else {
                    this.innerText = "Show Exchanges";
                    for (var ch_state2_block = 0; ch_state2_block < checkbox.length; ch_state2_block++){
                        checkbox[ch_state2_block].disabled = true;
                    }
                }
            }, false);
            btn_pair.setAttribute("onclick","true");
        }
   };
