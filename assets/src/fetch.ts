import { Cite } from '@citation-js/core'
import $ from 'jquery'

$(function() {
  $("#id_search").on('change', async function (e) {
    
    // fetch the upload file
    const searchText = $(this).val();

    const $hiddenText = $('input[name="text"]')

    const $preview = $('#citationPreview')

    const $submit = $('form :input[type="submit"]')
    try {
      // Initialize a Cite instance with the search text
      const cite = new Cite(searchText);

      // update the hidden text area input with the csl-json string
      $hiddenText.val(cite.format('data'))

      // add a preview below the form
      $preview.html(cite.format('bibliography', {
        format: 'html',
        template: 'apa',
      }))



      // enable confirm import button
      $submit.prop('disabled', false);


    } catch (error) {
      console.error('Error processing citation:', error);
      $hiddenText.val('');
      $preview.html("Sorry, we couldn't find that reference. Please check the value and try again.");
      $submit.prop('disabled', true);
    }





  })
})
