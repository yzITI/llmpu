<script>
  let { r, s, onclick } = $props()
  const classes = [
    ['opacity-50', 'opacity-100'],
    ['bg-blue-500', 'bg-gray-500', 'bg-orange-700', 'bg-green-700', 'bg-yellow-700', 'bg-red-700']
  ]
  let display = $derived(Number(r).toString(16).toUpperCase())
  let size = $derived(4 / display.length - 0.5 * Math.max(0, (3 - display.length) ** 2 ))
</script>

{#key r}
  <button {onclick} class="w-12 h-12 cursor-pointer rounded-xs font-mono font-bold flex items-center justify-center m-0.5 transition-all duration-500 {s.map((x, i) => classes[i][x]).join(' ')}" style="font-size: {size}rem;">
    <div>{display}</div>
  </button>
{/key}
