var exchs = document.getElementById("exchSelector");
{% for item in exchList %}
  var opt = document.createElement("option");
  opt.innerText = '{{ item }}';
  opt.style.textAlign = "left";
  exchs.appendChild(opt);
{% endfor %}

var update_pairs = function () {
    var success = false;
    $('#pairSelector').empty();
    $('.nothing').css('color', 'transparent');
    var pairs = document.getElementById("pairSelector");
    {% for item in combinations %}
        if ('{{ item.Exch }}' == $('#exchSelector').val()) {
          var opt = document.createElement("option");
          opt.innerText = '{{ item.Pair }}';
          opt.style.textAlign = "left";
          pairs.appendChild(opt);
          success = true;
        }
    {% endfor %}
    if (success == false) {
      $('.nothing').css('color', 'rgb(54, 54, 54)');
      $('.nothing').text('Похоже, для этой биржи ничего нет');
      $('#pairSelector').prop('disabled', true);
    }
    else {
      $('#pairSelector').prop('disabled', false);
    }
    $('#pairSelector').selectpicker('refresh');
};

$("#exchSelector").change(update_pairs);
$("#pairSelector").change( function () { $('.nothing').css('color', 'transparent'); } );


$('#okBtn').click( function() {
    if ($('#exchSelector').val().length && $('#pairSelector').val().length) {
        $('.nothing').css('color', 'transparent');
        window.location.href = $(location).attr('href')+$('#exchSelector').val()+'/'+$('#pairSelector').val();

    }
    else
    {
        $('.nothing').text('Сочетание не выбрано');
        $('.nothing').css('color', 'rgb(54, 54, 54)');
    }
});
