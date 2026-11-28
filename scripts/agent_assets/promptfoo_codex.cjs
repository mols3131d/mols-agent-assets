const { createRequire } = require("node:module");

module.exports = class CodexProvider {
  #native;
  #env;
  #timeoutMs;

  constructor({ config: { timeout_ms, ...config }, env }) {
    this.config = config;
    this.#env = env;
    this.#timeoutMs = timeout_ms;
  }

  id() {
    return `openai:codex-sdk:${this.config.model}`;
  }

  async callApi(prompt, context, options = {}) {
    // The CLI and SDK are installed together by npx, outside this checkout.
    const { loadApiProvider } = createRequire(process.argv[1])("promptfoo");
    this.#native ??= loadApiProvider(this.id(), {
      options: { config: this.config, env: this.#env },
    });
    const provider = await this.#native;
    const deadline = AbortSignal.timeout(this.#timeoutMs);
    const abortSignal = options.abortSignal
      ? AbortSignal.any([options.abortSignal, deadline])
      : deadline;
    const timedOut = () =>
      deadline.aborted && abortSignal.reason === deadline.reason;
    try {
      const response = await provider.callApi(prompt, context, {
        ...options,
        abortSignal,
      });
      if (!timedOut()) {
        return response;
      }
    } catch (error) {
      if (!timedOut()) {
        throw error;
      }
    }
    return { error: `Codex call timed out after ${this.#timeoutMs}ms` };
  }

  async cleanup() {
    const native = this.#native;
    this.#native = undefined;
    const provider = await native?.catch(() => undefined);
    await provider?.cleanup();
  }
};
