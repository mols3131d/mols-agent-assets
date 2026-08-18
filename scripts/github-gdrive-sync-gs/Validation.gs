function validateConfig(config = CONFIG) {
  validateRequiredString(
    config.TARGET_FOLDER_ID,
    "TARGET_FOLDER_ID",
    "구글 드라이브 폴더의 ID를 정확히 입력해 주세요.",
  );

  validateRequiredString(config.GITHUB_OWNER, "GITHUB_OWNER");
  validateRequiredString(config.GITHUB_REPO, "GITHUB_REPO");
  validateRequiredString(config.BRANCH, "BRANCH");
  validateRequiredString(config.SYNC_MARKER_FILENAME, "SYNC_MARKER_FILENAME");

  validatePositiveInteger(config.SYNC_INTERVAL_DAYS, "SYNC_INTERVAL_DAYS");

  validateIntegerRange(config.SYNC_RUN_HOUR, "SYNC_RUN_HOUR", 0, 23);

  if (!Array.isArray(config.IGNORE_RULES)) {
    throw new Error("설정 오류: IGNORE_RULES는 배열이어야 합니다.");
  }

  if (typeof config.DRY_RUN_DELETE !== "boolean") {
    throw new Error("설정 오류: DRY_RUN_DELETE는 boolean 값이어야 합니다.");
  }

  validateNonNegativeInteger(config.MAX_DELETE_PER_RUN, "MAX_DELETE_PER_RUN");

  validatePositiveInteger(
    config.MIN_EXPECTED_GITHUB_FILES,
    "MIN_EXPECTED_GITHUB_FILES",
  );

  if (config.TARGET_FOLDER_ID === "YOUR_GOOGLE_DRIVE_FOLDER_ID") {
    throw new Error(
      "설정 오류: TARGET_FOLDER_ID가 placeholder 값입니다. 실제 구글 드라이브 폴더 ID를 입력하세요.",
    );
  }
}

function validateRequiredString(value, name, extraMessage = "") {
  if (!value || String(value).trim() === "") {
    const suffix = extraMessage ? ` ${extraMessage}` : "";
    throw new Error(`설정 오류: ${name} 설정이 비어 있습니다.${suffix}`);
  }
}

function validatePositiveInteger(value, name) {
  const numberValue = Number(value);

  if (!Number.isInteger(numberValue) || numberValue <= 0) {
    throw new Error(
      `설정 오류: ${name}는 1 이상의 정수여야 합니다. 현재 입력값: "${value}"`,
    );
  }
}

function validateNonNegativeInteger(value, name) {
  const numberValue = Number(value);

  if (!Number.isInteger(numberValue) || numberValue < 0) {
    throw new Error(
      `설정 오류: ${name}은 0 이상의 정수여야 합니다. 현재 입력값: "${value}"`,
    );
  }
}

function validateIntegerRange(value, name, min, max) {
  const numberValue = Number(value);

  if (
    !Number.isInteger(numberValue) ||
    numberValue < min ||
    numberValue > max
  ) {
    throw new Error(
      `설정 오류: ${name}는 ${min}부터 ${max} 사이의 정수여야 합니다. 현재 입력값: "${value}"`,
    );
  }
}
