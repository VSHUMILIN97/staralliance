var ws = new WebSocket("ws://" + window.location.hostname + ":8070/");

ws.onopen = function (event) {
    ws.send(location.pathname);
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
    var art = JSON.parse(event.data);
    var json_msg = JSON.parse(art['tick']);
    var ohlcD = JSON.parse(art['ohlc']);
    var hsell = JSON.parse(art['hsell']);
    var hbuy = JSON.parse(art['hbuy']);
$.getJSON('https://jsonplaceholder.typicode.com/posts', function (data) {
//я В ДУШЕ не знаю ПОЧЕМУ он не работает без обращения за jsonом здесь, НО РАБОТАЕТ на фидле
//(нет, я знаю, как заставить его работать и без обращения, но тогда падает цветовая схема)
//возможно, когда-нибудь у нас будет своя страница, с которой можно будет взять json для графиков,
//поэтому давайте дружно сделаем вид, что эта ссылка - временная и стоит здесь как укор совести для того, чтобы не забыть об этом
//upd. теоретически, можно таскать данные и напрямую с бирж, если по пути избавиться от всего лишнего что они предоставляют
//и выделить только нужное (у меня на это не хватает мозгов)
        var ohlc = [],
        volBuy = [],
        volSell = [],

        groupingUnits = [[
            'hour',
            [1,3,6,12]
        ], [
            'day',
            [1,3,5,10]
        ], [
            'week',
            [1,2]
        ], [
            'month',
            [1, 2, 3, 4, 6]
        ]],

        i = 0;

    for (var oc in ohlcD){
        ohlc.push([
            ohlcD[oc]['TimeStamp']['$date'],
            ohlcD[oc]['Open'],
            ohlcD[oc]['High'], // Ввести FIX'en помощь. См compare. Функция fix
            ohlcD[oc]['Low'],
            ohlcD[oc]['Close']
        ]);
    }

    for (var vb in hbuy){
        volBuy.push([
            ohlcD[vb]['TimeStamp']['$date'],
            hbuy[vb]['Quantity']
        ]);
    }
    for (var vs in hsell){
        volSell.push([
            ohlcD[vs]['TimeStamp']['$date'],
            hsell[vs]['Quantity']
        ]);
    }


    Highcharts.stockChart('OHLCContainer', {
    		rangeSelector: {
            selected: 1,
            buttons: [{
            type: 'hour',
            count: 1,
            text: '1h'
            }, {
            type: 'day',
            count: 1,
            text: '1d'
            }, {
            type: 'week',
            count: 1,
            text: '1w'
            }, {
            type: 'month',
            count: 1,
            text: '1m'
            }, {
            type: 'month',
            count: 6,
            text: '6m'
            }, {
            type: 'year',
            count: 1,
            text: '1y'
            }, {
            type: 'all',
            text: 'All'
            }]
        },

        chart: {
            zoomType: 'x',
            events: {
    			load: function () {
      			this.pointCount = 1;
      		    },
    			redraw: function () {
      			this.pointCount = 1;
      		    }
    		},
        selectionMarkerFill: 'rgba(230, 220, 204, .3)'
        },

        title: {
            text: 'График свечек и объемов ' + art['pair'] +  ' для биржи ' + art['exchange']
        },

        yAxis: [{
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: 'Свечки'
            },
            height: '60%',
            lineWidth: 2,
            resize: {
                enabled: true
            }
        }, {
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: 'Объемы'
            },
            top: '65%',
            height: '35%',
            offset: 0,
            lineWidth: 2
        }],
		plotOptions: {
            column: {
                grouping: false,
                shadow: false,
                borderWidth: 0.5,
            }
    	},
        tooltip: {
            shared: true,
            useHTML: true,
            headerFormat: '<span>{point.key}</span>'
        },

        series: [{
            type: 'candlestick',
            name: art['pair'] + ' OHLC',
            data: ohlc,
            dataGrouping: {
                units: groupingUnits
            },
            tooltip: {
                valueDecimals: 8
            },
        }, {
            type: 'column',
            name: 'Покупка',
            data: volBuy,
            yAxis: 1,
            color: 'rgba(113, 218, 113, .7)',
            dataGrouping: {
                units: groupingUnits
            },
            tooltip: {
                valueDecimals: 8
            },
        },
        {
            type: 'column',
            name: 'Продажа',
            data: volSell,
            yAxis: 1,
            color: 'rgba(245, 112, 112, .9)',
            pointPadding: 0.3,
            dataGrouping: {
                units: groupingUnits
            },
            tooltip: {
                valueDecimals: 8
            },
        }]
    });
});

