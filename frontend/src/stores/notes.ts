import { defineStore } from 'pinia'
import {
  createNote as createNoteApi,
  deleteNote as deleteNoteApi,
  exportNotes as exportNotesApi,
  fetchTags as fetchTagsApi,
  getNote as getNoteApi,
  listNotes,
  updateNote as updateNoteApi,
} from '../api/notes'
import type { KnowledgeItem, KnowledgePayload, TagStat } from '../types'

export const useNotesStore = defineStore('notes', {
  state: () => ({
    notes: [] as KnowledgeItem[],
    selectedId: null as number | null,
    searchKeyword: '' as string,
    tagFilter: null as string | null,
    loading: false,
    tags: [] as TagStat[],
  }),
  getters: {
    selectedNote(state): KnowledgeItem | undefined {
      return state.notes.find((item) => item.id === state.selectedId)
    },
  },
  actions: {
    async loadNotes(params?: { q?: string; tag?: string }) {
      this.loading = true
      try {
        if (params?.q !== undefined) {
          this.searchKeyword = params.q
        }
        if (params?.tag !== undefined) {
          this.tagFilter = params.tag
        }
        const { data } = await listNotes({
          q: this.searchKeyword || undefined,
          tag: this.tagFilter || undefined,
        })
        this.notes = data
        if (!this.selectedId) {
          this.selectedId = data[0]?.id ?? null
        }
        if (this.selectedId && !this.notes.find((n) => n.id === this.selectedId)) {
          this.selectedId = data[0]?.id ?? null
        }
        return data
      } finally {
        this.loading = false
      }
    },
    selectNote(id: number) {
      this.selectedId = id
    },
    async fetchNote(id: number) {
      const { data } = await getNoteApi(id)
      const idx = this.notes.findIndex((n) => n.id === id)
      if (idx >= 0) {
        this.notes[idx] = data
      } else {
        this.notes.unshift(data)
      }
      return data
    },
    async addNote(payload: KnowledgePayload) {
      const { data } = await createNoteApi(payload)
      this.notes.unshift(data)
      this.selectedId = data.id
      return data
    },
    async updateNote(id: number, payload: Partial<KnowledgePayload>) {
      const { data } = await updateNoteApi(id, payload)
      this.notes = this.notes.map((n) => (n.id === id ? data : n))
      this.selectedId = id
      return data
    },
    async removeNote(id: number) {
      await deleteNoteApi(id)
      this.notes = this.notes.filter((n) => n.id !== id)
      if (this.selectedId === id) {
        this.selectedId = this.notes[0]?.id ?? null
      }
    },
    async loadTags() {
      const { data } = await fetchTagsApi()
      this.tags = data
      return data
    },
    async exportAll() {
      const { data } = await exportNotesApi()
      return data
    },
  },
})
