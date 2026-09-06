export function debounce (func, timeout = 300) {
  let timer
  return (...args) => {
    clearTimeout(timer)
    timer = setTimeout(() => { func.apply(this, args) }, timeout)
  }
}

export function throttle (func, timeout = 300) {
  let prev = 0
  return (...args) => {
    const now = Date.now()
    if (now - prev > timeout) {
      prev = now
      return func(...args)
    }
  }
}

