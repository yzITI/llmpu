<script>
  import { onMount } from 'svelte'

  let { value = $bindable('') } = $props()

  let editorContainer
  let editorInstance

  onMount(async () => {
    self.MonacoEnvironment = {
      getWorker() {
        const blob = new Blob([''], { type: 'application/javascript' })
        return new Worker(URL.createObjectURL(blob))
      }
    }

    const monaco = await import('monaco-editor')

    editorInstance = monaco.editor.create(editorContainer, {
      value,
      language: 'python',
      theme: 'vs',
      lineNumbers: 'on',
      tabSize: 4,
      insertSpaces: true,
      wordWrap: 'on',
      wrappingIndent: 'indent',
      automaticLayout: true
    })

    const subscription = editorInstance.onDidChangeModelContent(() => {
      const current = editorInstance.getValue()
      if (current !== value) {
        value = current
      }
    })

    return () => {
      subscription.dispose()
      editorInstance.dispose()
    }
  })

  $effect(() => {
    if (value === editorInstance?.getValue() || !editorInstance) return
    editorInstance.setValue(value ?? '')
  })
</script>

<div bind:this={editorContainer} class="h-full w-full overflow-hidden"></div>
