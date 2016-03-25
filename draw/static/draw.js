$(document).ready(function () {
    updateTeams();
    $("#btn-draw").click(draw);
    $(document).ajaxError(function (event, xhr, settings, error) {
        alert("Error: " + xhr.status + " " + xhr.statusText);
        enableUI();
    });
});

function updateTeams() {
    $.get("freeteams", {}, function (data, status, xhr) {
        var $select = $("#sel-teams");
        $select.empty();
        data.teams.forEach(function (t, i, a) {
            $("<option>").attr("value", t.id).html(t.name).appendTo($select);
        });
    });
}

function enableUI() {
    $(".draw-ui").removeAttr("disabled");
}

function disableUI() {
    $(".draw-ui").attr("disabled", "disabled");
}

function show(value, confirmed) {
    var $output = $("#output");
    $output.html(value);
    if (confirmed)
        $output.addClass("confirmed");
    else
        $output.removeClass("confirmed");
}

function draw() {
    var t = $("#sel-teams").val();
    if (!t)
        return alert("No more available teams for drawing.");

    disableUI();
    $.get("next", {"t": t}, function (data, status, xhr) {
        var time = 1;
        data.display.forEach(function (s, i, a) {
            setTimeout(show, time, s, false);
            time += 250;
        });
        setTimeout(show, time, data.slot, true);
        setTimeout("enableUI(); updateTeams();", time);
    });
};
