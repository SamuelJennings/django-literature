
const CSL_ALWAYS_SHOW = [
    "type",
    "title",
    "citation_key",
    "show_suggested",
    "keyword",
    "note",
    "custom",
    "language",
    "source",
];


const CSL_PROPS = [
    "abstract",
    "accessed",
    "annote",
    "archive",
    "archive-place",
    "archive_collection",
    "archive_location",
    "author",
    "authority",
    "available-date",
    "call-number",
    "categories",
    "chair",
    "chapter-number",
    "citation-key",
    "citation-label",
    "citation-number",
    "collection-editor",
    "collection-number",
    "collection-title",
    "compiler",
    "composer",
    "container-author",
    "container-title",
    "container-title-short",
    "contributor",
    "curator",
    "custom",
    "dimensions",
    "director",
    "division",
    "DOI",
    "edition",
    "editor",
    "editorial-director",
    "event",
    "event-date",
    "event-place",
    "event-title",
    "executive-producer",
    "first-reference-note-number",
    "genre",
    "guest",
    "host",
    "id",
    "illustrator",
    "interviewer",
    "ISBN",
    "ISSN",
    "issue",
    "issued",
    "journalAbbreviation",
    "jurisdiction",
    "keyword",
    "language",
    "locator",
    "medium",
    "narrator",
    "note",
    "number",
    "number-of-pages",
    "number-of-volumes",
    "organizer",
    "original-author",
    "original-date",
    "original-publisher",
    "original-publisher-place",
    "original-title",
    "page",
    "page-first",
    "part",
    "part-title",
    "performer",
    "PMCID",
    "PMID",
    "printing",
    "producer",
    "publisher",
    "publisher-place",
    "recipient",
    "references",
    "reviewed-author",
    "reviewed-genre",
    "reviewed-title",
    "scale",
    "script-writer",
    "section",
    "series-creator",
    "shortTitle",
    "source",
    "status",
    "submitted",
    "supplement",
    "title",
    "title-short",
    "translator",
    "type",
    "URL",
    "version",
    "volume",
    "volume-title",
    "volume-title-short",
    "year-suffix"
  ]
  