$.getJSON('https://www.highcharts.com/samples/data/jsonp.php?filename=usdeur.json&callback=?', function (data) {



    var ticks = [];
    //var art = JSON.parse(event.data);
    //var json_msg = JSON.parse(art['tick']);
    for (var item in json_msg){
        if (json_msg[item]['Tick'] !== 0){
            ticks.push([(json_msg[item]['TimeStamp']['$date']), json_msg[item]['Tick']]);
        } else {
            ticks.push([(json_msg[item]['TimeStamp']['$date']), null]);
        }

    }


    Highcharts.stockChart('tickContainer', {
    		rangeSelector: {
            selected: 1,
            buttons: [{
            type: 'hour',
            count: 1,
            text: '1h'
            }, {
            type: 'day',
            count: 1,
            text: '1d'
            }, {
            type: 'week',
            count: 1,
            text: '1w'
            }, {
            type: 'month',
            count: 1,
            text: '1m'
            }, {
            type: 'month',
            count: 6,
            text: '6m'
            }, {
            type: 'year',
            count: 1,
            text: '1y'
            }, {
            type: 'all',
            text: 'All'
            }]
        },

        chart: {
            zoomType: 'x',
            events: {
    			load: function () {
      			this.pointCount = 1;
      		    },
    			redraw: function () {
      			this.pointCount = 1;
      		    }
    		},
        selectionMarkerFill: 'rgba(230, 220, 204, .3)'
        },

        title: {
            text: 'График тика ' + art['pair'] + ' для биржи ' + art['exchange']
        },

        plotOptions: {
            series: {
                states: {
                    hover: {
                        halo: {
                            size: 6,
                            attributes: {
                                fill: 'rgb(54, 54, 54)'
                            }
                        },
                        lineWidth: 1
                    }
                },
                marker: {
                    fillColor: 'rgb(54, 54, 54)'
                },
            },
        },

        series: [{
            name: art['pair'],
            data: ticks,
            type: 'spline',
            connectNulls: true,
            tooltip: {
                valueDecimals: 8,
                useHTML: true,
                headerFormat: '<span>{point.key}</span>'
            },
            lineColor: 'rgb(54,54,54)'
            }]
        });
});
};



Highcharts.theme = {
   colors: ['#f35858', '#8085e9', '#8d4654', '#7798BF', '#aaeeee',
      '#ff0066', '#eeaaee', '#55BF3B', '#DF5353', '#7798BF', '#aaeeee'],
   chart: {
      backgroundColor: null,
      style: {
         fontFamily: 'Century Gothic, sans-serif'
      }
   },
   title: {
      style: {
         color: 'black',
         fontSize: '18px',
         fontWeight: 'bold'
      }
   },
   subtitle: {
      style: {
         color: 'black'
      }
   },
   tooltip: {
      borderWidth: 0.5,
      borderColor: '#3a3a3a'
   },

   plotOptions: {
      candlestick: {
      	upColor: '#33cc33',
        lineColor: '#3a3a3a',
        lineWidth: 0.5,
        animation: {
            duration: 500
        }
      },
      column: {
      	 borderColor: '#4a4a4a',
         animation: {
            duration: 500
         }
      },
      spline: {
         animation: {
            duration: 500
         }
      },
   },

   legend: {
      itemStyle: {
         fontWeight: 'bold',
         fontSize: '13px'
      }
   },
   xAxis: {
      labels: {
         style: {
            color: '#6e6e70'
         }
      },
      minRange: 3600 * 1000
   },
   yAxis: {
      labels: {
         style: {
            color: '#6e6e70'
         }
      }
   },

   // Highstock specific
   navigator: {
      xAxis: {
         gridLineColor: '#D0D0D8'
      },
      series: {
         color: '#aaaaaa',
         lineWidth: 1
      },
      maskFill: 'rgba(230, 220, 204, .5)'
   },
   rangeSelector: {
      buttonTheme: {
         fill: 'white',
         stroke: '#C0C0C8',
         'stroke-width': 1,
         states: {
            select: {
               fill: '#D0D0D8'
            }
         }
      }
   },
   scrollbar: {
      trackBorderColor: '#C0C0C8'
   },

   // General
   background2: '#E0E0E8'

};

Highcharts.setOptions(Highcharts.theme);

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
      $('.nothing').css('color', 'rgb(74, 54, 14)');
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
        var redirect = $(location).attr('href').replace('{{ exchange }}/','').replace('{{ pair }}/','');
        window.location.href = redirect+$('#exchSelector').val()+'/'+$('#pairSelector').val();
        window.host.refresh();
        ws.send($('#exchSelector').val()+' '+$('#pairSelector').val())
    }
    else
    {
        $('.nothing').text('Сочетание не выбрано');
        $('.nothing').css('color', 'rgb(54, 54, 54)');
    }
});
 
