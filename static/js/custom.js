$(document).ready(function () {
  $('.clickable-row').click(function() {
      window.location = $(this).data("href");
  });
});

$(document).ready(function () {
  $('.pc-context-enter').click(function () {
      var pc = $(this).data("pc");
      $('.pc-context-hide').hide();
      $('.pc-context-show').show();
      $('.pc-context-hide-unmatch').each(function () {
          if ($(this).data("pc") !== pc) {
              $(this).hide()
          }
      });
      $('.pc-context-hide-match').each(function () {
          if ($(this).data("pc") === pc) {
              $(this).hide()
          }
      });
  });
  $('.pc-context-leave').click(function () {
      var pc = $(this).data("pc");
      $('.pc-context-hide').show();
      $('.pc-context-show').hide();
      $('.pc-context-hide-unmatch').each(function () {
          if ($(this).data("pc") !== pc) {
              $(this).show()
          }
      });
      $('.pc-context-hide-match').each(function () {
          if ($(this).data("pc") === pc) {
              $(this).show()
          }
      });
  })
});