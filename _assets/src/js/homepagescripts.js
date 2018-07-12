module.exports = {

    initialize: function () {
        var body = $('body');

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

        $('#display-only-toggle-button').click(function () {
            body.toggleClass('context-display-only');
            $(this).toggleClass('text-muted')
        });

        body.on('click', '.combatant-context-enter', function () {
            var combatant = $(this).data('combatant');
            body.addClass('context-combatant').data('combatant', combatant);
            label_matched_combatants()
        });
        body.on('click', '.combatant-context-leave', function () {
            body.removeClass('context-combatant').data('combatant', '');
            $('.context-combatant-match').each(function () {
                $(this).removeClass('context-combatant-match');
            });
        });

        $('.enter-apply-context').click(function () {
            var which_context_type = $(this).data('apply-effect-type');
            body.addClass('context-apply').data('apply-effect-type', which_context_type);
        });

        $('.exit-apply-context').click(exit_apply_context);

        $('#effect-to-apply').on("change paste keyup", function () {
            var myval = $(this).val();
            var active_combatant_buttons = $('.context-activatable.active');
            if (myval === '') {
                $('#apply-button').prop('disabled', true);
            } else if (active_combatant_buttons.length) {
                $('#apply-button').prop('disabled', false);
            }
            active_combatant_buttons.each(function () {
                var combatant = $(this).data('combatant');
                $('#' + combatant + '-' + body.data('apply-effect-type')).val(myval)
            })
        });

        var effect_add_form = $('#effect-add-form');
        effect_add_form.submit(function () {
            $.ajax({
                type: effect_add_form.attr('method'),
                url: effect_add_form.attr('action'),
                data: effect_add_form.serialize(),
                success: function (data) {
                    $(".combatant-card-body").each(function () {
                        // todo change combatant card body data-id to data-combatant
                        var id = $(this).data('id');
                        $(this).html(data[id]);
                    });

                }
            });
            exit_apply_context();
            $('#effect-to-apply').val('');
            return false;
        });

        body.on('click', '.remove-effect', function () {
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

        body.on('click', '#enter-remove-context', function () {
            body.addClass('context-remove');
        });

        var remove_combatants_form = $('#remove-combatants-form');
        remove_combatants_form.submit(function () {
            $.ajax({
                type: remove_combatants_form.attr('method'),
                url: remove_combatants_form.attr('action'),
                data: remove_combatants_form.serialize(),
                success: function (return_html) {
                    if (return_html === '') {
                        return
                    }
                    $('#combatant-card-deck').html(return_html);
                    label_matched_combatants();
                }
            });
            exit_remove_context();
            return false;
        });


        body.on('click', '.context-activatable', function () {
            $(this).toggleClass('active');
            var combatant = $(this).data('combatant');
            if (body.hasClass('context-remove')) {
                var combatant_to_remove_selector = $("#combatant-to-remove-" + combatant);
                if ($(this).hasClass('active')) {
                    combatant_to_remove_selector.val('True')
                } else {
                    combatant_to_remove_selector.val('')
                }
                if ($('.context-activatable.active').length) {
                    $('#confirm-remove-combatants-button').prop('disabled', false);
                } else {
                    $('#confirm-remove-combatants-button').prop('disabled', true);
                }
            }
            if (body.hasClass('context-apply')) {
                var effect = '';
                var effect_to_apply = $('#effect-to-apply').val();
                var apply_effect_type = body.data('apply-effect-type');
                if ($(this).hasClass('active')) {
                    effect = effect_to_apply
                }
                $('#' + combatant + '-' + apply_effect_type).val(effect);
                if (effect_to_apply !== '') {
                    if ($('.context-activatable.active').length) {
                        $('#apply-button').prop('disabled', false);
                    } else {
                        $('#apply-button').prop('disabled', true);
                    }
                }
            }
        });

        body.on('click', '#cancel-remove', exit_remove_context);

        body.on('submit', '.update-initiative-form', function () {
            $.ajax({
                type: $(this).attr('method'),
                url: $(this).attr('action'),
                data: $(this).serialize(),
                success: function (return_html) {
                    if (return_html === '') {
                        return
                    }
                    $("#combatant-card-deck").html(return_html);
                    label_matched_combatants();
                }
            });
            return false;
        });
        var last_updated = new Date().getTime();
        setTimeout(function () {
            poll_server(last_updated)
        }, 2500);
    }
};

function exit_apply_context() {
    $('body').removeClass('context-apply');
    $('.effect-input').val('');
    $('.context-activatable').removeClass('active');
    $('#apply-button').prop('disabled', true)
}

function exit_remove_context() {
    $('body').removeClass('context-remove');
    $('.combatant-to-remove').val('');
    $('.context-activatable').removeClass('active');
    $('#confirm-remove-combatants-button').prop('disabled', true)
}

function poll_server(last_updated) {
    $.ajax({
        type: 'get',
        url: '/ajax/poll/',
        data: {
            last_updated: last_updated
        },
        success: function (return_data) {
            if (return_data.needs_update) {
                update_all_combatants();
                last_updated = new Date().getTime();
            }
        },
        complete: function (data) {
            setTimeout(function () {
                poll_server(last_updated)
            }, 2500);
        }
    })
}

function update_all_combatants() {
    var url = '/ajax/update-all-combatants/';
    $.ajax({
        type: 'post',
        url: url,
        data: {},
        success: function (return_html) {
            if (return_html === '') {
                return
            }
            $("#combatant-card-deck").html(return_html);
            label_matched_combatants();
        }
    });
}

function label_matched_combatants() {
    var body = $('body');
    if (body.hasClass('context-combatant')) {
        var combatant = body.data('combatant');
        if (combatant) {
            $('.combatant-context-match-hide, .combatant-context-unmatch-hide').each(function () {
                if ($(this).data('combatant') === combatant) {
                    $(this).addClass('context-combatant-match')
                }
            });
        }
    }
}