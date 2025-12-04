<script setup lang="ts">
import { computed } from 'vue'
import { Clock } from '@element-plus/icons-vue'
import type { KnowledgeItem } from '../types'

const props = defineProps<{
  notes: KnowledgeItem[]
  selectedId: number | null
}>()

const emit = defineEmits<{
  select: [id: number]
}>()

const formatDate = (value: string) => {
  const date = new Date(value)
  return date.toLocaleString()
}

const snippet = (content: string) => {
  const text = content.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim()
  return text.length > 140 ? `${text.slice(0, 140)}...` : text
}

const hasNotes = computed(() => props.notes.length > 0)
</script>

<template>
  <div class="note-list">
    <el-empty v-if="!hasNotes" description="还没有知识点，点击右上角创建吧" />
    <el-scrollbar v-else height="100%">
      <div
        v-for="note in notes"
        :key="note.id"
        class="note-card"
        :class="{ active: note.id === selectedId }"
        @click="emit('select', note.id)"
      >
        <div class="title-row">
          <h3>{{ note.title }}</h3>
          <div class="time">
            <el-icon><Clock /></el-icon>
            <span>{{ formatDate(note.updated_at) }}</span>
          </div>
        </div>
        <p class="snippet">{{ snippet(note.content) }}</p>
        <div class="tags" v-if="note.tags?.length">
          <el-tag v-for="tag in note.tags" :key="tag" size="small" effect="light">
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.note-list {
  height: 100%;
}
.note-card {
  background: #fff;
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 12px;
  border: 1px solid transparent;
  transition: all 0.2s ease;
  cursor: pointer;
}
.note-card:hover {
  border-color: #dfe6fd;
  box-shadow: 0 6px 18px rgba(93, 113, 255, 0.08);
}
.note-card.active {
  border-color: #4f46e5;
  box-shadow: 0 6px 24px rgba(79, 70, 229, 0.12);
}
.title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}
.title-row h3 {
  font-size: 16px;
  margin: 0;
  color: #111827;
}
.time {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #6b7280;
  font-size: 12px;
}
.snippet {
  color: #4b5563;
  margin: 8px 0 4px;
  line-height: 1.4;
}
.tags {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
</style>
