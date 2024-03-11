const Cite = require('citation-js')

function toggleSpinner() {
  const spinner = $("#loadingSymbol");
  if (spinner.css('opacity') == 0) {
    spinner.css("opacity", 1);
  } else {
    spinner.css("opacity", 0);
  }
}

async function readFileContents(e) {
  toggleSpinner()

  // fetch the upload file
  const file = e.target.files.item(0)

  // read the file contents
  const content = await file.text();

  // process the file contents using citation.js
  const citation = await Cite.async(content)

  // use the citation object to produce a preview and update data field
  processCitationObject(citation)

  toggleSpinner()
}

async function fetchCitation(e) {
  toggleSpinner();

  // get search term from text input
  const $input = $(e.target);
  const $row = $input.closest(".dj-form-errors");
  const $errors = $row.children('.errorlist');

  try {
    // ansynchronously find citation using citation.js
    const citation = await Cite.async($input.val())

    // use the citation object to produce a preview and update data field
    processCitationObject(citation)

    // remove any errors from previous searches
    $row.removeClass('errors');
    $errors.empty()

  }

  catch (error) {
    // add some informative UI messages for user
    $row.addClass('errors');
    $errors.append("<li>The requested resource could not be found.</li>");
    $('form :input[type="submit"]').prop('disabled', true);
    $("#citationPreview>.inner").html(error)
    console.error(error);
  }

  toggleSpinner();
};

function processCitationObject(citation) {
  // update the preview box with formatted citation
  $("#citationPreview>.inner").html(
    citation.format('bibliography', {
      format: 'html',
      template: 'apa',
    })
  )

  // update the hidden text area input with the csl-json string
  // $("#id_CSL").val(citation.format('data'))
  $('input[name="CSL"]').val(citation.format('data'))
  // enable save button
  $('form :input[type="submit"]').prop('disabled', false);
}

// $("#id_file").on("change", readFileContents);
