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
            $('#apply-button').html('Cancel').prop('type', 'button').addClass('exit-apply-context')
        } else {
            $('#apply-button').html('Apply').prop('type', 'submit').removeClass('exit-apply-context')
        }
    });

    $('.context-activatable').click(function () {
        $(this).toggleClass('active');
        var effect = '';
        if ($(this).hasClass('active')) {
            effect = $('#effect-to-apply').val()
        }
        var combatant = $(this).data('combatant');
        var id = '#' + combatant + '-' + $('#context').html();
        $(id).val(effect);
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
        if ($('#context').html() === 'remove') {
            localStorage.setItem('to-remove', localStorage.getItem('to-remove') + ',' + $(this).data('combatant'));
        }
    });
    $('body').on('click', '#cancel-remove', exit_remove_context);
});

function exit_apply_context() {
    $('.apply-context-hide').show();
    $('.apply-context-show').hide();
    console.log($('#context').html());
    $('#context').html('');
    console.log($('#context').html());
    $('.effect-input').val('');
    $('.context-activatable').removeClass('active');
}

function exit_remove_context() {
    $('.remove-context-hide').show();
    $('.remove-context-show').hide();
    console.log($('#context').html());
    $('#context').html('');
    console.log($('#context').html());
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
