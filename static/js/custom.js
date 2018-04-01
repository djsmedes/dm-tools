$(document).ready(function () {
    $('.clickable-row').click(function () {
        window.location = $(this).data("href");
    });
});

$(document).ready(function () {

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.combatant-context-enter').click(function () {
        var combatant = $(this).data("combatant");
        $('.combatant-context-hide').hide();
        $('.combatant-context-show').show();
        $('.combatant-context-hide-unmatch').each(function () {
            if ($(this).data("combatant") !== combatant) {
                $(this).hide()
            }
        });
        $('.combatant-context-hide-match').each(function () {
            if ($(this).data("combatant") === combatant) {
                $(this).hide()
            }
        });
    });
    $('.combatant-context-leave').click(function () {
        var combatant = $(this).data("combatant");
        $('.combatant-context-hide').show();
        $('.combatant-context-show').hide();
        $('.combatant-context-hide-unmatch').each(function () {
            if ($(this).data("combatant") !== combatant) {
                $(this).show()
            }
        });
        $('.combatant-context-hide-match').each(function () {
            if ($(this).data("combatant") === combatant) {
                $(this).show()
            }
        });
    });
    $('.enter-buff-apply-context').click(function () {
        $('.apply-context-hide').hide();
        $('.apply-context-show').show();
        $('#context').html('buff');
    });
    $('.enter-debuff-apply-context').click(function () {
        $('.apply-context-hide').hide();
        $('.apply-context-show').show();
        $('#context').html('debuff');
    });
    $('.enter-other-apply-context').click(function () {
        $('.apply-context-hide').hide();
        $('.apply-context-show').show();
        $('#context').html('other');
    });
    $('.exit-apply-context').click(exit_apply_context);

    $('#effect-to-apply').on("change paste keyup", function () {
        if ($(this).val() === '') {
            $('#apply-button').prop('disabled', true);
        } else if ($('.context-activatable.active').length) {
            $('#apply-button').prop('disabled', false);
        }
    });

    var frm = $('#effect-add-form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                $(".combatant-card-body").each(function () {
                    var id = $(this).data('id');
                    $(this).html(data[id]);
                });

            },
            error: function (data) {
                // $("#MESSAGE-DIV").html("Something went wrong!");
            }
        });
        exit_apply_context();
        $('#effect-to-apply').val('');
        return false;
    });

    $('body').on('click', '.remove-effect', function () {
        var index = $(this).data('index');
        var effect_type = $(this).data('effect-type');
        var combatant_id = $(this).data('combatant');

        $.ajax({
            type: 'post',
            url: '/ajax/remove-effect/',
            data: {
                'index': index,
                'effect_type': effect_type,
                'combatant': combatant_id
            },
            success: function (return_html) {
                if (return_html === '') {
                    return
                }
                $(".combatant-card-body").each(function () {
                    if ($(this).data('id') === combatant_id) {
                        $(this).html(return_html);
                    }
                });
            }
        })
    });
    $('body').on('click', '#remove-combatants', function () {
        if ($('#context').html() !== 'remove') {
            $('#context').html('remove');
            $('#add-combatant').html('Cancel').removeClass('btn-outline-success').addClass('btn-success').removeProp('href');
            $('#remove-combatants').removeClass('btn-outline-danger').addClass('btn-danger');
            $('.remove-context-hide').hide();
            $('.remove-context-show').show();
        } else {
            $.ajax({
                type: 'post',
                url: '/ajax/remove-combatants/',
                data: {
                    'combatant_ids': localStorage.getItem('to-remove')
                },
                success: function (return_html) {
                    if (return_html === '') {
                        return
                    }
                    $('#combatant-card-deck').html(return_html)
                }
            });
            exit_remove_context()
        }
    });
    $('body').on('click', '.context-activatable', function () {
        $(this).toggleClass('active');
        var context = $('#context').html();
        var combatant = $(this).data('combatant');
        if (context === 'remove') {
            localStorage.setItem('to-remove', localStorage.getItem('to-remove') + ',' + combatant);
        } else if (context !== '') {
            var effect = '';
            if ($(this).hasClass('active')) {
                effect = $('#effect-to-apply').val()
            }
            var id = '#' + combatant + '-' + context;
            $(id).val(effect);
            if ($('#effect-to-apply').val() !== '') {
                if ($('.context-activatable.active').length) {
                    $('#apply-button').prop('disabled', false);
                } else  {
                    $('#apply-button').prop('disabled', true);
                }
            }
        }
    });
    $('body').on('click', '#cancel-remove', exit_remove_context);
    $('body').on('submit', '.update-initiative-form', function () {
        $.ajax({
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            data: $(this).serialize(),
            success: function (return_html) {
                if (return_html === '') {
                    return
                }
                $("#combatant-card-deck").html(return_html)
            },
            error: function (data) {
                // $("#MESSAGE-DIV").html("Something went wrong!");
            }
        });
        return false;
    });
    setTimeout(poll_server, 2000);
});

function exit_apply_context() {
    $('.apply-context-hide').show();
    $('.apply-context-show').hide();
    $('#context').html('');
    $('.effect-input').val('');
    $('.context-activatable').removeClass('active');
    $('#apply-button').prop('disabled', true)
}

function exit_remove_context() {
    $('.remove-context-hide').show();
    $('.remove-context-show').hide();
    $('#context').html('');
    localStorage.setItem('to-remove', '');
    $('.context-activatable').removeClass('active');
    $('#add-combatant').html(
        'Add a combatant'
    ).removeClass(
        'btn-success'
    ).addClass(
        'btn-outline-success'
    ).prop(
        'href', $(this).data('url')
    );
    $('#remove-combatants').removeClass('btn-danger').addClass('btn-outline-danger');
}

function poll_server() {
    $.ajax({
        type: 'get',
        url: '/ajax/poll/',
        data: {
            time: new Date().getTime()
        },
        success: function (return_data) {

        },
        complete: function (data) {
            setTimeout(poll_server, 2000)
        }
    })
}