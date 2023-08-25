$(document).ready(function() {
  $("#leftside-navigation .sub-menu > a").click(function(e) {
    $("#leftside-navigation ul ul").slideUp();
    if (!$(this).next().is(":visible")) {
      $(this).next().slideDown();
    }
    e.stopPropagation();
  });
});


function searchTable() {
  var input, filter, table, tr, td, i, j, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.querySelector("table");
  tr = table.getElementsByTagName("tr");

  for (i = 0; i < tr.length; i++) {
      tds = tr[i].getElementsByTagName("td");
      for (j = 0; j < tds.length; j++) {
          td = tds[j];
          if (td) {
              txtValue = td.textContent || td.innerText;
              if (txtValue.toUpperCase().indexOf(filter) > -1) {
                  tr[i].style.display = "";
                  break;
              } else {
                  tr[i].style.display = "none";
              }
          }
      }
  }
}

var sortDirections = {};

function sortTable(colIndex) {
  var table, rows, switching, i, x, y, shouldSwitch;
  table = document.querySelector("table");
  switching = true;

  var currentDirection = sortDirections[colIndex] || 'asc';
  var newDirection = currentDirection === 'asc' ? 'desc' : 'asc';
  sortDirections[colIndex] = newDirection;


  while (switching) {
      switching = false;
      rows = table.getElementsByTagName("tr");

      for (i = 1; i < (rows.length - 1); i++) {
          shouldSwitch = false;

          x = rows[i].getElementsByTagName("td")[colIndex];
          y = rows[i + 1].getElementsByTagName("td")[colIndex];

          var xValue = x.innerHTML.toLowerCase();
          var yValue = y.innerHTML.toLowerCase();

          if (currentDirection === 'asc') {
              if (xValue > yValue) {
                  shouldSwitch = true;
                  break;
              }
          } else if (currentDirection === 'desc') {
              if (xValue < yValue) {
                  shouldSwitch = true;
                  break;
              }
          }
      }

      if (shouldSwitch) {
          rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
          switching = true;
      }
  }
}