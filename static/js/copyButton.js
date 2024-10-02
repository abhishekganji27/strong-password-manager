var table = document.getElementById("table");
var row_cnt = table.rows.length;
var col_cnt = table.rows[0].cells.length;
for(var i=1; i<row_cnt; i++) {
    for(var j=0; j<col_cnt; j++) {

        table.rows[i].cells[j].onclick = function() {
            
            navigator.clipboard.writeText(this.innerText)
                    // .then(() => alert("Copied to clipboard"))
    }

    }
}    