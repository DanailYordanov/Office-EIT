$("#tableSearch").keyup(function () {
    var rows = $(".cars-body-table").find("tr").hide();
    if (this.value.length) {
        var data = this.value.split(" ");
        $.each(data, function (i, v) {
            rows.find('.brands').filter(":contains('" + v + "')").parent().show();
            rows.find('.number-plates').filter(":contains('" + v + "')").parent().show();
        });
    } else rows.show();
});