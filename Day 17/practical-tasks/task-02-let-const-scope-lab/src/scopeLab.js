/**
 * Classic `var` loop closure trap: all functions close over the same binding.
 * @returns {number[]}
 */
export function varLoopClosureMappedValues() {
  const funcs=[];

  for(var i=0;i<3;i++) {
    funcs.push(function(){
      return i;
    })
  }
  return funcs.map((fn)=> fn())
}

/**
 * `let` loop closure: each iteration gets its own binding.
 * @returns {number[]}
 */
export function letLoopClosureMappedValues() {
  const funcs=[];

  for(let i=0;i<3;i++) {
    funcs.push(function(){
      return i;
    })
  }
  return funcs.map((fn)=> fn())

}

/**
 * Demonstrate block-local shadowing with `let`.
 * @returns {number}
 */
export function blockShadowValue() {
  let x=1;
  {
    let x=2;
    return x;
  }
}

/**
 * `const` prevents rebinding, but object properties may still change.
 * @returns {number}
 */
export function constObjectPropertyMutation() {
  const o = {n:3};
  o.n=7;
  return o.n;
}
