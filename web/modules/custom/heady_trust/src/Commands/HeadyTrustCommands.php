<?php

namespace Drupal\heady_trust\Commands;

use Drush\Commands\DrushCommands;

/**
 * Drush commands for the Heady Trust Center.
 */
final class HeadyTrustCommands extends DrushCommands {

  /**
   * Seed the Trust Center pages.
   *
   * @command heady-trust:seed
   * @aliases htc-seed
   */
  public function seed(): void {
    $this->logger()->notice('Seeding Trust Center pages is a stub. Implement content creation in a deployment-aware manner.');
  }

}
