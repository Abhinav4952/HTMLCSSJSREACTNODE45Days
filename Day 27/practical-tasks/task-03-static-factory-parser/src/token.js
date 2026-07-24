export class Token {
  static fromString(s) {
    if(typeof s==="string") {
      s = s.trim();
      let parts = s.split(":")
      if(parts.length===2 && parts[0].trim()!=="" && parts[1].trim()!=="") return new Token(parts[0].trim(),parts[1].trim());
    }
    return null;
  }

  constructor(kind, value) {
    this.kind = kind;
    this.value = value;
  }
}
