<?php

namespace Drupal\heady_trust\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Component\Serialization\Json;

/**
 * Provides a Trust Center system status block stub.
 *
 * @Block(
 *   id = "heady_trust_system_status",
 *   admin_label = @Translation("Heady Trust System Status"),
 * )
 */
final class SystemStatusBlock extends BlockBase {

  /**
   * {@inheritdoc}
   */
  public function build(): array {
    $statusPath = getenv('HEADY_STATUS_FEED_PATH') ?: 'public://status/system.json';
    $fileSystem = \Drupal::service('file_system');
    $realPath = $fileSystem->realpath($statusPath) ?: $statusPath;
    $logger = \Drupal::logger('heady_trust');

    $status = 'unknown';
    $summary = 'Status feed unavailable';
    $updatedAt = null;
    $allowedStatuses = ['ok', 'degraded', 'outage', 'unknown'];

    if (!$realPath || !is_readable($realPath)) {
      $logger->warning('Status feed not readable at {path}', ['path' => $realPath ?: $statusPath]);
    }
    else {
      $raw = file_get_contents($realPath);
      if ($raw === false) {
        $logger->warning('Status feed could not be read at {path}', ['path' => $realPath]);
      }
      else {
        $data = Json::decode($raw) ?? [];
        if (!is_array($data)) {
          $logger->warning('Status feed JSON invalid at {path}', ['path' => $realPath]);
        }
        else {
          $status = strtolower((string) ($data['status'] ?? $status));
          $summary = trim((string) ($data['summary'] ?? $summary));
          $updatedAt = $data['updated_at'] ?? null;
        }
      }
    }

    if (!in_array($status, $allowedStatuses, true)) {
      $logger->warning('Status feed value invalid: {status}', ['status' => $status]);
      $status = 'unknown';
    }
    if ($summary === '') {
      $summary = 'Status feed unavailable';
    }

    $isHealthy = $status === 'ok';
    $label = match ($status) {
      'ok' => 'Operational',
      'degraded' => 'Degraded',
      'outage' => 'Outage',
      default => 'Unknown',
    };
    $indicator = match ($status) {
      'ok' => '#16a34a',
      'degraded' => '#f59e0b',
      'outage' => '#dc2626',
      default => '#64748b',
    };

    return [
      '#type' => 'inline_template',
      '#template' => '<div class="heady-trust-status" style="display:flex;gap:12px;align-items:center;">'
        . '<span class="heady-trust-status__dot" style="width:10px;height:10px;border-radius:999px;background:{{ indicator }};box-shadow:0 0 8px {{ indicator }};"></span>'
        . '<div><strong>{{ label }}</strong><div style="font-size:0.85em;color:#475569;">{{ summary }}</div>'
        . '{% if updated_at %}<div style="font-size:0.75em;color:#64748b;">Updated {{ updated_at }}</div>{% endif %}</div></div>',
      '#context' => [
        'indicator' => $indicator,
        'label' => $this->t($label),
        'summary' => $this->t($summary),
        'updated_at' => $updatedAt,
      ],
      '#cache' => [
        'max-age' => 30,
      ],
    ];
  }

}
