<template>
  <div class="max-w-xl mx-auto">
    <div class="flex flex-col min-h-screen w-full">
      <div class="flex-1 overflow-y-auto bg-gray-100 p-4 rounded shadow mb-4" ref="scrollBox">
        <div v-for="(msg, idx) in messages" :key="idx" class="mb-1">
          <span class="bg-white px-3 py-1 min-w-20 rounded shadow">{{ msg }}</span>
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="h-16 flex gap-2">
        <input v-model="input" class="flex-1 border rounded px-3 py-1 h-16" placeholder="Type a message..." />
        <button class="bg-blue-600 text-white px-4 py-1 h-16 w-16 flex items-center justify-center rounded"
          type="submit">Send</button>
      </form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'

const input = ref('')
const messages = ref<string[]>([])
const scrollBox = ref<HTMLDivElement | null>(null)

let socket: WebSocket

onMounted(() => {
  socket = new WebSocket('ws://localhost:8000/ws')

  socket.onmessage = (event) => {
    messages.value.push(event.data)
  }
})

onBeforeUnmount(() => {
  socket?.close()
})

const sendMessage = () => {
  if (
    socket &&
    socket.readyState === WebSocket.OPEN &&
    input.value.trim()) {
    socket.send(input.value)
    input.value = ''
  } else if (socket.readyState === WebSocket.CONNECTING) {
    console.warn('WebSocket is still connecting...')
  } else {
    console.error('WebSocket is not open. Reconnecting...')
  }
}

// auto-scroll
watch(messages, () => {
  nextTick(() => {
    scrollBox.value?.scrollTo({ top: scrollBox.value.scrollHeight })
  })
})
</script>
