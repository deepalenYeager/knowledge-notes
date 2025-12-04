<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { ArrowLeft, Check, Close } from '@element-plus/icons-vue'
import { QuillEditor } from '@vueup/vue-quill'
import { useNotesStore } from '../stores/notes'

const route = useRoute()
const router = useRouter()
const store = useNotesStore()

const idParam = route.params.id
const noteId = idParam ? Number(idParam) : null

const formRef = ref<FormInstance>()
const loading = ref(false)

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
      <el-button text :icon="ArrowLeft" @click="handleCancel">返回</el-button>
      <div>
        <h2>{{ noteId ? '编辑知识点' : '新建知识点' }}</h2>
        <p class="subtitle">记录问题与收获，保持持续成长</p>
      </div>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-width="90px" class="form">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="一句话描述知识点" />
      </el-form-item>
      <el-form-item label="标签">
        <el-select
          v-model="form.tags"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="添加或选择标签"
        >
          <el-option v-for="tag in availableTags" :key="tag" :label="tag" :value="tag" />
        </el-select>
      </el-form-item>
      <el-form-item label="来源">
        <el-input v-model="form.source" placeholder="例如：书籍、链接、课程..." />
      </el-form-item>
      <el-form-item label="难度">
        <el-radio-group v-model="form.difficulty">
          <el-radio-button :label="0">简单</el-radio-button>
          <el-radio-button :label="1">一般</el-radio-button>
          <el-radio-button :label="2">较难</el-radio-button>
          <el-radio-button :label="null">未标注</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="正文" prop="content" class="rich-text-item">
        <QuillEditor
          v-model:content="form.content"
          theme="snow"
          toolbar="full"
          content-type="html"
          class="editor"
        />
      </el-form-item>
      <el-form-item class="actions-item">
        <div class="actions">
          <el-button :icon="Close" size="large" @click="handleCancel">取消</el-button>
          <el-button type="primary" :icon="Check" size="large" @click="handleSubmit">保存</el-button>
        </div>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.edit-page {
  max-width: 960px;
  margin: 0 auto;
  padding: 24px 18px 40px;
}
.header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}
.header h2 {
  margin: 0;
  font-size: 22px;
  color: #0f172a;
}
.subtitle {
  color: #6b7280;
  margin: 4px 0 0;
}
.form {
  background: #fff;
  border-radius: 14px;
  padding: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.04);
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.editor {
  width: 100%;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}
.editor :global(.ql-toolbar) {
  border: none;
  border-bottom: 1px solid #e5e7eb;
  background: #f8fafc;
}
.editor :global(.ql-container) {
  border: none !important;
  min-height: 360px;
  background: #fff;
}
.editor :global(.ql-editor) {
  min-height: 280px;
  font-size: 15px;
  line-height: 1.7;
}
.actions-item .el-form-item__content {
  justify-content: flex-end;
}
.actions {
  display: inline-flex;
  gap: 12px;
}
.rich-text-item .el-form-item__content {
  flex-direction: column;
}
</style>
