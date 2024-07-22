function fixUpIds(fieldGroup) {
  fieldGroup.find('.attributes-pair').each(function (idx, value) {
    $(value).find('.attributes-key').attr('id', 'field-key-row-' + idx)
      .siblings('label').attr('for', 'field-key-row-' + idx)
    $(value).find('.attributes-value').attr('id', 'field-value-row-' + idx)
      .siblings('label').attr('for', 'field-value-row-' + idx)
  })
}

$(function () {
  $('.djangocms-attributes-field').each(function () {
    var that = $(this)

    if (that.data('isAttributesFieldInitialized')) {
      return
    }

    that.data('isAttributesFieldInitialized', true)

    var emptyRow = that.find('.template')
    var btnAdd = that.find('.add-attributes-pair')
    var btnDelete = that.find('.delete-attributes-pair')

    btnAdd.on('click', function (event) {
      event.preventDefault()
      emptyRow.before(emptyRow.find('.attributes-pair').clone())
      fixUpIds(that)
    })

    that.on('click', '.delete-attributes-pair', function (event) {
      event.preventDefault()
      var removeButton = $(this)
      removeButton.closest('.attributes-pair').remove()
      fixUpIds(that)
    })

    fixUpIds(that)
  })
})