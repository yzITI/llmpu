<script>
  let { r, s, onclick } = $props()
  const classes = [
    ['opacity-50', 'opacity-100'],
    ['', 'ring-3 ring-inset'],
    ['bg-gray-500', 'bg-green-700', 'bg-blue-700', 'bg-red-700']
  ]
  let display = $derived(Number(r).toString(16).toUpperCase())
  let size = $derived(4 / display.length - 0.5 * Math.max(0, (3 - display.length) ** 2 ))
</script>

{#key r}
  <button {onclick} class="relative w-12 h-12 cursor-pointer rounded-xs font-mono font-bold flex items-center justify-center m-0.5 transition-all duration-500 {classes.map((x, i) => x[s[i]]).join(' ')}" style="font-size: {size}rem;">
    <div class="absolute right-1 top-1 rounded-full w-2 h-2 bg-white transition-all duration-500 { s[3] ? 'opacity-100' : 'opacity-0' }"></div>
    <div>{display}</div>
  </button>
{/key}
