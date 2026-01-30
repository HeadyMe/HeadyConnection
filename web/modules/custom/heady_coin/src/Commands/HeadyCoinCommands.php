<?php

namespace Drupal\heady_coin\Commands;

use Drush\Commands\DrushCommands;

/**
 * Drush commands for the HeadyCoin informational pages.
 */
final class HeadyCoinCommands extends DrushCommands {

  /**
   * Seed HeadyCoin informational pages under /hdc.
   *
   * @command heady-coin:seed
   * @aliases hdc-seed
   */
  public function seed(): void {
    $this->logger()->notice('Seeding HeadyCoin pages is a stub. Use compliance-reviewed copy before publishing.');
  }

}
