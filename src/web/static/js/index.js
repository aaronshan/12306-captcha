$(document).ready(function() {
    $("#error_idx").val("");
    $("#result0").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-0") == -1) {
            value = value + "-0";
            $("#error_idx").val(value)
        }
    });
    $("#result1").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-1") == -1) {
            value = value + "-1";
            $("#error_idx").val(value)
        }
    });
    $("#result2").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-2") == -1) {
            value = value + "-2";
            $("#error_idx").val(value)
        }
    });
    $("#result3").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-3") == -1) {
            value = value + "-3";
            $("#error_idx").val(value)
        }
    });
    $("#result4").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-4") == -1) {
            value = value + "-4";
            $("#error_idx").val(value)
        }
    });
    $("#result5").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-5") == -1) {
            value = value + "-5";
            $("#error_idx").val(value)
        }
    });
    $("#result6").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-6") == -1) {
            value = value + "-6";
            $("#error_idx").val(value)
        }
    });
    $("#result7").keyup(function() {
        var value = $("#error_idx").val();
        if (value.indexOf("-7") == -1) {
            value = value + "-7";
            $("#error_idx").val(value)
        }
    });
});