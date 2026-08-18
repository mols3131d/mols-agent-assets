function normalizePath(path) {
  return String(path || "")
    .replace(/^\/+/, "")
    .replace(/\/+$/, "");
}

function splitFilePath(path) {
  const normalizedPath = normalizePath(path);
  const parts = normalizedPath.split("/");
  const filename = parts.pop();

  return {
    filename,
    parentPath: parts.join("/"),
  };
}

function globToRegex(pattern) {
  const escaped = normalizePath(pattern)
    .replace(/[.+^${}()|[\]\\]/g, "\\$&")
    .replace(/\*\*/g, "___DOUBLE_STAR___")
    .replace(/\*/g, "[^/]*")
    .replace(/___DOUBLE_STAR___/g, ".*");

  return new RegExp(`^${escaped}$`);
}

function isIgnoredPath(path, rules = CONFIG.IGNORE_RULES) {
  const normalizedPath = normalizePath(path);

  return (rules || []).some((rule) => {
    return globToRegex(rule).test(normalizedPath);
  });
}
