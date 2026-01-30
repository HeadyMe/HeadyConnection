export default {
  async fetch(request, env, ctx) {
    return new Response(JSON.stringify({ status: "ok" }), {
      headers: { "content-type": "application/json" }
    });
  },
  async scheduled(event, env, ctx) {
    // Placeholder scheduler hook for periodic intel refresh.
    ctx.waitUntil(Promise.resolve());
  },
  async queue(batch, env, ctx) {
    // Placeholder queue hook for async processing.
    ctx.waitUntil(Promise.resolve());
  }
};
