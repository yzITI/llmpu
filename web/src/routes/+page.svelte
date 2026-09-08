<script>
  import Swal from 'sweetalert2'
  import srpc from '$lib/utilities/srpc.js'
  import { debounce } from '$lib/utilities/utils.js'
  import Cell from '$lib/components/Cell.svelte'
  import CodeEditor from '$lib/components/CodeEditor.svelte'
  import { AIcon } from 'ace.svelte'
  import { mdiUpload, mdiDownload, mdiRefresh, mdiPlus, mdiPlay, mdiSquareRounded, mdiClockOutline  } from '@mdi/js'

  const LS = window.localStorage, SS = window.sessionStorage
  let url = $state(LS.url || 'http://localhost:22222/')
  let dumpPath = $state(LS.dumpPath || 'dump.json')
  let registers = $state({}), last = $state({})
  let newRegister = $state(''), focus = $state(false)
  let content = $state(''), code = $state('')
  let interval = $state(''), countdown = $state('N/A')
  let loading = $state(false), connected = $state(false)
  let refs = $state([[], [], []])

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
    loading = 'Reading'
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
    if (refs[0].includes(r)) res[1] = 3
    if (refs[1].includes(r)) res[1] = 4
    if (refs[2].includes(r)) res[1] = 5
    if (registers[r] !== last[r]) res[1] = 2
    if (r === focus) res[1] = 0
    return res
  }

  async function load () {
    if (loading || !connected) return
    loading = 'Loading'
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
    loading = 'Dumping'
    try {
      await srpc.dump(dumpPath)
    } catch (e) {
      Swal.fire('Error', e.toString(), 'error')
    }
    loading = false
  }

  async function cycle () {
    if (loading || !connected) return
    code = ''
    await readAll()
    loading = 'Cycling'
    try {
      code = await srpc.cycle()
    } catch (e) {
      Swal.fire('Error', e.toString(), 'error')
    }
    loading = false
  }

  async function run () {
    if (loading || !connected) return
    loading = 'Running'
    try {
      await srpc.run(code)
    } catch (e) {
      Swal.fire('Error', e.toString(), 'error')
    }
    loading = false
    readAll()
  }

  async function cycle2run () {
    if (loading || !connected) return
    await cycle()
    await run()
  }

  async function writeFocus () {
    if (loading || !connected) return
    loading = 'Writing'
    await srpc.write(focus, registers[focus])
    loading = false
  }

  function trace () {
    const match = r => [...code.matchAll(r)].map(match => Number(match[1]))
    refs[0] = match(/read\(([0-9a-fA-Fx]+)\)/g)
    refs[1] = match(/write\(([0-9a-fA-Fx]+)/g)
    refs[2] = match(/run\(([0-9a-fA-Fx]+)\)/g)
  }
  const debounceTrace = debounce(trace)
  $effect(() => { code; debounceTrace() })

  const sleep = ms => new Promise(r => setTimeout(r, ms))
  async function tick () {
    if (!(interval > 0)) return countdown = 'N/A'
    if (isNaN(countdown)) return countdown = 0
    if (countdown <= 0) {
      cycle2run()
      return countdown = Number(interval)
    }
    countdown--
  }
  async function loop () {
    while (1) {
      await tick()
      const n = Date.now()
      await sleep((Math.floor(n / 1000) + 1 - n / 1000) * 1000)
    }
  }
  loop()
</script>

<div class="w-full h-screen min-w-[768px] flex">
  <div class="w-1/2 h-full bg-gray-700 text-white">
    <div class="flex items-center justify-between p-4">
      <input bind:value={url} placeholder="Server URL" class="outline-none block grow">
      <div class="flex items-center">
        <b>{ connected ? (loading || 'Idle') : 'Disconnected'}</b>
        <button class="cursor-pointer w-5 h-5 font-bold ml-2 rounded-full {!connected ? 'bg-gray-500' : (loading ? 'bg-yellow-500' : 'bg-green-500')}" onclick={init} title="connect"></button>
      </div>
    </div>
    <div class="flex items-center px-3 justify-between">
      <div class="flex items-center grow">
        <button class="cursor-pointer transition-all hover:text-blue-300" onclick={load} title="load">
          <AIcon path={mdiUpload} size="1.75rem"></AIcon>
        </button>
        <button class="mx-1 cursor-pointer transition-all hover:text-blue-300" onclick={dump} title="dump">
          <AIcon path={mdiDownload} size="1.75rem"></AIcon>
        </button>
        <input bind:value={dumpPath} placeholder="Dump Path" class="outline-none block grow">
      </div>
      <div class="flex items-center">
        <button class="cursor-pointer mr-4 transition-all hover:scale-130 {loading === 'Cycling' ? 'text-yellow-500' : 'text-white'}" onclick={cycle} title="cycle">
          <AIcon path={mdiSquareRounded} size="2.25rem"></AIcon>
        </button>
        <button class="cursor-pointer transition-all hover:scale-130 {loading === 'Running' ? 'text-yellow-500' : 'text-white'}" onclick={run} title="run">
          <AIcon path={mdiPlay} size="2.5rem"></AIcon>
        </button>
      </div>
    </div>
    <div class="px-4 my-3 w-full flex items-center justify-between">
      <div class="flex items-center">
        <button class="cursor-pointer mr-2 transition-all hover:rotate-90" onclick={readAll} title="refresh">
          <AIcon path={mdiRefresh}></AIcon>
        </button>
        <div class="font-mono font-bold flex items-center">
          <AIcon path={mdiPlus}></AIcon>
          0x
          <input class="outline-none w-20 block" bind:value={newRegister} placeholder="______" onkeyup={newRegisterKeyup}>
        </div>
      </div>
      <div class="flex items-center">
        <code>{countdown} s</code>
        <AIcon path={mdiClockOutline} class="mx-2 { countdown <= 0 ? 'text-yellow-500' : 'text-white'}"></AIcon>
        <input class="outline-none font-mono border-2 border-white rounded px-2 py-1 block w-24 text-right" placeholder="N/A" bind:value={interval}>
      </div>
    </div>
    <div class="flex flex-wrap items-start p-4 w-full">
      {#each rs as r}
        <Cell {r} s={s(r)} onclick={() => focus = focus === r ? false : r } />
      {/each}
    </div>
  </div>
  <div class="w-1/2 h-full overflow-hidden">
    <div class="h-1/2">
      <CodeEditor bind:value={code}></CodeEditor>
    </div>
    <div class="h-1/2 transition-all {focus !== false ? 'bg-blue-200' : 'bg-gray-200'}">
      {#if focus !== false}
        <textarea class="w-full h-full outline-none p-2" bind:value={registers[focus]} onchange={writeFocus}></textarea>
      {/if}
    </div>
  </div>
</div>
