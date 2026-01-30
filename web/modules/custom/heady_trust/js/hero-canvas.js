(function (Drupal, drupalSettings) {
  Drupal.behaviors.headyTrustHero = {
    attach: function (context) {
      if (context.querySelector('.heady-trust-hero')) {
        return;
      }
      const hero = document.createElement('div');
      hero.className = 'heady-trust-hero';
      hero.style.position = 'absolute';
      hero.style.inset = '0';
      hero.style.pointerEvents = 'none';
      hero.style.background = 'radial-gradient(circle at 20% 20%, rgba(59,130,246,0.12), transparent 45%)';
      const main = document.querySelector('main');
      if (main) {
        main.style.position = 'relative';
        main.prepend(hero);
      }
    }
  };
})(Drupal, drupalSettings);
