/* ------------ Event Handlers ------------ */
/** @listens onclick: delete the selected row */
$("#cart_table").on("click", "tr i.remove", function(){
    this.closest("tr").remove();
    basket_total(); // re-compute basket total
})

/** @listens onclick: delete all product rows */
$("#del_all").on("click",function(){
    $("#cart_table > tbody").children().remove();
    basket_total(); // re-compute basket total
})

/**
 * Calls updateLineAmt to provide the line total
 * @listens onchange:  quantity
*/
$("#cart_table").on("change", "tr input.qty", function () {
    updateLineAmt(this);
})

/* ------------ Functions ------------ */
/**
 * Updates the line amount and basket total
 * @param {object} trigger DOM element executing the function, `this`
*/
function updateLineAmt(trigger) {
    var row = $(trigger).closest("tr");
    row.find("td:eq(5)").text(
        parseFloat(row.find("td:eq(3) > input").val() *
            row.find("td:eq(4)").text()).toFixed(2)); // 2d.p
    basket_total(); // update the basket total
}

/** Loops over the entire rows to compute and update the basket total */
function basket_total(){
    var sum = 0;
    var line_amt;
    $(".s_n").each(function(i, elem){$(elem).text(i+1)}); // set the S/N
    $(".line_amt").each(function(){
        line_amt = parseFloat($(this).text())
        if (!isNaN(line_amt)) {
            sum += line_amt;
        }
    });
    if (sum === 0) {
        $('#empty_cart').show();
    } else {
        $('#empty_cart').hide();
    }
    $(".total").text(sum.toLocaleString());
}

/**
 * Generates JSON object from table cart lines id and quantity for all lines
 * with specified quantity
 * @returns {object[]} JSON object representation of table cart lines
 */
function jsonifyCartTable() {
    var table_data = [];
    var line_qty;
    var line_data;
    $("#cart_table>tbody tr").each(function(){
        line_qty = $(this).find(".qty").val();
        if (line_qty > 0){
            line_data={};
            line_data.id = $(this).find("select").val();
            line_data.qty = $(this).find(".qty").val();
            table_data.push(line_data);
        }
    });
    return table_data;
}

$(document).ready(function(){
  $(".line_amt").each(function(){
    updateLineAmt(this);
    })
})