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

    $('#addCourseBtn').click(addAddressField);

    $('#driverTripOrderID').change(courseOptionsLoad);

    $('#courseExportTripOrderID').change(datesLoad);

    $('#courseImportTripOrderID').change(datesLoad);

    $('#contractorID').change(contractorReminder);
});


function addAddressField(e) {
    e.preventDefault();

    var totalForms = $('input[name="courseaddress_set-TOTAL_FORMS"]');
    var formsNum = $('.adress-form').length;
    var formRegex = RegExp(`courseaddress_set-(\\d){1}-`, 'g')
    var copiedForm = $($('.adress-form')[0]).clone();

    copiedForm.find('.address-field input[type="text"]').removeAttr('value');
    copiedForm.find('.address-field select option').removeAttr('selected');
    copiedForm.find('.address-field select option[value=""]').attr('seleted', '');
    copiedForm.find('.address-field select').niceSelect('update');
    copiedForm.find('.address-field input[type="checkbox"]').removeAttr('checked');
    copiedForm.find('input[type="hidden"][name$="id"]').removeAttr('value');
    copiedForm = copiedForm.html().replace(formRegex, `courseaddress_set-${formsNum}-`);

    $('#addCourseBtn').before(copiedForm);
    totalForms.attr('value', formsNum + 1);

    $(".date-picker").datepicker({
        format: 'yyyy-mm-dd',
    });
}


function courseOptionsLoad() {
    var driver_id = $(this).val();
    var loadCoursesURL = $(this).attr('data-load-courses-url');
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: loadCoursesURL,
        type: 'POST',
        data: {
            'driver_id': driver_id,
            'export': 'True'
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (data) {
            $('#courseExportTripOrderID').html(data);
            $('#courseExportTripOrderID').niceSelect('update');
        },
        error: function (response) {
            alert('Нещо се обърка. Опитайте отново!');
        }
    });

    $.ajax({
        url: loadCoursesURL,
        type: 'POST',
        data: {
            'driver_id': driver_id,
            'export': ''
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (data) {
            $('#courseImportTripOrderID').html(data);
            $('#courseImportTripOrderID').niceSelect('update');
        },
        error: function (response) {
            alert('Нещо се обърка. Опитайте отново!');
        }
    });
}


function datesLoad() {
    var course_export_id = $('#courseExportTripOrderID').val();
    var course_import_id = $('#courseImportTripOrderID').val();
    var loadDatesURL = $(this).attr('data-load-dates-url');
    var csrf_token = $("input[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: loadDatesURL,
        type: 'POST',
        data: {
            'course_export_id': course_export_id,
            'course_import_id': course_import_id
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