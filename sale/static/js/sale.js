
var ROW_NUMBER = 5;

$(document).ready( function () {

    /* set up text box inovice data to datepicker, it popup calendar after click text box */
    $("#txt_SaleDate").datepicker({ 
        dateFormat: 'dd/mm/yy' 
    });
    
    /* When click button calendar, call datepicker show, it popup calendar after click  button */
    $('#btn_SaleDate').click(function() {
        $('#txt_SaleDate').datepicker('show');
    });

    /* Add one row to table (in last row), When click button '+' in header of table */
    $('.table-add').click(function () {
        // Copy hidden row of table and clear hidden class
        var clone = $('#div_table').find('tr.hide').clone(true).removeClass('hide table-line');
        // Append copyed row to body of table, add to last row
        $('#div_table').find('tbody').append(clone);
        // Call re_order_no to set item_no
        re_order_no();
    });

    /* Delete row after click 'X' in last column */
    $('.table-remove').click(function () {
        $(this).parents('tr').detach();         // Delete that table row (TR) and all table data (TD)

        // Check number of row, if number of row < 9 then add one row
        // 9 = default row (5) + header (1) + footer (3)
        if ($('#table_main tr').length <= (ROW_NUMBER + 1 + 3)) {   
            add_last_one_row();
        }
        re_order_no();                          // Call re_order_no to re-order item_no (order_no)
        re_calculate_total_price();             // Call re_calculate_total_price to calculate  total_price, vat, amount_due
    });

    /* Check input on table are corrected format, if not correct use last value */
    $('table').on('focusin', 'td[contenteditable]', function() {
        $(this).data('val', $(this).html());                    // keep value in table before change
    }).on('keypress', 'td[contenteditable]', function (e) {
        if (e.keyCode == 13) {
            return false;
        }
    }).on('focusout', 'td[contenteditable]', function() {
        var prev = $(this).data('val');                         // get last keep value in table after change
        var data = $(this).html();                              // get changed value
        if (!numberRegex.test(data)) {                          // check changed value correct format Ex 1,000.00
            $(this).text(prev);                                 // if format not correct use last keep value
        } else {
            $(this).data('val', $(this).html());                // if format correct keep this value are last value
        }
        re_calculate_total_price();                             // Call re_calculate_total_price to calculate  total_price, vat, amount_due
    });

    /* Get Customer Name when type in text box customer code */
    $('#txt_CustomerCode').change (function () {
        var customer_code = $(this).val().trim();       // get customer_code from text box

        $.ajax({                                        // call backend /customer/detail/<customer_code>
            url:  '/customer/detail/' + customer_code,
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                if (data.customers.length > 0) {        // check data not empty customer
                    $('#txt_CustomerCode').val(data.customers[0].customer_code);    // put to text box
                    $('#txt_CustomerName').val(data.customers[0].name);             // put to text box (label)
                } else {
                    $('#txt_CustomerName').val('');    // if can't find customer_name, reset text box
                }
            },
            error: function (xhr, status, error) {
                $('#txt_CustomerName').val('');         // if something error, reset text box
            }
        });
    });

    /* Load customer list to Modal and show popup */
    /* when click button magnifying glass after Customer Code */
    $('.search_customer_code').click(function () {
        $.ajax({
            url:  '/customer/list',                     // call backend /customer/list
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.customers.forEach(customer => {    // loop each result of customers to create table rows
                    rows += `
                    <tr>
                        <td>${i++}</td>
                        <td><a class='a_click' href='#'>${customer.customer_code}</a></td>
                        <td>${customer.name}</td>
                        <td></td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);   // set new table rows to table body (tbody) of popup

                $('#model_header_1').text('Customer Code');     // set header of popup
                $('#model_header_2').text('Customer Name');
                $('#model_header_3').text('Note');

                $('#txt_modal_param').val('customer_code');     // mark customer_code for check after close modal
                $('#modal_form').modal();                       // open popup (modal)
            },
        });        
    });

    /* search product code, load product list to Modal and show popup */
    /* when click button magnifying glass after Product Code in table */
    $('.search_product_code').click(function () {
        $(this).parents('tr').find('.order_no').html('*');  // mark row number with '*' for return value after close modal

        $.ajax({                                        // call backend /product/list
            url:  '/product/list',
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.products.forEach(product => {       // loop each result of products to create table rows
                    rows += `
                    <tr>
                        <td>${i++}</td>
                        <td><a class='a_click' href='#'>${product.code}</a></td>
                        <td>${product.name}</td>
                        <td>${formatNumber(product.units)}</td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);       // set new table rows to table body (tbody) of popup

                $('#model_header_1').text('Product Code');      // set header of popup
                $('#model_header_2').text('Product Name');
                $('#model_header_3').text('Unit Price');
                
                $('#txt_modal_param').val('product_code');      // mark product_code for check after close modal
                $('#modal_form').modal();                       // open popup
            },
        });
    });
    $('#txt_PaymentMethod').change (function () {
        var payment_method = $(this).val().trim();       // get payment_method from text box

        $.ajax({                                        // call backend /payment_method/detail/<payment_method>
            url:  '/payment_method/detail/' + payment_method,
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                if (data.payment_methods.length > 0) {        // check data not empty customer
                    $('#txt_PaymentMethod').val(data.payment_methods[0].payment_method);    // put to text box
                    $('#txt_Description').val(data.payment_methods[0].description);             // put to text box (label)
                } else {
                    $('#txt_Description').val('');    // if can't find customer_name, reset text box
                }
            },
            error: function (xhr, status, error) {
                $('#txt__Description').val('');         // if something error, reset text box
            }
        });
    });    

        /* Load ของ ตัว payment_method list to Modal and show popup */
    /* when click button magnifying glass after Payment Method */
    $('.search_payment_method').click(function () {
        $.ajax({
            url:  '/payment_method/list',                     // call backend /payment_method/list
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.payment_methods.forEach(payment_method=> {    // loop each result of payment_method to create table rows
                    rows += `
                    <tr>
                        <td>${i++}</td>
                        <td><a class='a_click' href='#'>${payment_method.payment_method}</a></td>
                        <td>${payment_method.description}</td>
                        <td></td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);   // set new table rows to table body (tbody) of popup

                $('#model_header_1').text('Payment Method');     // set header of popup
                $('#model_header_2').text('Description');
                $('#model_header_3').text('Note');

                $('#txt_modal_param').val('payment_method');     // mark payment_method for check after close modal
                $('#modal_form').modal();                       // open popup (modal)
            },
        });        
    });

    // After click link in Model (popup), Return value of product_code, customer_code, sale_no to main form
    $('body').on('click', 'a.a_click', function() {
        var code = $(this).parents('tr').find('td:nth-child(2)').children().html();
        var name = $(this).parents('tr').find('td:nth-child(3)').html();
        var note = $(this).parents('tr').find('td:nth-child(4)').html();
        var option = $(this).parents('tr').find('td:nth-child(5)').html();
        var option2 = $(this).parents('tr').find('td:nth-child(6)').html();
        if ($('#txt_modal_param').val() == 'product_code') {
            // Loop each in data table
            $("#table_main tbody tr").each(function() {
                // Return data in row number = * (jquery mark * before popup (modal) )
                if ($(this).find('.order_no').html() == '*') {
                    // return selected product detail (code,name,units) to table row
                    $(this).find('.project_code_1 > span').html(code);
                    $(this).find('.product_name').html(name);
                    $(this).find('.unit_price').html(note);
                    $(this).find('.quantity').html("1");           // default quantiy is '1'
                }
            });
            
            re_calculate_total_price();
        } else if ($('#txt_modal_param').val() == 'customer_code') {
            $('#txt_CustomerCode').val(code);
            $('#txt_CustomerName').val(name);
        } else if ($('#txt_modal_param').val() == 'sale_no') {
            $('#txt_SaleNo').val(code);
            $('#txt_SaleDate').val(name);
            $('#txt_CustomerCode').val(note);
            $('#txt_CustomerCode').change();
            $('#txt_PaymentMethod').val(option);
            $('#txt_PaymentMethod').change();
            get_sale_detail(code);
        } else if ($('#txt_modal_param').val() == 'payment_method') {
            $('#txt_PaymentMethod').val(code);
            $('#txt_Description').val(name);
            
        }

        $('#modal_form').modal('toggle');               // close modal
    });

    // detect modal form closed, call re_order_no
    $('#modal_form').on('hidden.bs.modal', function () {
        re_order_no();
    });

    /* Click button 'NEW', reset form */
    $('#btnNew').click(function () {
        reset_form();
    });


    /* Click button 'EDIT', load sale list to modal */
    $('#btnEdit').click(function () {
        $.ajax({                                        // call backend /sale/list
            url:  '/sale/list',
            type:  'get',
            dataType:  'json',
            success: function  (data) {
                let rows =  '';
                var i = 1;
                data.sales.forEach(sale => {      // loop each result of sales to create table rows
                    var sale_date = sale.date;
                    // Change format date from 01-12-2022 -> 01/12/2022
                    sale_date = sale_date.slice(0,10).split('-').reverse().join('/');
                    rows += `
                    <tr>
                        <td>${i++}</td>
                        <td><a class='a_click' href='#'>${sale.sale_no}</a></td>
                        <td>${sale_date}</td>
                        <td>${sale.customer_code_id}</td>
                        <td class='hide'></td>
                    </tr>`;
                });
                $('#table_modal > tbody').html(rows);      // set new table rows to table body (tbody) of popup

                $('#model_header_1').text('Sale No');    // set header of popup
                $('#model_header_2').text('Sale Date');
                $('#model_header_3').text('Customer Code');

                $('#txt_modal_param').val('sale_no');    // mark sale_no for check after close modal
                $('#modal_form').modal();                   // open popup
            },
        });        
    });

    /* Click button 'SAVE', call /sale/create or /sale/update */
    $('#btnSave').click(function () {
        var customer_code = $('#txt_CustomerName').val().trim();    // get customer_code from text box
        if (customer_code == '') {                                  // check customer_code is empty
            alert('กรุณาระบุ Customer');
            $('#txt_CustomerCode').focus();
            return false;
        }
        var sale_date = $('#txt_SaleDate').val().trim();      // get sale data from text box
        if (!dateRegex.test(sale_date)) {                        // check sale data is correct format DD/MM/YYYY
            alert('กรุณาระบุวันที่ ให้ถูกต้อง');
            $('#txt_SaleDate').focus();
            return false;
        }
        var payment_method_code = $('#txt_PaymentMethod').val().trim();
        if (payment_method_code == '') {
            alert('กรุณาระบุ Payment Method');
            $('#txt_PaymentMethod').focus();
            return false;
        }
        if ($('#txt_SaleNo').val() == '<new>') {                 // check sale no in form, if sale no = <new> then call create otherwise call update
            var token = $('[name=csrfmiddlewaretoken]').val();      // get django security code
                  
            $.ajax({                                                // call backend /sale/create
                url:  '/sale/create',
                type:  'post',
                data: $('#form_sale').serialize() + "&lineitem=" +lineitem_to_json(),
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    if (data.error) {                               // if backend return error message, log it
                        console.log(data.error);
                        alert('การบันทึกล้มเหลว');
                    } else {
                        $('#txt_SaleNo').val(data.sale.sale_no)    // SAVE success, show new sale no
                        alert('บันทึกสำเร็จ');
                    }                    
                },
            });  
        } else {
            var token = $('[name=csrfmiddlewaretoken]').val();      // get django security code

            $.ajax({                                                // call backend /sale/update
                url:  '/sale/update',
                type:  'post',
                data: $('#form_sale').serialize() + "&lineitem=" +lineitem_to_json() + "&sale_no=" + $('#txt_SaleNo').val(),
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    if (data.error) {                           // if backend return error message, log it
                        console.log(data.error);
                        alert('การบันทึกล้มเหลว');
                    } else {            
                        alert('บันทึกสำเร็จ');                      // SAVE success, show popup message
                    }
                },
            }); 
        }
    });

    /* Click button 'DELETE', call backend /sale/delete */
    $('#btnDelete').click(function () {
        if ($('#txt_SaleNo').val() == '<new>') {
            alert ('ไม่สามารถลบ Sale ใหม่ได้');
            return false;
        }
        if (confirm ("คุณต้องการลบ Sale No : '" + $('#txt_SaleNo').val() + "' ")) {
            console.log('Delete ' + $('#txt_SaleNo').val());
            var token = $('[name=csrfmiddlewaretoken]').val();          // get django security code
            $.ajax({                                                    // call backend /sale/delete
                url:  '/sale/delete',
                data: 'sale_no=' + $('#txt_SaleNo').val(),
                type:  'post',
                headers: { "X-CSRFToken": token },
                dataType:  'json',
                success: function  (data) {
                    reset_form();                                       // after delete success call reset_form
                },
            });            
        }
    });

    /* Click button 'PRINT', open new tab of browser with /sale/reprot/<invpoce_no> */
    $('#btnPrint').click(function () {
        if ($('#txt_SaleNo').val() == '<new>') {
            return false;
        }
        window.open('/sale/report/' + $('#txt_SaleNo').val());
    });

    /* Start from */
    reset_form ();
});

/* read all data inside table and convert to json string */
/* return json string of line item (all data inside table) */
function lineitem_to_json () {
    var rows = [];                                                  // create empty array 'rows'
    var i = 0;
    $("#table_main tbody tr").each(function(index) {                // loop each table data
        if ($(this).find('.project_code_1 > span').html() != '') {  // check row have data
            rows[i] = {};                                           // create empty object in rows[index]
            rows[i]["item_no"] = (i+1);                             // copy data from table row to variable 'rows'
            rows[i]["product_code"] = $(this).find('.project_code_1 > span').html();
            rows[i]["product_name"] = $(this).find('.product_name').html();
            rows[i]["unit_price"] = $(this).find('.unit_price').html();
            rows[i]["quantity"] = $(this).find('.quantity').html();
            rows[i]["extended_price"] = $(this).find('.extended_price').html();
            i++;
        }
    });
    var obj = {};                                                   // create empty object
    obj.lineitem = rows;                                            // assign 'rows' to object.lineitem
    //console.log(JSON.stringify(obj));

    return JSON.stringify(obj);                                     // return object in JSON format
}

/* get sale detail from backend with sale_no and fill to the form */
function get_sale_detail (sale_no) {
    $.ajax({                                                            // call backend /sale/detail/IN100/22
        url:  '/sale/detail/' + encodeURIComponent(sale_no),
        type:  'get',
        dataType:  'json',
        success: function  (data) {
            console.log(data);

            reset_table();                                              // reset table
            for(var i=ROW_NUMBER;i<data.salelineitem.length;i++) {   // generate row by number of result
                add_last_one_row();
            }
            var i = 0;
            $("#table_main tbody tr").each(function() {                 // fill result data to each row
                if (i < data.salelineitem.length) {
                    $(this).find('.project_code_1 > span').html(data.salelineitem[i].product_code);
                    $(this).find('.product_name').html(data.salelineitem[i].product_code__name);
                    $(this).find('.unit_price').html(data.salelineitem[i].unit_price);
                    $(this).find('.quantity').html(data.salelineitem[i].quantity);
                }
                i++;
            });
            re_calculate_total_price();                                 // re-calculate total_price, vat, amount due
        },
    });
}

/* Loop each data table and calculate extended_price, total_price, vat, amount due */
function re_calculate_total_price () {
    var total_price = 0;

    // Loop each in Data Table
    $("#table_main tbody tr").each(function() {
        //get product_code from Table Row in Table
        var product_code = $(this).find('.project_code_1 > span').html().trim();
        //console.log (product_code);
        if (product_code != '') {
            var unit_price = $(this).find('.unit_price').html().replace(/,/g, '');
            $(this).find('.unit_price').html(formatNumber((unit_price)));
            var quantity = $(this).find('.quantity').html();
            $(this).find('.quantity').html(parseInt(quantity));
        
            var extended_price = unit_price * quantity;
            $(this).find('.extended_price').html(formatNumber(extended_price));
            total_price += extended_price;
        }
    });

    $('#lbl_TotalPrice').text(formatNumber(total_price));
    $('#txt_TotalPrice').val($('#lbl_TotalPrice').text());
}

/* Reset form to original form */
function reset_form() {
    $('#txt_SaleNo').attr("disabled", "disabled");
    $('#txt_SaleNo').val('<new>');

    reset_table();
    
    $('#txt_SaleDate').val(new Date().toJSON().slice(0,10).split('-').reverse().join('/'));

    $('#txt_CustomerCode').val('');
    $('#txt_CustomerName').val('');
    $('#txt_PaymentMethod').val('');
    $('#txt_Description').val('');
    $('#lbl_TotalPrice').text('0.00');
}

/* Reset Table to original from */
function reset_table() {
    $('#table_main > tbody').html('');          // Clear body of table (tbody), table will remain header and footer
    for(var i=1; i<= ROW_NUMBER; i++) {         // Loop 5 times
        add_last_one_row()                      // Add one row to table
    }    
}

/* Add one row to table */
function add_last_one_row () {
    $('.table-add').click();                    // Call event click of button '+' in header of table, for add one row
}

/* Reorder number item_no (order_no) on table */
function re_order_no () {
    var order_number = 1;
    // Loop each data table
    $("#table_main tbody tr").each(function() {         
        // set order number to column order_no
        $(this).find('.order_no').html(order_number);   
        order_number++;
    });
}

/* Format input to display number 2 floating point Ex 1,000.00 */
function formatNumber (num) {
    if (num === '') return '';
    num = parseFloat(num); 
    return num.toFixed(2).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,");
}

/* Check n is integer */
function isInt(n){
    return Number(n) === n && n % 1 === 0;
}

/* Check n is floating point */
function isFloat(n){
    return Number(n) === n && n % 1 !== 0;
}

/* Pattern for check input is Date format DD/MM/YYYY */
var dateRegex = /^(?=\d)(?:(?:31(?!.(?:0?[2469]|11))|(?:30|29)(?!.0?2)|29(?=.0?2.(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00)))(?:\x20|$))|(?:2[0-8]|1\d|0?[1-9]))([-.\/])(?:1[012]|0?[1-9])\1(?:1[6-9]|[2-9]\d)?\d\d(?:(?=\x20\d)\x20|$))?(((0?[1-9]|1[012])(:[0-5]\d){0,2}(\x20[AP]M))|([01]\d|2[0-3])(:[0-5]\d){1,2})?$/;
//var numberRegex = /^-?\d+\.?\d*$/;

/* Pattern for check input is Money format 1,000.00 */
var numberRegex = /^-?\d*\.?\d*$/

// A few jQuery helpers for exporting only
jQuery.fn.pop = [].pop;
jQuery.fn.shift = [].shift;

