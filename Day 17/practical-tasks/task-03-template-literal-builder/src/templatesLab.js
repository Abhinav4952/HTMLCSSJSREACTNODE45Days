/**
 * @param {{id: string|number, title: string, severity: string, url: string}} issue
 * @returns {string}
 */
export function formatIssue(issue) {
  return `ISSUE ${issue.id}: ${issue.title}
Severity: ${issue.severity.toUpperCase()}
Link: ${issue.url}
`;
}