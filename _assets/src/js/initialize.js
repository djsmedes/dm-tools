document.addEventListener('DOMContentLoaded', function () {
    $('.clickable-row').click(function () {
        window.location = $(this).data("href");
    });

    require('js/vue/main.js');
});
