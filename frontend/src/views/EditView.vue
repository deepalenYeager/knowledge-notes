<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { ArrowLeft, Check, Close, Loading, Link } from '@element-plus/icons-vue'
import { QuillEditor } from '@vueup/vue-quill'
import { useNotesStore } from '../stores/notes'

const route = useRoute()
const router = useRouter()
const store = useNotesStore()

const idParam = route.params.id
const noteId = idParam ? Number(idParam) : null

const formRef = ref<FormInstance>()
const loading = ref(false)
const toolbarOptions = [
  [{ header: [1, 2, 3, false] }],
  ['bold', 'italic', 'underline', 'strike'],
  [{ list: 'ordered' }, { list: 'bullet' }],
  ['link', 'blockquote', 'code-block'],
  [{ color: [] }, { background: [] }],
  [{ align: [] }],
]

const form = reactive({
  title: '',
  tags: [] as string[],
  source: '',
  difficulty: null as number | null,
  content: '',
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入正文内容', trigger: 'blur' }],
}

const availableTags = computed(() => store.tags.map((t) => t.name))

const loadData = async () => {
  if (noteId) {
    const note = await store.fetchNote(noteId)
    form.title = note.title
    form.tags = note.tags ?? []
    form.source = note.source ?? ''
    form.difficulty = note.difficulty ?? null
    form.content = note.content
  }
  await store.loadTags()
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      if (noteId) {
        await store.updateNote(noteId, {
          title: form.title,
          tags: form.tags,
          source: form.source || null,
          difficulty: form.difficulty,
          content: form.content,
        })
        ElMessage.success('已更新')
      } else {
        const created = await store.addNote({
          title: form.title,
          tags: form.tags,
          source: form.source || null,
          difficulty: form.difficulty,
          content: form.content,
        })
        ElMessage.success('已创建')
        router.replace(`/edit/${created.id}`)
      }
      router.push('/')
    } catch (err) {
      ElMessage.error('保存失败，请稍后重试')
    } finally {
      loading.value = false
    }
  })
}

const handleCancel = () => {
  router.back()
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="edit-page" v-loading="loading">
    <div class="header">
      <div class="header-left">
        <el-button circle :icon="ArrowLeft" @click="handleCancel" class="back-btn" />
        <div>
          <h2 class="page-title">{{ noteId ? '编辑知识点' : '新建知识点' }}</h2>
        </div>
      </div>

      <div class="header-actions">
        <el-button :icon="Close" @click="handleCancel">取消</el-button>
        <el-button type="primary" :icon="Check" @click="handleSubmit">保存内容</el-button>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-position="top"
      class="main-form"
    >
      <div class="layout-grid">
        <div class="left-panel">
          <div class="panel-card">
            <h3 class="panel-title">基础信息</h3>
            <el-form-item label="标题" prop="title">
              <el-input
                v-model="form.title"
                type="textarea"
                :rows="2"
                placeholder="输入知识点标题..."
                class="title-input"
              />
            </el-form-item>

            <el-form-item label="标签">
              <el-select
                v-model="form.tags"
                multiple
                filterable
                allow-create
                default-first-option
                placeholder="选择标签"
                class="full-width"
              >
                <el-option
                  v-for="tag in availableTags"
                  :key="tag"
                  :label="tag"
                  :value="tag"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="难度等级">
              <el-radio-group v-model="form.difficulty" class="difficulty-group">
                <el-radio-button :label="0">简单</el-radio-button>
                <el-radio-button :label="1">一般</el-radio-button>
                <el-radio-button :label="2">较难</el-radio-button>
              </el-radio-group>
            </el-form-item>

            <el-form-item label="来源/出处">
              <el-input
                v-model="form.source"
                placeholder="例如：书籍、链接..."
                :prefix-icon="Link"
              />
            </el-form-item>
          </div>
        </div>

        <div class="right-panel">
          <el-form-item prop="content" class="editor-wrapper">
            <div class="editor-container">
              <QuillEditor
                v-model:content="form.content"
                theme="snow"
                :toolbar="toolbarOptions"
                content-type="html"
                class="custom-quill"
              />
            </div>
          </el-form-item>
        </div>
      </div>
    </el-form>
  </div>
</template>

<style scoped>
.edit-page {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #f8fafc;
}

/* --- Header Styles --- */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 24px;
  background: #fff;
  border-bottom: 1px solid #e2e8f0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.03);
  z-index: 10;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.page-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* --- Main Layout Grid --- */
.main-form {
  flex: 1;
  overflow: hidden;
  height: 100%;
  padding: 0;
}

.layout-grid {
  display: grid;
  grid-template-columns: 320px minmax(0, 1fr);
  gap: 0;
  height: 100%;
  width: 100%;
}

/* --- Left Panel (Metadata) --- */
.left-panel {
  padding: 24px;
  border-right: 1px solid #e2e8f0;
  background: #fff;
  overflow-y: auto;
}

.panel-card {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.panel-title {
  margin: 0 0 16px;
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
  font-weight: 700;
}

.title-input :deep(.el-textarea__inner) {
  font-size: 16px;
  font-weight: 600;
  padding: 10px;
}

.full-width {
  width: 100%;
}

.difficulty-group {
  width: 100%;
  display: flex;
}
.difficulty-group :deep(.el-radio-button) {
  flex: 1;
}
.difficulty-group :deep(.el-radio-button__inner) {
  width: 100%;
  padding: 8px 0;
}

/* --- Right Panel (Content) --- */
.right-panel {
  background-color: #f1f5f9;
  padding: 0;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Make the form item + content fill the space */
.editor-wrapper {
  width: 100%;
  max-width: none;
  margin: 0;
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Ensure Element Plus form-item content stretches */
.editor-wrapper :deep(.el-form-item__content) {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
}

/* Quill Editor Container – no card, full height */
.editor-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: transparent;
  border-radius: 0;
  box-shadow: none;
  width: 100%;
}

/* Quill root */
.custom-quill {
  display: flex;
  flex-direction: column;
  flex: 1;
  width: 100%;
}

/* Toolbar – borderless, stick to top */
.custom-quill :deep(.ql-toolbar) {
  border: none;
  border-bottom: 1px solid #e2e8f0;
  padding: 8px 12px;
  display: flex;
  justify-content: center;
  background: #f1f5f9;
  position: sticky;
  top: 0;
  z-index: 5;
}

/* Content container – full height, no border */
.custom-quill :deep(.ql-container) {
  border: none;
  font-size: 16px;
  line-height: 1.8;
  flex: 1;
  width: 100%;
}

/* Editor – this is the text area */
.custom-quill :deep(.ql-editor) {
  padding: 16px 20px;
  height: 100%;
  min-height: auto;
}

/* Responsive */
@media (max-width: 960px) {
  .layout-grid {
    grid-template-columns: 1fr;
    overflow-y: auto;
  }
  .left-panel {
    border-right: none;
    border-bottom: 1px solid #e2e8f0;
  }
  .right-panel {
    height: auto;
  }
  .custom-quill :deep(.ql-editor) {
    padding: 12px 12px;
  }
}
</style>