const CSL_TYPES = {
    "article": [
        "author",
        "title",
        "title-short",
        "container", 
        "container-title-short",
        "issue",
        "number",
        "page",
        "publisher-place",
        "edition",
        "issued",
        "collection-number",
        "collection-title",
        "section",
        "status",
        "supplement-number",
        "volume", 
        "volume-title",
    ],
    "article-journal": [
        "author",
        "title",
        "container",
        "volume",
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "article-magazine": [
        "author",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "article-newspaper": [
        "author",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "bill": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "book": [
        "author",
        "collection_editor",
        "title",
        "publisher",
        "publisher-place",
        "volume", 
        "edition",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "broadcast": [
        "title",
        "event-date",
        "medium",
        "URL",
    ],
    "chapter": [
        "author",
        "title",
        "container", 
        "volume", 
        "page",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "classic": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "volume", 
        "edition",
        "issued",
        "ISBN",
        "URL",
    ],
    "collection": [
        "editor",
        "collection_editor",
        "title",
        "publisher",
        "publisher-place",
        "volume", 
        "edition",
        "issued",
        "ISBN",
        "URL",
    ],
    "dataset": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "URL",
        "compiler",
        "license",
    ],
    "document": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "license",
        "URL",
    ],
    "entry": [
        "title",
        "container", 
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "entry-dictionary": [
        "title",
        "container", 
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "entry-encyclopedia": [
        "title",
        "container", 
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "event": [
        // "title",
        "event",
        "chair",
        "URL",
    ],
    "figure": [
        "title",
        "creator",
        "dimensions",
        "URL",
    ],
    "graphic": [
        "title",
        "creator",
        "illustrator",
        "dimensions",
        "URL",
    ],
    "hearing": [
        "title",
        "event-date",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "interview": [
        "interviewer",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "legal_case": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "legislation": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "manuscript": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "map": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "scale",
        "ISBN",
        "DOI",
        "URL",
    ],
    "motion_picture": [
        "director",
        "executive-producer",
        "title",
        "container", 
        "guest",
        "host",
        "narrator",
        "volume", 
        "page",
        "issued",
        "medium",
        "DOI",
        "URL",
    ],
    "musical_score": [
        "author",
        "composer",
        "title",
        "publisher",
        "publisher-place",
        "volume", 
        "edition",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "pamphlet": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "volume", 
        "edition",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "paper-conference": [
        "author",
        "title",
        "container", 
        "event-date",
        "page",
        "publisher",
        "publisher-place",
        "issued",
        "DOI",
        "URL",
    ],
    "patent": [
        "title",
        "authority",
        "URL",
    ],
    "performance": [
        "performer",
        "title",
        "event-date",
        "medium",
        "URL",
    ],
    "periodical": [
        "editor",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "personal_communication": [
        "author",
        "title",
        "URL",
    ],
    "post": [
        "author",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "post-weblog": [
        "author",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "regulation": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "report": [
        "author",
        "title",
        "institution",
        "URL",
    ],
    "review": [
        "author",
        "title",
        "reviewed-title",
        "reviewed-genre",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "review-book": [
        "author",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "software": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "version",
        "license",
        "URL",
    ],
    "song": [
        "author",
        "title",
        "container", 
        "volume", 
        "page",
        "issued",
        "DOI",
        "URL",
    ],
    "speech": [
        "author",
        "title",
        "event-date",
        "medium",
        "URL",
    ],
    "standard": [
        "authority",
        "title",
        "URL",
    ],
    "thesis": [
        "author",
        "title",
        "publisher",
        "publisher-place",
        "issued",
        "ISBN",
        "DOI",
        "URL",
    ],
    "treaty": [
        "title",
        "jurisdiction",
        "authority",
        "URL",
    ],
    "webpage": [
        "author",
        "title",
        "container", 
        "page",
        "issued",
        "URL",
    ],
}


function showHideFields() {
    var $refType = $("#id_type");
    const $form = $("#literatureForm");
    const show_suggested = $("#id_show_suggested").is(":checked");
    var relevantFields = [];

    if (show_suggested) {
        // Get relevant fields for the selected type from CSL_TYPES
        relevantFields = CSL_TYPES[$refType.val()];


        // Check if any item in CSL_PROPS starts with the relevant field name
        relevantFields = relevantFields.concat(CSL_PROPS.filter(function(prop) {
            return relevantFields.some(function(field) {
                return prop.startsWith(field + "-");
            });
        }));

        console.log(relevantFields);

        // Replace hyphens in field names with underscores
        relevantFields = relevantFields.map(function(field) {
            return field.replace(/-/g, "_");
        });

    }

    // Loop through div elements on the form and show/hide based on relevant field names
    $($form.find("div")).each(function() {
        var div = $(this);

        // Check if div has an id
        if (div.attr("id")) {
            // Get div id
            var divId = div.attr("id");

            // Extract relevant field name from div id
            var relevantFieldName = divId.replace("div_id_", "");

            // If div id matches relevant field name or toggle is not checked, or field is in CSL_ALWAYS_SHOW, show div element
            if (relevantFields.includes(relevantFieldName) || !show_suggested || CSL_ALWAYS_SHOW.includes(relevantFieldName)) {
                div.show();
            } else {
                div.hide();
            }
        }
    });
}

function showHideFieldsets() {

    const $form = $("#literatureForm");

    $form.find("fieldset").each(function() {
        const $fieldset = $(this);
        const $divsWithId = $fieldset.find('div[id]');

        if ($divsWithId.length > 0 && $divsWithId.filter(':visible').length === 0) {
            $fieldset.hide();
        } else {
            $fieldset.show();
        }
    });


    // Loop through fieldsets and hide if all divs inside are hidden
    // $($form.find("fieldset")).each(function() {
    //     var $fieldset = $(this);
    //     var $divsWithId = $fieldset.find('div[id]');

    //     if ($divsWithId.length > 0) {
    //         var allHidden = true;
    //         $divsWithId.each(function() {
    //             if ($(this).css('display') !== 'none') {
    //                 allHidden = false;
    //                 return false; // break the loop
    //             }
    //         });

    //         if (allHidden) {
    //             $fieldset.hide();
    //         }
    //     }
    // });
}

$(function() {

    showHideFields();
    showHideFieldsets();

    $("#id_show_suggested").on("change", function() {
        showHideFields();
        showHideFieldsets();
    });
    $("#id_type").on("change", function() {
        showHideFields();
        showHideFieldsets();
    });
});


// $(target.closest("form").find("input")).each(function() {
//     var el = $(this);

//     // Get input name
//     var inputName = el.attr("name");

//     // If input name is in relevant fields or toggle is not checked, display input element
//     if (relevantFields.includes(inputName) || !$("#id_show_suggested").is(":checked")) {
//         el.show();
//     } else {
//         el.hide();
//     }
// });


// var orderedRelevantNodes = [];

//     for (var i=0; i < relevantFields.length; i++) {
//         var field = relevantFields[i];
//         var el = document.querySelector(`[name="${field}"]`);
//         if (!el) {
//             console.log(`Could not find element with name "${field}"`);
//             continue;
//         }
//         var parent = el.closest(el.dataset.cslParent);
//         orderedRelevantNodes.push(parent);
//     }


//     target.closest(target.dataset.cslParent).after(...orderedRelevantNodes)
    // loop through relevant fields and append


    // // reinsert fields into the dom based on the order in CSL_TYPES
    // for (var i=0; i < reversedFields.length; i++) {
    //     var el = document.querySelector(`[name="${reversedFields[i]}"]`);
    //     var parent = el.closest(el.dataset.cslParent);

    //     // parent element of the "type" select
    //     var targetParent = target.closest(".form-control");

    //     // move parent to the first position beneath "target"
    //     parent.insertBefore(parent, targetParent.nextSibling);


    //     // parent.parentNode.appendChild(parent);
    // }



    // var fieldset = target.closest("fieldset");
    // var children = fieldset.children;

    // // loop through children and reorder based on relevant fields
    // for (var i = 0; i < children.length; i++) {
    //     var child = children[i];
    //     var name = child.querySelector("input").name;

    //     if (relevantFields.includes(name)) {
    //         // display relevant field elements
    //         fieldset.appendChild(child);
    //     }
    // }




// wait for the page to load
document.addEventListener("DOMContentLoaded", function(event) {
    var element = document.querySelector('select[name="type"]');

    // trigger onchange event for element on page load
    var event = new Event('change');

    // trigger event
    element.dispatchEvent(event);
});
