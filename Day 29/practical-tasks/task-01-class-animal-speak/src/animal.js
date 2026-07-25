export class Animal {
  constructor(name = "") {
    if(typeof name ==="string") this.name = name;
  }

  speak() {
    if(this.name.trim()!=="") return `${this.name.trim()} says something`
    return "...";
  }
}
