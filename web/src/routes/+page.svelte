<script>
  import srpc from '$lib/utilities/srpc.js'
  import Cell from '$lib/components/Cell.svelte'

  const LS = window.localStorage, SS = window.sessionStorage
  let url = $state(LS.url || 'http://localhost:22222/')
  let dumpPath = $state(LS.dumpPath || 'dump.json')
  let registers = $state({}), last = $state({})
  let newRegister = $state(''), focus = $state(false)
  let loading = $state(false)

  let rs = $derived([...new Set([...Object.keys(registers), ...Object.keys(last)])].map(Number).sort((a, b) => a - b))

  async function init () {
    srpc(url)
    await readAll()
    last = JSON.parse(JSON.stringify(registers))
  }
  init()

  async function readAll () {
    last = JSON.parse(JSON.stringify(registers))
    registers = await srpc.read_all()
  }
  
  async function newRegisterKeyup (e) {
    if (e.key !== 'Enter') return
    const r = parseInt(newRegister, 16)
    if (isNaN(r)) return newRegister = ''
    registers[r] = registers[r] || ''
    last[r] = last[r] || ''
    newRegister = ''
  }

  function s (r) {
    let res = [0, 1]
    if (registers[r]) res[0] = 1
    if (registers[r] !== last[r]) res[1] = 2
    if (r === focus) res[1] = 0
    return res
  }
</script>

<div class="w-full h-screen min-w-[768px] flex">
  <div class="w-1/2 h-full bg-gray-700 text-white">
    <h2 class="m-4 mb-0 w-full flex items-center justify-between">
      <b class="text-xl">Registers</b>
      <div class="font-mono mx-4 flex items-center">
        0x
        <input class="outline-none w-20 block" bind:value={newRegister} placeholder="___" onkeyup={newRegisterKeyup}>
      </div>
    </h2>
    <div class="flex flex-wrap items-start p-4 w-full">
      {#each rs as r}
        <Cell {r} s={s(r)} onclick={() => focus = r} />
      {/each}
    </div>
  </div>
  <div class="w-1/2 h-full">
    <p>To be constructed</p>
    <div>
      <input bind:value={url} placeholder="Server URL" class="outline-none text-xs">
    </div>
    <div>
      <input bind:value={dumpPath} placeholder="Dump Path" class="outline-none text-xs">
    </div>
  </div>
</div>
