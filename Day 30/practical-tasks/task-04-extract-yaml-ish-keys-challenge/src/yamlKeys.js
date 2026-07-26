export function parseKeyValueLines(text) {

  const res = {}
  const lines = text.split(/\r?\n/)
  for(const line of lines) {
    if(line.trim()==="") continue;
    const [key,value] = line.split(/\s*:\s*/);
    res[key.trim()] = value.trim();
  }
  return res;
}
