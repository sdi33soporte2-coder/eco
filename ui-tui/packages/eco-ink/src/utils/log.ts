export function logError(error: unknown): void {
  if (!process.env.ECO_INK_DEBUG_ERRORS) {
    return
  }

  console.error(error)
}
