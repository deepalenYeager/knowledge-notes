import apiClient from './client'
import type { KnowledgeItem, KnowledgePayload, TagStat } from '../types'

export function listNotes(params?: { q?: string; tag?: string }) {
  return apiClient.get<KnowledgeItem[]>('/notes', { params })
}

export function getNote(id: number) {
  return apiClient.get<KnowledgeItem>(`/notes/${id}`)
}

export function createNote(payload: KnowledgePayload) {
  return apiClient.post<KnowledgeItem>('/notes', payload)
}

export function updateNote(id: number, payload: Partial<KnowledgePayload>) {
  return apiClient.put<KnowledgeItem>(`/notes/${id}`, payload)
}

export function deleteNote(id: number) {
  return apiClient.delete<void>(`/notes/${id}`)
}

export function exportNotes() {
  return apiClient.get<KnowledgeItem[]>('/export')
}

export function fetchTags() {
  return apiClient.get<TagStat[]>('/tags')
}

