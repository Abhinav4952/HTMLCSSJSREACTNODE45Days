export class Token {
  static fromString(s) {
    // TODO(Day27-task03): if s is string "kind:value", return new Token(kind, value) trimmed; else null
    return null;
  }

  constructor(kind, value) {
    this.kind = kind;
    this.value = value;
  }
}
