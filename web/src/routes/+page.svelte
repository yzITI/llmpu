<script>
  import Swal from 'sweetalert2'
  import srpc from '$lib/utilities/srpc.js'
  import Cell from '$lib/components/Cell.svelte'
  import { AIcon } from 'ace.svelte'
  import { mdiUpload, mdiDownload, mdiRefresh } from '@mdi/js'

  const LS = window.localStorage, SS = window.sessionStorage
  let url = $state(LS.url || 'http://localhost:22222/')
  let dumpPath = $state(LS.dumpPath || 'dump.json')
  let registers = $state({}), last = $state({})
  let newRegister = $state(''), focus = $state(false)
  let loading = $state(false), connected = $state(false)

  let rs = $derived([...new Set([...Object.keys(registers), ...Object.keys(last)])].map(Number).sort((a, b) => a - b))
  $effect(() => LS.url = url)
  $effect(() => LS.dumpPath = dumpPath)

  async function init () {
    srpc(url)
    await readAll()
    last = JSON.parse(JSON.stringify(registers))
  }
  init()

  async function readAll () {
    if (loading) return
    last = JSON.parse(JSON.stringify(registers))
    loading = 'Loading registers...'
    connected = true
    try {
      registers = await srpc.read_all()
    } catch {
      connected = false
    }
    loading = false
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

  async function load () {
    if (loading || !connected) return
    loading = 'Loading dump file...'
    try {
      await srpc.load(dumpPath)
    } catch (e) {
      Swal.fire('Error', e.toString(), 'error')
    }
    loading = false
    await readAll()
    last = JSON.parse(JSON.stringify(registers))
  }

  async function dump () {
    if (loading || !connected) return
    loading = 'Dumping...'
    try {
      await srpc.dump(dumpPath)
    } catch (e) {
      Swal.fire('Error', e.toString(), 'error')
    }
    loading = false
  }
</script>

<div class="w-full h-screen min-w-[768px] flex">
  <div class="w-1/2 h-full bg-gray-700 text-white">
    <h2 class="m-4 mb-0 w-full flex items-center justify-between">
      <div class="flex items-center">
        <b class="text-xl">Registers</b>
        <button class="cursor-pointer mx-2 transition-all hover:rotate-90" onclick={readAll}>
          <AIcon path={mdiRefresh}></AIcon>
        </button>
      </div>
      <div class="font-mono mx-4 flex items-center">
        0x
        <input class="outline-none w-20 block" bind:value={newRegister} placeholder="______" onkeyup={newRegisterKeyup}>
      </div>
    </h2>
    <div class="flex flex-wrap items-start p-4 w-full">
      {#each rs as r}
        <Cell {r} s={s(r)} onclick={() => focus = r} />
      {/each}
    </div>
  </div>
  <div class="w-1/2 h-full">
    <div class="flex items-center justify-between p-4">
      <div class="flex items-center">
        <button class="cursor-pointer w-5 h-5 font-bold mr-2 rounded-full {(loading || !connected) ? 'bg-gray-500' : 'bg-green-500'}" onclick={init}></button>
        <b>{ connected ? (loading || 'Idle') : 'Disconnected'}</b>
      </div>
      <input bind:value={url} placeholder="Server URL" class="outline-none block grow text-right">
    </div>
    <div class="flex items-center mx-3">
      <button class="cursor-pointer transition-all hover:text-blue-500" onclick={load}>
        <AIcon path={mdiUpload} size="1.75rem"></AIcon>
      </button>
      <button class="mx-1 cursor-pointer transition-all hover:text-blue-500" onclick={dump}>
        <AIcon path={mdiDownload} size="1.75rem"></AIcon>
      </button>
      <input bind:value={dumpPath} placeholder="Dump Path" class="outline-none block grow">
    </div>
  </div>
</div>
