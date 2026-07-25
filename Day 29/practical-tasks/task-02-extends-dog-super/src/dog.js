import { Animal } from "./animal.js";

export class Dog extends Animal {
  constructor(name, breed="mixed") {
    super(name);
    this.breed = breed;
  }

  speak() {
    return super.speak() + ` (${this.breed})`;
  }
}
