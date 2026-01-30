# Foundation UI Patterns

## Six-Dot Action Button

The Foundation landing page and the Parent Portal use a six-dot action button to signal verified, intentional actions.
This pattern is intended to reinforce deliberate, high-trust interactions (for example: navigation to the patent stack or
parental control actions).

### Structure

```html
<button class="six-dot-button">
  <span>Action Label</span>
  <span class="dot-grid" aria-hidden="true">
    <span class="dot"></span>
    <span class="dot"></span>
    <span class="dot"></span>
    <span class="dot"></span>
    <span class="dot"></span>
    <span class="dot"></span>
  </span>
</button>
```

### Behavior

- Hover: dots brighten and expand slightly to show readiness.
- Focus-visible: a high-contrast outline appears for keyboard navigation.
- Active filter state (Parent Portal only): the button stays highlighted for clarity.

### Accessibility Notes

- The dot grid is `aria-hidden` to keep screen-reader output clean.
- Use `aria-pressed` for toggle-style filters.
- Ensure primary actions retain the six-dot pattern to keep visual consistency across pages.
