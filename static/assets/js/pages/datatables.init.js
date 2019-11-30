$(document).ready(function(){$("#datatable").DataTable();var a=$("#datatable-buttons").DataTable({lengthChange:!1,buttons:["copy","excel","pdf"]});$("#key-table").DataTable({keys:!0}),$("#responsive-datatable").DataTable(),$("#selection-datatable").DataTable({select:{style:"multi"}}),a.buttons().container().appendTo("#datatable-buttons_wrapper .col-md-6:eq(0)")});


$(document).ready(function() {
  $('#selection-datatable1').DataTable( {
    dom: "Blfrtip",
    lengthMenu: [
    [ 5, 10, 20, -1 ],
    [ '5 rows', '10 rows', '20 rows', 'All' ]
    ],
    buttons: [
    'copy',
    'csv',
    'excel',
    'pdf',
    'pageLength',
    {
        extend: 'print',
        text: 'Print all',
        exportOptions: {
            modifier: {
                selected: null
            }
        }
    },
    {
        extend: 'print',
        text: 'Print selected'
    }
    ],
    select:{
        style:"multi",
    },

} );
} );