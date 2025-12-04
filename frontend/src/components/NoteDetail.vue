<script setup lang="ts">
import { computed } from 'vue'
import DOMPurify from 'dompurify'
import { Edit, Delete, Link } from '@element-plus/icons-vue'
import type { KnowledgeItem } from '../types'

const props = defineProps<{
  note?: KnowledgeItem | null
}>()

const emit = defineEmits<{
  edit: []
  delete: []
}>()

const difficultyText = computed(() => {
  const map: Record<number, string> = {
    0: '简单',
    1: '一般',
    2: '较难',
  }
  const value = props.note?.difficulty
  return value === undefined || value === null ? '未标注' : map[value] ?? '未标注'
})

const sanitizedContent = computed(() => {
  if (!props.note?.content) return '<p>暂无内容</p>'
  return DOMPurify.sanitize(props.note.content)
})

const formatDate = (value?: string) => {
  if (!value) return ''
  return new Date(value).toLocaleString()
}
</script>

<template>
  <div class="detail-card" v-if="note">
    <div class="detail-header">
      <div>
        <h1>{{ note.title }}</h1>
        <div class="meta">
          <span>创建：{{ formatDate(note.created_at) }}</span>
          <span>更新：{{ formatDate(note.updated_at) }}</span>
        </div>
      </div>
      <div class="actions">
        <el-button type="primary" :icon="Edit" @click="emit('edit')">编辑</el-button>
        <el-button type="danger" plain :icon="Delete" @click="emit('delete')">删除</el-button>
      </div>
    </div>
    <div class="tags-row" v-if="note.tags?.length">
      <el-tag v-for="tag in note.tags" :key="tag" size="small" effect="plain">
        {{ tag }}
      </el-tag>
    </div>
    <div class="info-row">
      <el-tag type="info" size="small">难度：{{ difficultyText }}</el-tag>
      <el-tag v-if="note.source" type="warning" size="small" :icon="Link" effect="plain">
        {{ note.source }}
      </el-tag>
    </div>
    <div class="content" v-html="sanitizedContent"></div>
  </div>
  <el-empty v-else description="请选择一条知识点查看详情" />
</template>

<style scoped>
.detail-card {
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 10px 34px rgba(79, 70, 229, 0.08);
  height: 100%;
  overflow: auto;
}
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
}
.detail-header h1 {
  margin: 0;
  font-size: 22px;
  color: #0f172a;
}
.meta {
  color: #6b7280;
  display: flex;
  gap: 16px;
  font-size: 13px;
  margin-top: 8px;
}
.actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
.tags-row,
.info-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin: 12px 0;
}
.content {
  margin-top: 12px;
  line-height: 1.6;
  color: #111827;
}
.content :global(code) {
  background: #f3f4f6;
  padding: 2px 6px;
  border-radius: 6px;
}
.content :global(pre) {
  background: #0f172a;
  color: #f8fafc;
  padding: 12px;
  border-radius: 10px;
  overflow: auto;
}
</style>
