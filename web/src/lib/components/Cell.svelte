<script>
  let { r, s, onclick } = $props()
  const classes = [
    ['opacity-50', 'opacity-100'],
    ['bg-blue-500', 'bg-gray-500', 'bg-orange-500']
  ]
</script>

{#key r}
  <button {onclick} class="w-10 h-10 cursor-pointer rounded-xs font-mono font-bold flex items-center justify-center m-0.5 transition-all {s.map((x, i) => classes[i][x]).join(' ')}">
    <div>{Number(r).toString(16).toUpperCase()}</div>
  </button>
{/key}
