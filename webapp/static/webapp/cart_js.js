  $(document).ready(function() {
      $('.minus').click(function () {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
      });
      $('.plus').click(function () {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
      });
    });

  new Drift(document.querySelector('.drift-demo-trigger'), {
  paneContainer: document.querySelector('.details'),
  inlinePane: 769,
  inlineOffsetY: -85,
  containInline: true,
  hoverBoundingBox: true
});