/*  
    JavaScript Example -  Lucio Tavernini

    Adaptive Simpson's Quadrature

    integral(f, a, b, errorBound) attempts to integrate f from
    a to b while keeping the asymptotic error estimate below
    errorBound using an adaptive implementation of Simpson's rule.

    The integrand can be unbounded and the limits can be infinite.
*/

var integralError = false;
var integralBound = 0;
var ru = roundingUnit();

//  Compute the rounding unit.
function roundingUnit() {
  var ru = 1
  do {
    ru = 0.5*ru
    var value = 1 + ru
  }
  while (value != 1)
  return 2*ru
}

function integral(f, a, b, errorBound) {
  var msg;
  //  Test parameters.
  msg = '';
  if (isNaN(a)) 
    msg = ' The lower limit is undefined.';
  if (isNaN(b)) 
    msg = msg + ' The upper limit is undefined.';
  if (isNaN(errorBound)) 
    msg = msg + ' The error bound is undefined.';
  else if (errorBound <= 0) 
    msg = msg + ' The error bound must be positive.';
  else if (errorBound == Number.POSITIVE_INFINITY)
    msg = msg + ' The error bound cannot be +infinity.';
  if (msg != '') {
    if (document.all) document.cookie = msg;  //  Explorer
    else document.cookie += msg;              //  Netscape
    window.open("integralerror.html","","width=600," + 
      "height=80,screenX=50,screenY=50,resizable=0," + 
      "toolbar=0,directories=0," + 
      "status=0,menubar=0,scrollbars=1");
    return NaN;
  }
  //  Return 0? 
  if (a == b) return 0;
  //  Set globals. 
  integralBound = errorBound;
  integralError = false;
  //  Compute.
  return _integral(f, a, b, errorBound);
}

function _integral(f, a, b, errorBound) {
  var left, right, max, mstart, j;
  var jend, step, m, m1, fa, fb, v1, v2;
  var error, bound, h, h6, value, result;
  if (integralError) return Math.NaN;

  //  Swap integration limits?
  if (a > b)  return -_integral(f, b, a, errorBound);

  //  Integrate over ]-infinity,+infinity[? 
  if (a == Number.NEGATIVE_INFINITY && 
    b == Number.POSITIVE_INFINITY) 
    return _integral(f, 0, b, 0.5*errorBound) 
             + _integral(f, a, 0, 0.5*errorBound);

  //  Integrate over [a,+infinity[? 
  if (b == Number.POSITIVE_INFINITY) {
    h = 5;
    left = a;
    right = a + h;
    result = 0;
    do {
      value = _integral(f, left, right, errorBound/h);
      result += value;
      h = 2*h;
      left = right;
      right = left + h;
    }
    while (!isNaN(value) && 
      Math.abs(value) >= 0.5*errorBound/h && left < right)
    if (integralError) result = Number.NaN;
    return result;
  }

  //  Integrate over ]-infinity,b]? 
  if (a == Number.NEGATIVE_INFINITY) {
    h = 5;
    left = b - h;
    right = b;
    result = 0;
    do {
      value = _integral(f, left, right, errorBound/h);
      result += value;
      h = 2*h;
      right = left;
      left = right - h;
    }
    while (!isNaN(value) && 
      Math.abs(value) >= 0.5*errorBound/h && left < right)
    if (integralError) result = Number.NaN;
    return result;
  }

  //  Integrate over [a,b].  Initialize. 
  if (integralError) return Number.NaN;
  max = 1024;
  var x = new Array(max);
  var f1 = new Array(max);
  var f2 = new Array(max);
  var f3 = new Array(max);
  var v = new Array(max);
  step = 1;
  m = 1;
  bound = errorBound;
  value = 0;
  h = b - a;
  x[0] = a;
  f1[0] = f(a);
  f2[0] = f(0.5*(a + b));
  f3[0] = f(b);
  v[0] = h*(f1[0] + 4*f2[0] + f3[0])/6;
  do {
    //  Are we going to go forward or backward? 
    if (step == -1) {
      //  Forward: j = m,...,max 
      step = 1;
      j = m + 1;
      jend = max;
      m = 0;
      mstart = 0;
    }
    else {
      //  Backward: j = m,...,1
      step = -1;
      j = m - 1;
      jend = -1;
      m = max - 1;
      mstart = max - 1;
    }
    h = 0.5*h;
    h6 = h/6;
    bound = 0.5*bound;
    do {
      left = x[j];
      right = x[j] + 0.5*h;
      //  Complete loss of significance?
      if (left >= right) {
        alert('integral: Error 1');
        return value;
      }
      fa = f(x[j] + 0.5*h);
      fb = f(x[j] + 1.5*h);
      v1 = h6*(f1[j] + 4*fa + f2[j]);
      v2 = h6*(f2[j] + 4*fb + f3[j]);
      error = (v[j] - v1 - v2)/15;
      if (Math.abs(error) <= bound || 
        Math.abs(v1 + v2) < Math.abs(value)*ru) {
        value = ((v1 + v2) + value) - error;
      }
      else {
        if (integralError) return Number.NaN;
        //  Are we out of memory?
        if (m == j) {
          left = x[j];
          right = x[j] + 0.5*h;
          //  Complete loss of significance?
          if (left >= right) {
            alert('integral: Error 2');
            return value;
          }
          value += _integral(f, left, x[j] + 2*h, bound);
        }
        else {
          //  No, we are not.
          left = x[j];
          right = x[j] + 0.125*h;
          if (left >= right) {
            msg = ' The error bound specified (' + 
                  integralBound + ') is too small.';
            if (document.all) document.cookie = msg;  //  Explorer
            else document.cookie += msg;              //  Netscape
            window.open("integralerror.html","",
              "width=600,height=40," +
              "screenX=50,screenY=50," + 
              "resizable=0,toolbar=0,directories=0," + 
              "status=0,menubar=0,scrollbars=1");
            integralError = true;
            return Math.NaN;
          }
          m1 = m + step;
          x[m] = x[j];
          x[m1] = x[j] + h;
          v[m] = v1;
          v[m1] = v2;
          f1[m] = f1[j];
          f2[m] = fa;
          f3[m] = f2[j];
          f1[m1] = f2[j];
          f2[m1] = fb;
          f3[m1] = f3[j];
          m += 2*step;
        }
      }
      j += step;
    }
    while (j != jend)
  }
  while (m != mstart)
  result = value;
  if (integralError) result = NaN;
  return result;
}