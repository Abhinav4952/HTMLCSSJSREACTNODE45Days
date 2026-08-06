export function redactEmails(text) {
  return text.replace(/(\w+)@([\w.]+)/g, "<redacted:$2>");
}