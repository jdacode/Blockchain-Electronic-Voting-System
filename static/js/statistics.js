

function drawVotesColumn(result) {
          var var_color = '#0040ff';
          var winner = [var_color, var_color, var_color, var_color, var_color, var_color];
          var max = -Infinity, argmax = [];
          for(var i=0; i<result.length; ++i)
            if(result[i] > max) max = result[i], argmax = [i];
            else if(result[i] === max) argmax.push(i);
          for (var y in argmax) {
            winner[argmax[y]] = '#00ff00';
          }

          var scale = [];
          var l = Math.max(...result);
          for (var z = 0; z < l; z++) {
            scale.push(z+1);
          }
          var opc = 0.6;

          var data = google.visualization.arrayToDataTable([
            ['Candidate', 'Votes', { role: 'style' } ],
            ['Candidate #1', result[0], 'color:' + winner[0] + '; opacity:' + opc],
            ['Candidate #2', result[1], 'color:' + winner[1] + '; opacity:' + opc],
            ['Candidate #3', result[2], 'color:' + winner[2] + '; opacity:' + opc],
            ['Candidate #4', result[3], 'color:' + winner[3] + '; opacity:' + opc],
            ['Candidate #5', result[4], 'color:' + winner[4] + '; opacity:' + opc],
            ['Candidate #6', result[5], 'color:' + winner[5] + '; opacity:' + opc]
          ]);

          var options = {
            title: 'GENERAL RESULTS:',
            hAxis: {
              title: 'CANDIDATES'
            },
            vAxis: {
              title: 'VOTES [ # ]',
              ticks: scale
            },
            legend: { position: 'bottom', maxLines: 3, alignment: 'start' },
            bar: {groupWidth: "90%"},
            chartArea: {
              left: 'auto',
              top:'auto',
              width:'auto',
              height:'auto'
            },
            legend: {position: 'none'},
            format: 'decimal',
            backgroundColor: {
              fill: '#ffffff',
              fillOpacity: 1,
            },
          };

          var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
          chart.draw(data, options);
    };
    function drawVotesDonut(result) {
          var data = google.visualization.arrayToDataTable([
            ['Candidate', 'Votes'],
            ['Candidate #1', result[0]],
            ['Candidate #2', result[1]],
            ['Candidate #3', result[2]],
            ['Candidate #4', result[3]],
            ['Candidate #5', result[4]],
            ['Candidate #6', result[5]]
          ]);

          var options = {
            title: 'GENERAL RESULTS:',
            pieHole: 1,
            chartArea: {width: '100%'},
            is3D: true,
          };

          var chart = new google.visualization.PieChart(document.getElementById('chart_div2'));
          chart.draw(data, options);
    };


$(window).resize(function(){
      drawVotesColumn();
      drawVotesDonut();
    });