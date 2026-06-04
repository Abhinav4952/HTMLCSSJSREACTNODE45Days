import { Animal } from "./animal.js";

export class Dog extends Animal {
  constructor(name, breed) {
    // TODO(Day29-task02): super(name); store breed string (default "mixed")
    super("");
    this.breed = "mixed";
  }

  speak() {
    // TODO(Day29-task02): return super.speak() + " (" + this.breed + ")"
    return "";
  }
}
