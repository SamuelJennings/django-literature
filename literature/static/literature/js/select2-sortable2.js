$(document).ready(function () {

    // Make selected items sortable
    $('#id_author').on('select2:select', function () {
      makeSortable()
    })

    // Function to make the selected items sortable
    function makeSortable() {
      var $choices = $('.select2-selection__choice').parent();
      $choices.sortable({
        tolerance: 'pointer',
        stop: function(event, ui) {
          // Get the new order of selected items
          var order = $(this).children('.select2-selection__choice').map(function() {
            return $(this).data().select2Id;
          }).get();

          // Update the Select2 selection
          var $select = $('#id_author');
        //   $select.val(order).trigger('change');
          $select.val(order).trigger('change');

          // Update the underlying <select> options order
        //   var $options = $select.find('option');
        //   $options.sort(function(a, b) {
        //     return order.indexOf(a.value) - order.indexOf(b.value);
        //   });
        //   $select.append($options);
        }
      }).disableSelection();
    }

    // Initialize sortable after the first item is selected
    if ($('#id_author').val().length > 0) {
      makeSortable()
    }
  });
