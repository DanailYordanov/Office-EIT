$("#tableSearch").keyup(function () {
    var rows = $(".table-body").find("tr").hide();
    if (this.value.length) {
        var data = this.value.split(" ");
        $.each(data, function (i, v) {
            rows.find('.searchable').filter(":contains('" + v + "')").parent().show();
        });
    } else rows.show();
});