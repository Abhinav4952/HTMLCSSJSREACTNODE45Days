"use strict"

export function standaloneThisType() {
  return (function() {return typeof this})();
}
