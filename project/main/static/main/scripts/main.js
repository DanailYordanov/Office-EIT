jQuery.expr[':'].icontains = function (a, i, m) {
    return jQuery(a).text().toUpperCase()
        .indexOf(m[3].toUpperCase()) >= 0;
};

$(document).ready(function () {
    $("#tableSearch").keyup(function () {
        var rows = $(".table-body").find("tr").hide();
        if (this.value.length) {
            var data = this.value.split(" ");
            $.each(data, function (i, v) {
                rows.find('.searchable').filter(":icontains('" + v + "')").parent().show();
            });
        } else rows.show();
    });

    if ($('#id_bulstat').length > 0) {
        let vat_button_html = "<button type='button' class='btn btn-outline-primary mt-2' id='vatPopulateBtn'>Попълни</button>";
        $('#id_bulstat').after(vat_button_html);
        let vat_button = $('#vatPopulateBtn');
        vat_button.hide();
    }

    if ($('#id_export').length > 0) {
        hidePerpetratorFields();
    }

    $('#addFormsetForm').click(addFormsetForm);

    $('#courseTripOrderID').change(datesLoad);

    $('#contractorID').change(contractorReminder);

    $('#id_bulstat').keyup(showVatPopulateButton);

    $('#id_bulstat').change(showVatPopulateButton);

    $('#vatPopulateBtn').click(populateVatFields);

    $('#id_export').change(hidePerpetratorFields);
});


function addFormsetForm(e) {
    e.preventDefault();

    $('#emptyFormsetForm').find('select').select2('destroy');

    var formsNum = $('.formset-form').length - 1;
    var copiedForm = $('#emptyFormsetForm').clone();
    var totalForms = $('input[name$="TOTAL_FORMS"]');

    totalForms.val(formsNum + 1);
    copiedForm.removeAttr('id');
    copiedForm.removeClass('d-none');
    copiedForm.html(copiedForm.html().replace(/__prefix__/g, formsNum));

    $('#addFormsetForm').before(copiedForm);

    copiedForm.find(".date-picker").datepicker({
        format: 'dd/mm/yyyy'
    });
    copiedForm.find('select').djangoSelect2();
    copiedForm.find('.select-tag').djangoSelect2();

    $('#emptyFormsetForm').find('select').djangoSelect2();
}


function datesLoad() {
    var course_id = $('#courseTripOrderID').val();
    var loadDatesURL = $(this).attr('data-load-dates-url');
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: loadDatesURL,
        type: 'POST',
        data: {
            'course_id': course_id
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (data) {
            $('#id_from_date').val(data['from_date']);
            $('#id_to_date').val(data['to_date']);
        },
        error: function (response) {
            alert('Нещо се обърка. Опитайте отново!');
        }
    });
}


function contractorReminder() {
    var contractor_id = $(this).val();
    var loadContractorReminderURL = $(this).attr('data-load-contractor-reminder-url');
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: loadContractorReminderURL,
        type: 'POST',
        data: {
            'contractor_id': contractor_id,
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (data) {
            if (data['cmr_reminder']) {
                var errorlist = $('#contractorID').parent().parent().find('.errorlist');
                var element = `<li class="contractor-cmr-reminder">${data['cmr_reminder']}</li>`;

                if (errorlist.length > 0) {
                    errorlist.append(element);
                }
                else {
                    $('#contractorID').parent().parent().append(`<ul class="errorlist">${element}</ul>`);
                }
            }
            else {
                $('.contractor-cmr-reminder').remove();
            }

            if (data['license_reminder']) {
                var errorlist = $('#contractorID').parent().parent().find('.errorlist');
                var element = `<li class="contractor-license-reminder">${data['license_reminder']}</li>`;

                if (errorlist.length > 0) {
                    errorlist.append(element);
                }
                else {
                    $('#contractorID').parent().parent().append(`<ul class="errorlist">${element}</ul>`);
                }
            }
            else {
                $('.contractor-license-reminder').remove();
            }
        },
        error: function (response) {
            alert('Нещо се обърка. Опитайте отново!');
        }
    });
}


function vatRegexCheck(input) {
    return [
        /^\d{8}$/gi,
        /^\d{8,10}$/gi,
        /^\d{8}[a-z]$/gi,
        /^\d{9}$/gi,
        /^\d{9,10}$/gi,
        /^\d{9}B\d{2,3}$/gi,
        /^\d{10}$/gi,
        /^\d{2,10}$/gi,
        /^\d{11}$/gi,
        /^\d{12}$/gi,
        /^((\d{9})|(\d{12}))$/gi,
        /^[\da-z]\d{7}[\da-z]$/gi,
        /^[\da-hj-np-z]{2}\d{9}$/gi,
        /^((\d{9})|(\d{12})|(GD\d{3})|(HA\d{3}))$/gi,
        /^((\d{7}[a-z])|(\d[a-z]\d{5}[a-z])|(\d{6,7}[a-z]{2}))$/gi
    ].some(function (regexp) {
        return regexp.test(input);
    });
}


function showVatPopulateButton() {
    var bulstat_input = $(this).val();
    var button_element = $('#vatPopulateBtn');

    if (vatRegexCheck(bulstat_input)) {
        if (button_element.length > 0) {
            button_element.show();
        }
    }
    else {
        if (button_element.length > 0) {
            button_element.hide();
        }
    }
}


function populateVatFields() {
    var bulstat = $('#id_bulstat').val();
    var url = $('#id_bulstat').attr('data-populate-vat-info-url');
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'bulstat': bulstat,
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (data) {
            $('#id_name').val(data['name']);
            $('#id_city').val(data['city']);
            $('#id_address').val(data['address']);
            $('#id_postal_code').val(data['postal_code']);
        },
        error: function (response) {
            alert('Нещо се обърка. Опитайте отново!');
        }
    });
}


function hidePerpetratorFields() {
    var exportCheckbox = $('#id_export')[0];

    if (exportCheckbox.checked) {
        $('#id_medical_examination_perpetrator').parent().parent().show();
        $('#id_technical_inspection_perpetrator').parent().parent().show();
    } else {
        $('#id_medical_examination_perpetrator').parent().parent().hide();
        $('#id_technical_inspection_perpetrator').parent().parent().hide();
    }
}