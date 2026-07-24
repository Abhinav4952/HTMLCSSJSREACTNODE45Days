export class Animal {
  constructor(name = "") {
    this.name = typeof name === "string" ? name : "";
  }
}

export class Dog extends Animal {
  constructor(name = "", breed = "mixed") {
    super(name);
    this.breed = typeof breed === "string" ? breed : "mixed";
  }
}

export function classifyPet(x) {
  if (x instanceof Dog) {
    return "dog";
  } else if (x instanceof Animal) {
    return "animal";
  }
  return "unknown";
}