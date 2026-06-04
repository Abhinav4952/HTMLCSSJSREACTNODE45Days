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
  // TODO(Day29-task03): return "dog" if Dog, else "animal" if Animal, else "unknown" (most specific first)
  return "unknown";
}
