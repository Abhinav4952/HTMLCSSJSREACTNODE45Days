export class ValidationError extends Error {
  constructor(message, field) {
    // TODO(Day32-task03): super(message); set this.field = field; set this.name = "ValidationError"
    super();
    this.field = "";
  }
}
