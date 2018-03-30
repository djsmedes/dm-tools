$(document).ready(function () {
  $('.clickable-row').click(function() {
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
  })
});