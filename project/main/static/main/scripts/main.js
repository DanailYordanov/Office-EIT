$(document).ready(function () {
    $("#tableSearch").keyup(function () {
        var rows = $(".table-body").find("tr").hide();
        if (this.value.length) {
            var data = this.value.split(" ");
            $.each(data, function (i, v) {
                rows.find('.searchable').filter(":contains('" + v + "')").parent().show();
            });
        } else rows.show();
    });

    $('#addCourseBtn').click(addAddressField);

    $('#driverTripOrderID').change(courseOptionsLoad);

    $('#courseTripOrderID').change(datesLoad);
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
            'driver_id': driver_id
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        success: function (data) {
            $('#courseTripOrderID').html(data);
            $('#courseTripOrderID').niceSelect('update');
        },
        error: function (response) {
            alert('Нещо се обърка. Опитайте отново!');
        }
    });
}


function datesLoad() {
    var course_id = $(this).val();
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