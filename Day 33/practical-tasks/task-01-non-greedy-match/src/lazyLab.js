export function firstTagContents(html) {
  const res =  html.match(/<[a-z]+>(.*?)<\/[a-z]+>/);
  return res? res[1] : null;
}
