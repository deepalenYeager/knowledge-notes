export interface KnowledgeItem {
  id: number
  title: string
  content: string
  tags?: string[] | null
  source?: string | null
  difficulty?: number | null
  created_at: string
  updated_at: string
}

export interface KnowledgePayload {
  title: string
  content: string
  tags?: string[] | null
  source?: string | null
  difficulty?: number | null
}

export interface TagStat {
  name: string
  count: number
}

