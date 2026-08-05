export class ValidationError extends Error {
  constructor(message, field) {
    super(message);
    this.name="ValidationError"
    this.field = field;
  }
}
