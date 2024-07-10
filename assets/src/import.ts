import { Cite } from '@citation-js/core'
import $ from 'jquery'

$(function() {
  $("#id_upload").on('change', async function (e) {

    // fetch the upload file
    const file = (e.target as HTMLInputElement).files?.item(0);

    // read the file contents
    const content = await file?.text();
    // process the file contents using citation.js
    const citation = await Cite.async(content);

    // add a preview below the form
    $("#citationPreview").html(citation.format('bibliography', {
      format: 'html',
      template: 'apa',
    }));

    // update the hidden text area input with the csl-json string
    $('input[name="text"]').val(citation.format('data'));

    // enable confirm import button
    $('form :input[type="submit"]').prop('disabled', false);

  })
})
