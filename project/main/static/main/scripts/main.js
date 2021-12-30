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