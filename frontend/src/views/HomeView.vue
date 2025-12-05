<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus, Refresh } from '@element-plus/icons-vue'
import NoteDetail from '../components/NoteDetail.vue'
import NoteList from '../components/NoteList.vue'
import { useNotesStore } from '../stores/notes'

const store = useNotesStore()
const router = useRouter()

const search = ref(store.searchKeyword)
const tagFilter = ref<string | null>(store.tagFilter)
const loading = computed(() => store.loading)
const notes = computed(() => store.notes)
const selected = computed(() => store.selectedNote)
const tags = computed(() => store.tags)

let searchTimer: number | null = null

const refresh = () => store.loadNotes({ q: search.value, tag: tagFilter.value || undefined })

const handleSearchInput = () => {
  if (searchTimer) {
    window.clearTimeout(searchTimer)
  }
  searchTimer = window.setTimeout(() => {
    refresh()
  }, 400)
}

const handleTagChange = () => refresh()

const handleSelect = (id: number) => {
  store.selectNote(id)
}

const goCreate = () => {
  router.push('/edit')
}

const goEdit = () => {
  if (!selected.value) return
  router.push(`/edit/${selected.value.id}`)
}

const confirmDelete = async () => {
  if (!selected.value) return
  try {
    await ElMessageBox.confirm('确定要删除这条知识点吗？此操作不可撤销。', '删除确认', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await store.removeNote(selected.value.id)
    ElMessage.success('已删除')
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败，请稍后重试')
    }
  }
}

onMounted(async () => {
  await Promise.all([store.loadNotes(), store.loadTags()])
})
</script>

<template>
  <div class="page">
    <header class="topbar">
      <div class="branding">
        <div class="title">知识盲点笔记</div>
        <p class="subtitle">快速记录与复盘自己的知识盲点</p>
      </div>
      <div class="actions">
        <el-input
          v-model="search"
          placeholder="搜索标题或正文..."
          clearable
          class="search"
          :prefix-icon="Search"
          @input="handleSearchInput"
        />
        <el-select
          v-model="tagFilter"
          clearable
          filterable
          placeholder="按标签过滤"
          class="tag-select"
          @change="handleTagChange"
        >
          <el-option v-for="tag in tags" :key="tag.name" :label="`${tag.name} (${tag.count})`" :value="tag.name" />
        </el-select>
        <el-button circle :icon="Refresh" @click="refresh" />
        <el-button type="primary" :icon="Plus" @click="goCreate">新建知识点</el-button>
      </div>
    </header>

    <section class="board" v-loading="loading">
      <div class="list-pane">
        <NoteList :notes="notes" :selected-id="store.selectedId" @select="handleSelect" />
      </div>
      <div class="detail-pane">
        <NoteDetail :note="selected" @edit="goEdit" @delete="confirmDelete" />
      </div>
    </section>
  </div>
</template>

<style scoped>
.page {
  width: 100%;
  margin: 0 auto;
  padding: 28px clamp(16px, 4vw, 36px) 40px;
}
.topbar {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 16px;
  margin-bottom: 16px;
}
.branding .title {
  font-size: 26px;
  font-weight: 700;
  color: #0f172a;
}
.subtitle {
  margin: 4px 0 0;
  color: #6b7280;
}
.actions {
  display: flex;
  gap: 10px;
  align-items: center;
}
.search {
  width: 280px;
}
.tag-select {
  width: 200px;
}
.board {
  display: grid;
  grid-template-columns: minmax(320px, 380px) 1fr;
  gap: 16px;
  min-height: calc(100vh - 180px);
}
.list-pane,
.detail-pane {
  height: calc(100vh - 180px);
  background: rgba(255, 255, 255, 0.4);
  border-radius: 16px;
  padding: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.04);
  backdrop-filter: blur(4px);
}
.detail-pane {
  padding: 0;
}
@media (max-width: 960px) {
  .board {
    grid-template-columns: 1fr;
  }
  .list-pane,
  .detail-pane {
    height: auto;
  }
  .topbar {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
