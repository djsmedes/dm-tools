$(document).ready(function () {
    $('.clickable-row').click(function () {
        window.location = $(this).data("href");
    });
});

$(document).ready(function () {
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
        localStorage.setItem('effect-context', 'buff');
    });
    $('.enter-debuff-apply-context').click(function () {
        $('.apply-context-hide').hide();
        $('.apply-context-show').show();
        localStorage.setItem('effect-context', 'debuff');
    });
    $('.enter-other-apply-context').click(function () {
        $('.apply-context-hide').hide();
        $('.apply-context-show').show();
        localStorage.setItem('effect-context', 'other');
    });
    $('.exit-apply-context').click(exit_apply_context);

    $('#effect-to-apply').on("change paste keyup", function () {
        if ($(this).val() === '') {
            $('#apply-button').html('Cancel').prop('type', 'button').addClass('exit-apply-context')
        } else {
            $('#apply-button').html('Apply').prop('type', 'submit').removeClass('exit-apply-context')
        }
    });

    $('.apply-context-activatable').click(function () {
        $(this).toggleClass('active');
        var effect = '';
        if ($(this).hasClass('active')) {
            effect = $('#effect-to-apply').val()
        }
        var combatant = $(this).data('combatant');
        var id = '#' + combatant + '-' + localStorage.getItem('effect-context');
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
        var csrftoken = $("[name=csrfmiddlewaretoken]").val();

        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

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
    })
});

function exit_apply_context() {
    $('.apply-context-hide').show();
    $('.apply-context-show').hide();
    localStorage.setItem('effect-context', '');
    $('.effect-input').val('');
    $('.apply-context-activatable').removeClass('active');
}
